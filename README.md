# Static Site Generator Documentation

## Overview

This project implements a static site generator that converts Markdown content into HTML. It includes functionality for parsing Markdown syntax, converting it to an intermediate representation, and finally rendering it as HTML.

## Main Components

### TextNode

```
class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text", text_type_text)
        node2 = TextNode("This is a text", text_type_text)
        self.assertEqual(node1, node2)
```

The `TextNode` class represents a piece of text with a specific type (e.g., plain text, bold, italic, code). It's the fundamental building block for parsing Markdown content.

### HTMLNode

```
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
```

The `HTMLNode` class is the base class for representing HTML elements. It includes methods for rendering HTML and handling properties (attributes).

### LeafNode

```
class TestLeafNode(unittest.TestCase):
    
    def test_to_html_with_tag_and_value(self):
        """Test rendering of LeafNode with a tag and value"""
        node = LeafNode("p", "This is a paragraph of text.")
        expected_html = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node.to_html(), expected_html)
        self.assertEqual(node.to_html(), expected_html)
    def test_to_html_with_props(self):
        """Test rendering of LeafNode with props (attributes)"""
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected_html = "<a href='https://www.google.com'>Click me!</a>"
        self.assertEqual(node.to_html(), expected_html)
        self.assertEqual(node.to_html(), expected_html)
    def test_to_html_without_tag(self):
        """Test rendering of LeafNode with no tag (raw text)"""
        node = LeafNode(None, "Raw text content.")
        expected_html = "Raw text content."
        self.assertEqual(node.to_html(), expected_html)
        self.assertEqual(node.to_html(), expected_html)
    def test_to_html_missing_value(self):
        """Test that missing value raises a ValueError"""
        with self.assertRaises(ValueError):
            node = LeafNode("p", "")
            node.to_html()
```

`LeafNode` is a subclass of `HTMLNode` that represents HTML elements without children, such as `<p>` or `<a>` tags.

### Markdown Parsing Functions

1. `split_nodes_delimiter`: Splits text nodes based on Markdown delimiters (e.g., `**` for bold, `*` for italic).
2. `split_nodes_link`: Parses Markdown links.
3. `split_nodes_image`: Parses Markdown images.
4. `text_to_textnodes`: Converts raw text to a list of `TextNode` objects.
5. `markdown_to_blocks`: Splits Markdown content into blocks (paragraphs, headings, lists).
6. `block_to_block_type`: Determines the type of a Markdown block (e.g., heading, paragraph, list).
7. `markdown_to_html_node`: Converts Markdown content to an `HTMLNode` tree.

## Testing

The project includes comprehensive unit tests for all major components and functions. Test cases cover various scenarios, including:

- Basic text node equality
- Splitting text nodes with delimiters
- Parsing links and images
- Converting complex Markdown to HTML structures

## Usage

To use the static site generator:

1. Load Markdown content from a file or string.
2. Use `markdown_to_html_node` to convert the Markdown to an `HTMLNode` tree.
3. Call the `to_html` method on the root `HTMLNode` to generate the final HTML output.

## Future Improvements

1. Implement support for more Markdown features (e.g., tables, blockquotes).
2. Add a command-line interface for easy use.
3. Implement a file watcher for automatic regeneration of HTML when Markdown files change.
4. Add support for custom templates and themes.
