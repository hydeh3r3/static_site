import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold", "https://boot.dev")
        node2 = TextNode("This is a text node", "bold", "https://boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", "bold", "https://boot.dev")
        self.assertEqual(repr(node), "TextNode(text='This is a text node', text_type='bold', url='https://boot.dev')")
    
    def test_render(self):
        node = TextNode("This is a text node", "bold", "https://boot.dev")
        self.assertEqual(node.render(include_url=False), "This is a text node")

    def test_render_with_url(self):
        node = TextNode("This is a text node", "bold", "https://boot.dev")
        self.assertEqual(node.render(), "[This is a text node](https://boot.dev)")
        
    def test_url_is_none(self):
        node = TextNode("This is a text node", "bold", None)
        self.assertEqual(node.render(), "This is a text node")

if __name__ == "__main__":
    unittest.main()