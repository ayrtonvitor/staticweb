import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold
)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is another text node", text_type_bold)
        node3 = TextNode("This is a text node", text_type_bold, "http://www.abc.com")
        node4 = TextNode("This is a text node", text_type_text)
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)

    def test_eq_url(self):
        node = TextNode("This is a text node", text_type_text, "https://www.abc.com")
        node2 = TextNode("This is a text node", text_type_text, "https://www.abc.com")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_text, "https://www.abc.com")
        self.assertEqual("TextNode(This is a text node, text, https://www.abc.com)", repr(node))

if __name__ == "__main__":
    unittest.main()
