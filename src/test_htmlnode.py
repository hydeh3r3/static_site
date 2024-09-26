import unittest
from htmlnode import HTMLNode,LeafNode,ParentNode, text_node_to_html_node

class TestHTMLNode(unittest.TestCase):

    def test_repr(self):
        """Test the __repr__ method for correct output"""
        node = HTMLNode(tag='div', value='Hello', children=[], props={})
        expected_repr = "HTMLNode(tag='div', value='Hello', children=[], props={})"
        self.assertEqual(repr(node), expected_repr)

    def test_render(self):
        """Test the render method for correct HTML output"""
        node = HTMLNode(tag='p', value='This is a paragraph', children=[], props={})
        expected_render = "<p>This is a paragraph</[]>"
        self.assertEqual(node.render(), expected_render)

    def test_props_to_html(self):
        """Test the props_to_html method for correct property rendering"""
        node = HTMLNode(tag='img', value='', children=[], props={'src': 'image.jpg', 'alt': 'An image'})
        expected_props = "src='image.jpg' alt='An image'"  # Notice the space here
        self.assertEqual(node.props_to_html(), expected_props)

    def test_not_implemented_to_html(self):
        """Test that to_html method raises NotImplementedError"""
        node = HTMLNode(tag='div', value='Content', children=[], props={})
        with self.assertRaises(NotImplementedError):
            node.to_html()

class TestLeafNode(unittest.TestCase):
    
    def test_to_html_with_tag_and_value(self):
        """Test rendering of LeafNode with a tag and value"""
        node = LeafNode("p", "This is a paragraph of text.")
        expected_html = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_with_props(self):
        """Test rendering of LeafNode with props (attributes)"""
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected_html = "<a href='https://www.google.com'>Click me!</a>"
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_without_tag(self):
        """Test rendering of LeafNode with no tag (raw text)"""
        node = LeafNode(None, "Raw text content.")
        expected_html = "Raw text content."
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_missing_value(self):
        """Test that missing value raises a ValueError"""
        with self.assertRaises(ValueError):
            node = LeafNode("p", "")
            node.to_html()

class TestParentNode(unittest.TestCase):

    def test_parent_node_with_children(self):
        """Test that ParentNode correctly renders with child LeafNodes"""
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
            ]
        )
        expected_html = "<p><b>Bold text</b>Normal text<i>italic text</i></p>"
        self.assertEqual(node.to_html(), expected_html)

    def test_parent_node_missing_tag(self):
        """Test that missing tag raises a ValueError"""
        with self.assertRaises(ValueError):
            node = ParentNode(
                None,
                [LeafNode("b", "Bold text")]
            )
            node.to_html()

    def test_parent_node_missing_children(self):
        """Test that missing children raises a ValueError"""
        with self.assertRaises(ValueError):
            node = ParentNode("div", [])
            node.to_html()

    def test_nested_parent_node(self):
        """Test rendering of nested ParentNodes"""
        node = ParentNode(
            "div",
            [
                LeafNode("b", "Bold text"),
                ParentNode(
                    "p",
                    [
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Some normal text"),
                    ]
                ),
                LeafNode(None, "Additional text outside the paragraph.")
            ]
        )
        expected_html = (
            "<div><b>Bold text</b>"
            "<p><i>italic text</i>Some normal text</p>"
            "Additional text outside the paragraph.</div>"
        )
        self.assertEqual(node.to_html(), expected_html)

    def test_parent_node_with_props(self):
        """Test ParentNode with props rendering"""
        node = ParentNode(
            "a",
            [LeafNode(None, "Click me!")],
            {"href": "https://example.com", "class": "link"}
        )
        expected_html = "<a href='https://example.com' class='link'>Click me!</a>"
        self.assertEqual(node.to_html(), expected_html)

class TestTextNodeConversion(unittest.TestCase):
    
    def test_text_type_text(self):
        text_node = {"type": "text", "text": "Simple text"}
        node = text_node_to_html_node(text_node)
        self.assertEqual(node.to_html(), "Simple text")

    def test_text_type_bold(self):
        text_node = {"type": "bold", "text": "Bold text"}
        node = text_node_to_html_node(text_node)
        self.assertEqual(node.to_html(), "<b>Bold text</b>")

    def test_text_type_italic(self):
        text_node = {"type": "italic", "text": "Italic text"}
        node = text_node_to_html_node(text_node)
        self.assertEqual(node.to_html(), "<i>Italic text</i>")

    def test_text_type_code(self):
        text_node = {"type": "code", "text": "code block"}
        node = text_node_to_html_node(text_node)
        self.assertEqual(node.to_html(), "<code>code block</code>")

    def test_text_type_link(self):
        text_node = {"type": "link", "text": "Google", "url": "https://www.google.com"}
        node = text_node_to_html_node(text_node)
        self.assertEqual(node.to_html(), "<a href='https://www.google.com'>Google</a>")

    def test_text_type_image(self):
        text_node = {"type": "image", "src": "image.jpg", "alt": "An image"}
        node = text_node_to_html_node(text_node)
        self.assertEqual(node.to_html(), "<img src='image.jpg' alt='An image' />")

    def test_unknown_type(self):
        text_node = {"type": "unknown", "text": "Unknown type"}
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)

if __name__ == '__main__':
    unittest.main()
