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

        sections = node.text.split(delimiter)
        current_type = text_type_text
        
        for i, section in enumerate(sections):
            new_nodes.append(TextNode(section, current_type))
            current_type = text_type if current_type == text_type_text else text_type_text

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

def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    # Process code formatting first to prevent conflicts
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    # Process bold before italic to handle nested formatting
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return [node for node in nodes if node.text]  # Remove empty nodes

def markdown_to_blocks(markdown):
    # Split the markdown into blocks based on headings, paragraphs, and list items
    blocks = re.split(r'(\n\s*\n|\n(?=\#))', markdown)
    
    # Strip leading and trailing whitespace from each block and remove empty blocks
    blocks = [block.strip() for block in blocks if block.strip()]
    
    # Combine consecutive list items into single blocks
    combined_blocks = []
    current_block = []
    for block in blocks:
        if block.startswith(('* ', '- ', '+ ')) or re.match(r'^\d+\.', block):
            current_block.append(block)
        else:
            if current_block:
                combined_blocks.append('\n'.join(current_block))
                current_block = []
            combined_blocks.append(block)
    if current_block:
        combined_blocks.append('\n'.join(current_block))
    
    # Separate ordered list items from unordered list items
    final_blocks = []
    for block in combined_blocks:
        if '\n' in block and (block.startswith(('* ', '- ', '+ ')) or re.match(r'^\d+\.', block)):
            unordered = []
            ordered = []
            for line in block.split('\n'):
                if line.startswith(('* ', '- ', '+ ')):
                    if ordered:
                        final_blocks.append('\n'.join(ordered))
                        ordered = []
                    unordered.append(line)
                elif re.match(r'^\d+\.', line):
                    if unordered:
                        final_blocks.append('\n'.join(unordered))
                        unordered = []
                    ordered.append(line)
            if unordered:
                final_blocks.append('\n'.join(unordered))
            if ordered:
                final_blocks.append('\n'.join(ordered))
        else:
            final_blocks.append(block)
    
    return final_blocks

def block_to_block_type(block):
    lines = block.split('\n')
    
    # Check for heading
    if block.startswith(('#', '##', '###', '####', '#####', '######')):
        return "heading"
    
    # Check for code block
    if block.startswith('```') and block.endswith('```'):
        return "code"
    
    # Check for quote block
    if all(line.startswith('>') for line in lines):
        return "quote"
    
    # Check for unordered list
    if all(line.startswith(('* ', '- ')) for line in lines):
        return "unordered_list"
    
    # Check for ordered list
    if all(line.strip().startswith(f"{i+1}. ") for i, line in enumerate(lines)):
        return "ordered_list"
    
    # If none of the above, it's a paragraph
    return "paragraph"