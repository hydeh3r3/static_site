class TextNode:
    def __init__(self, text, text_type, url):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode(text='{self.text}', text_type='{self.text_type}', url='{self.url}')"
    
    def render(self, include_url=True):
        if self.url and include_url:
            return f"[{self.text}]({self.url})"
        return self.text
        
    def __str__(self):
        return self.render()