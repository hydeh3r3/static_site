import unittest
from textnode import TextNode, text_type_text, text_type_bold, text_type_italic, text_type_code, split_nodes_delimiter, split_nodes_link, split_nodes_image, text_type_image, text_type_link

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text", text_type_text)
        node2 = TextNode("This is a text", text_type_text)
        self.assertEqual(node1, node2)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        result = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is text with a ")
        self.assertEqual(result[0].text_type, text_type_text)
        self.assertEqual(result[1].text, "code block")
        self.assertEqual(result[1].text_type, text_type_code)
        self.assertEqual(result[2].text, " word")
        self.assertEqual(result[2].text_type, text_type_text)

    def test_split_bold(self):
        node = TextNode("This is **bold** text", text_type_text)
        result = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[1].text_type, text_type_bold)
        self.assertEqual(result[2].text, " text")

    def test_split_italic(self):
        node = TextNode("This is *italic* text", text_type_text)
        result = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[1].text_type, text_type_italic)
        self.assertEqual(result[2].text, " text")

    def test_no_split_needed(self):
        node = TextNode("Plain text without delimiters", text_type_text)
        result = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Plain text without delimiters")
        self.assertEqual(result[0].text_type, text_type_text)

    def test_empty_text(self):
        node = TextNode("", text_type_text)
        result = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(len(result), 1)  # Expecting one empty text node
        self.assertEqual(result[0].text, "")  # Should be empty

    def test_only_delimiters(self):
        node = TextNode("``", text_type_text)  # String of only delimiters
        result = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(len(result), 2)  # Expecting one empty text node
        self.assertEqual(result[0].text, "")  # Confirm that it's indeed an empty string
        self.assertEqual(result[0].text_type, text_type_text)  # Check the text type

    def test_unmatched_delimiter(self):
        node = TextNode("Unmatched `delimiter", text_type_text)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", text_type_code)

    def test_multiple_nodes(self):
        nodes = [
            TextNode("First `code`", text_type_text),
            TextNode("**Bold** text", text_type_text),
            TextNode("No delimiters", text_type_text)
        ]
        result = split_nodes_delimiter(nodes, "`", text_type_code)
        result = split_nodes_delimiter(result, "**", text_type_bold)
        self.assertEqual(len(result), 7)

    def test_nested_delimiters(self):
        node = TextNode("Nested `code **with bold**`", text_type_text)
        result = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].text, "code **with bold**")
        self.assertEqual(result[1].text_type, text_type_code)

class TestSplitNodesImage(unittest.TestCase):
    def test_split_image(self):
        node = TextNode("This is an ![image](https://example.com/image.jpg) in text", text_type_text)
        result = split_nodes_image([node])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is an ")
        self.assertEqual(result[1].text, "image")
        self.assertEqual(result[1].text_type, text_type_image)
        self.assertEqual(result[1].url, "https://example.com/image.jpg")
        self.assertEqual(result[2].text, " in text")

    def test_multiple_images(self):
        node = TextNode("![First](first.jpg) and ![Second](second.jpg)", text_type_text)
        result = split_nodes_image([node])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text_type, text_type_image)
        self.assertEqual(result[1].text, " and ")
        self.assertEqual(result[2].text_type, text_type_image)

    def test_no_images(self):
        node = TextNode("Just plain text", text_type_text)
        result = split_nodes_image([node])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], node)

    def test_empty_node(self):
        node = TextNode("", text_type_text)
        result = split_nodes_image([node])
        self.assertEqual(len(result), 0)

class TestSplitNodesLink(unittest.TestCase):
    def test_split_link(self):
        node = TextNode("This is a [link](https://example.com) in text", text_type_text)
        result = split_nodes_link([node])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is a ")
        self.assertEqual(result[1].text, "link")
        self.assertEqual(result[1].text_type, text_type_link)
        self.assertEqual(result[1].url, "https://example.com")
        self.assertEqual(result[2].text, " in text")

    def test_multiple_links(self):
        node = TextNode("[First](first.com) and [Second](second.com)", text_type_text)
        result = split_nodes_link([node])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text_type, text_type_link)
        self.assertEqual(result[1].text, " and ")
        self.assertEqual(result[2].text_type, text_type_link)

    def test_no_links(self):
        node = TextNode("Just plain text", text_type_text)
        result = split_nodes_link([node])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], node)

    def test_empty_node(self):
        node = TextNode("", text_type_text)
        result = split_nodes_link([node])
        self.assertEqual(len(result), 0)

    def test_complex_scenario(self):
        node = TextNode("Text with [link](https://example.com) and ![image](image.jpg) mixed", text_type_text)
        result = split_nodes_link([node])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].text_type, text_type_link)
        result = split_nodes_image(result)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[3].text_type, text_type_image)

if __name__ == "__main__":
    unittest.main()