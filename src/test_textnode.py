import unittest
from textnode import TextNode, text_type_text, text_type_bold, text_type_italic, text_type_code, split_nodes_delimiter, split_nodes_link, split_nodes_image, text_type_image, text_type_link, text_to_textnodes, markdown_to_blocks

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
        self.assertEqual(len(result), 3)  # Empty text, code, empty text
        self.assertEqual(result[0].text_type, text_type_text)
        self.assertEqual(result[1].text_type, text_type_code)
        self.assertEqual(result[2].text_type, text_type_text)

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

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_no_special_text(self):
        text = "This is just plain text"
        expected = [TextNode("This is just plain text", text_type_text)]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_multiple_bold(self):
        text = "This **is** **bold** text"
        expected = [
            TextNode("This ", text_type_text),
            TextNode("is", text_type_bold),
            TextNode(" ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" text", text_type_text),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_with_links_and_images(self):
        text = "Check out this [link](https://example.com) and ![image](https://example.com/image.jpg)"
        expected = [
            TextNode("Check out this ", text_type_text),
            TextNode("link", text_type_link, "https://example.com"),
            TextNode(" and ", text_type_text),
            TextNode("image", text_type_image, "https://example.com/image.jpg"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

class TestMarkdownToBlocks(unittest.TestCase):
    def test_basic_split(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_remove_empty_blocks(self):
        markdown = "# Heading\n\n\n\nParagraph\n\n\n* List item\n\n\n"
        expected = [
            "# Heading",
            "Paragraph",
            "* List item"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_mixed_content(self):
        markdown = "# Heading 1\n\nParagraph 1\n\n## Heading 2\n\nParagraph 2\n\n* List item 1\n* List item 2\n\n1. Ordered item 1\n2. Ordered item 2"
        expected = [
            "# Heading 1",
            "Paragraph 1",
            "## Heading 2",
            "Paragraph 2",
            "* List item 1\n* List item 2",
            "1. Ordered item 1\n2. Ordered item 2"
        ]
        actual = markdown_to_blocks(markdown)
        print("Actual:", actual)
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()