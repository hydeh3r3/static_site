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
        return "".join([f"{key}='{value}'" for key, value in self.props.items()])
    