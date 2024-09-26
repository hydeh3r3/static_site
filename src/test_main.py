import unittest
from main import extract_title

class TestExtractTitle(unittest.TestCase):

    def test_extract_simple_title(self):
        markdown = "# Hello World"
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_extract_title_with_extra_content(self):
        markdown = "# My Title\n\nThis is some content.\n## Subtitle"
        self.assertEqual(extract_title(markdown), "My Title")

    def test_extract_title_with_leading_whitespace(self):
        markdown = "  #    Spaced Title    "
        self.assertEqual(extract_title(markdown), "Spaced Title")

    def test_raise_error_when_no_title(self):
        markdown = "This is just some text\nwithout a title"
        with self.assertRaises(ValueError):
            extract_title(markdown)

if __name__ == '__main__':
    unittest.main()