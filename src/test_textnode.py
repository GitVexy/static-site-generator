import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)

        self.assertEqual(node, node2)

    def test_not_eq(self):
        node    = TextNode("Test 1", TextType.ITALIC)
        node2   = TextNode("Test 2", TextType.BOLD, "https://boot.dev/")

        self.assertNotEqual(node, node2)

    def test_type_text(self):
        node = TextNode(1, TextType.NORMAL, True)

        self.assertIsInstance(node.text, str)

    def test_type_text_type(self):
        node = TextNode(1, TextType.NORMAL, 69)

        self.assertIsInstance(node.text_type, TextType)

    def test_type_url_string(self):
        node = TextNode(1, TextType.NORMAL, "https://boot.dev/")

        self.assertIsInstance(node.url, str)

    def test_type_url_none(self):
        node = TextNode(1, TextType.NORMAL)

        self.assertIsInstance(node.url, type(None))


if __name__ == "__main__":
    unittest.main()
