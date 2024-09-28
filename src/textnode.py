from htmlnode import HTMLNode, LeafNode, ParentNode
import re

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

def block_to_html_node(block, block_type):
    if block_type == "paragraph":
        return paragraph_to_html_node(block)
    elif block_type == "heading":
        return heading_to_html_node(block)
    elif block_type == "code":
        return code_to_html_node(block)
    elif block_type == "quote":
        return quote_to_html_node(block)
    elif block_type == "unordered_list":
        return unordered_list_to_html_node(block)
    elif block_type == "ordered_list":
        return ordered_list_to_html_node(block)
    else:
        raise ValueError(f"Invalid block type: {block_type}")

def paragraph_to_html_node(block):
    text_nodes = text_to_textnodes(block)
    child_nodes = text_nodes_to_html_nodes(text_nodes)
    return ParentNode("p", child_nodes)

def text_nodes_to_html_nodes(text_nodes):
    html_nodes = []
    for text_node in text_nodes:
        if isinstance(text_node, str):
            html_nodes.append(LeafNode(None, text_node))
        elif text_node.text_type == text_type_text:
            html_nodes.append(LeafNode(None, text_node.text))
        elif text_node.text_type == text_type_bold:
            html_nodes.append(LeafNode("b", text_node.text))
        elif text_node.text_type == text_type_italic:
            html_nodes.append(LeafNode("i", text_node.text))
        elif text_node.text_type == text_type_code:
            html_nodes.append(LeafNode("code", text_node.text))
        elif text_node.text_type == text_type_link:
            html_nodes.append(LeafNode("a", text_node.text, {"href": text_node.url}))
        elif text_node.text_type == text_type_image:
            html_nodes.append(LeafNode("img", "", {"src": text_node.url, "alt": text_node.text}))
        else:
            raise ValueError(f"Invalid text type: {text_node.text_type}")
    return html_nodes

def heading_to_html_node(block):
    level = block.count("#")
    content = block.lstrip("#").strip()
    children = text_to_children(content)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    code_content = block.strip("`").strip()
    return ParentNode("pre", [ParentNode("code", [LeafNode(None, code_content)])])

def code_to_html_node(block):
    code_content = block.strip("`").strip()
    return ParentNode("pre", [ParentNode("code", [LeafNode(None, code_content)])])

def quote_to_html_node(block):
    return ParentNode("blockquote", text_to_children(block[2:]))

def unordered_list_to_html_node(block):
    items = block.split("\n")
    list_items = [ParentNode("li", text_nodes_to_html_nodes(text_to_textnodes(item.strip("* ")))) for item in items if item.strip()]
    return ParentNode("ul", list_items)

def ordered_list_to_html_node(block):
    items = block.split("\n")
    list_items = [ParentNode("li", text_nodes_to_html_nodes(text_to_textnodes(item.split(". ", 1)[1]))) for item in items if item.strip()]
    return ParentNode("ol", list_items)

def text_to_children(text):
    nodes = text_to_textnodes(text)
    return [textnode_to_html_node(node) for node in nodes]

def textnode_to_html_node(node):
    if isinstance(node, str):
        return LeafNode(None, node)
    elif node.text_type == text_type_text:
        return LeafNode(None, node.text)
    elif node.text_type == text_type_bold:
        return LeafNode("b", node.text)
    elif node.text_type == text_type_italic:
        return LeafNode("i", node.text)
    elif node.text_type == text_type_code:
        return LeafNode("code", node.text)
    elif node.text_type == text_type_link:
        return LeafNode("a", node.text, {"href": node.url})
    elif node.text_type == text_type_image:
        return LeafNode("img", "", {"src": node.url, "alt": node.text})
    else:
        raise ValueError(f"Invalid text type: {node.text_type}")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_to_html_node(block, block_type)
        if isinstance(html_node, (LeafNode, ParentNode)):
            children.append(html_node)
        elif isinstance(html_node, str):
            children.append(LeafNode(None, html_node))
        else:
            raise ValueError(f"Unexpected node type: {type(html_node)}")
    return ParentNode("div", children)