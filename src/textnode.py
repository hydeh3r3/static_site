# Define TextNode types
text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            isinstance(other, TextNode)
            and self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode(text='{self.text}', text_type='{self.text_type}', url='{self.url}')"

    def render(self, include_url=True):
        if self.url and include_url:
            return f"[{self.text}]({self.url})"
        return self.text

    def __str__(self):
        return self.render()

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        
        parts = node.text.split(delimiter)
        
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax: Unmatched delimiter '{delimiter}'")
        
        # Process each part, alternating between text type
        for i, part in enumerate(parts):
            if part:  # If part is not empty
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, text_type_text))  # Even index is text
                else:
                    new_nodes.append(TextNode(part, text_type))  # Odd index is the current text_type
            elif i % 2 == 0:  # If the part is empty and it's an even index
                new_nodes.append(TextNode("", text_type_text))  # Ensure to add an empty text node

    # Handle edge cases for only delimiters or empty string
    if len(new_nodes) == 0:
        new_nodes.append(TextNode("", text_type_text))
    
    return new_nodes

import re

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        
        pattern = r"!\[(.*?)\]\((.*?)\)"
        matches = re.finditer(pattern, node.text)
        last_end = 0
        
        for match in matches:
            start, end = match.span()
            if start > last_end:
                new_nodes.append(TextNode(node.text[last_end:start], text_type_text))
            
            alt_text = match.group(1)
            image_url = match.group(2)
            new_nodes.append(TextNode(alt_text, text_type_image, image_url))
            
            last_end = end
        
        if last_end < len(node.text):
            new_nodes.append(TextNode(node.text[last_end:], text_type_text))
    
    return [node for node in new_nodes if node.text]

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        
        pattern = r'(?<!!)\[([^\]]+)\]\(([^)]+)\)'  # This pattern excludes image syntax
        parts = re.split(pattern, node.text)
        
        for i, part in enumerate(parts):
            if i % 3 == 0:  # Text part
                if part:
                    new_nodes.append(TextNode(part, text_type_text))
            elif i % 3 == 1:  # Link text
                link_text = part
            else:  # Link URL
                new_nodes.append(TextNode(link_text, text_type_link, part))
    
    return [node for node in new_nodes if node.text]