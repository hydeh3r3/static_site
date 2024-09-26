class HTMLNode:
    def __init__(self, tag, value, children, props):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"htmlnode(tag='{self.tag}', value='{self.value}', children='{self.children}', props='{self.props}')"
    
    def render(self):
        return f"<{self.tag}>{self.value}</{self.children}>"

    def to_html(self):
        raise NotImplementedError("This method must be implemented by a subclass")

    def props_to_html(self):
        return " ".join([f"{key}='{value}'" for key, value in self.props.items()])
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if props is None:
            props = {}
        super().__init__(tag, value, [], props)

    def to_html(self):
        # If tag is None, return the value as raw text
        if self.tag is None:
            return self.value

        # Render props as HTML attributes
        props_html = self.props_to_html()

        # Special case for self-closing tags like <img>
        if self.tag == "img":
            return f"<{self.tag} {props_html} />"

        # For other tags, raise ValueError if value is missing
        if not self.value:
            raise ValueError(f"LeafNode with tag '{self.tag}' must have a value.")

        # Render the tag with the value
        if props_html:
            return f"<{self.tag} {props_html}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if props is None:
            props = {}
        if not children:
            raise ValueError("Must have children nodes.")
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag.")
        
        # Recursively render all children using their `to_html` methods
        children_html = "".join([child.to_html() for child in self.children])
        
        # Render the props
        props_html = self.props_to_html()
        
        # Render the tag with the children
        if props_html:
            return f"<{self.tag} {props_html}>{children_html}</{self.tag}>"
        else:
            return f"<{self.tag}>{children_html}</{self.tag}>"

def text_node_to_html_node(text_node):
    node_type = text_node.get("type")
    text = text_node.get("text", "")
    
    if node_type == "text":
        return LeafNode(None, text)
    elif node_type == "bold":
        return LeafNode("b", text)
    elif node_type == "italic":
        return LeafNode("i", text)
    elif node_type == "code":
        return LeafNode("code", text)
    elif node_type == "link":
        url = text_node.get("url")
        return LeafNode("a", text, {"href": url})
    elif node_type == "image":
        src = text_node.get("src")
        alt = text_node.get("alt")
        return LeafNode("img", "", {"src": src, "alt": alt})
    else:
        raise ValueError(f"Unknown TextNode type: {node_type}")