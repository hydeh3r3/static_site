import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_repr(self):
        """Test the __repr__ method for correct output"""
        node = HTMLNode(tag='div', value='Hello', children=[], props={})
        expected_repr = "htmlnode(tag='div', value='Hello', children='[]', props='{}')"
        self.assertEqual(repr(node), expected_repr)

    def test_render(self):
        """Test the render method for correct HTML output"""
        node = HTMLNode(tag='p', value='This is a paragraph', children=[], props={})
        expected_render = "<p>This is a paragraph</[]>"
        self.assertEqual(node.render(), expected_render)

    def test_props_to_html(self):
        """Test the props_to_html method for correct property rendering"""
        node = HTMLNode(tag='img', value='', children=[], props={'src': 'image.jpg', 'alt': 'An image'})
        expected_props = "src='image.jpg'alt='An image'"
        self.assertEqual(node.props_to_html(), expected_props)

    def test_not_implemented_to_html(self):
        """Test that to_html method raises NotImplementedError"""
        node = HTMLNode(tag='div', value='Content', children=[], props={})
        with self.assertRaises(NotImplementedError):
            node.to_html()

if __name__ == '__main__':
    unittest.main()
