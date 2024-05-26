import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
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

    def test_to_html_node_no_type(self):
        node = TextNode("This is a text node", None)
        with self.assertRaises(ValueError) as cm:
            node.text_node_to_html_node()
        self.assertEqual(str(cm.exception), "A text node must have a text type")

    def test_to_html_node_type_not_supported(self):
        node = TextNode("This is a text node", "error_type")
        with self.assertRaises(ValueError) as cm:
            node.text_node_to_html_node()
        self.assertEqual(str(cm.exception), "Text type error_type is not supported")

    def test_to_html_node_text(self):
        node = TextNode("This is a text node", text_type_text, "https://www.abc.com")
        html_node = node.text_node_to_html_node()
        self.assertEqual("This is a text node", html_node.to_html())

    def test_to_html_node_bold(self):
        node = TextNode("This is a text node", text_type_bold, "https://www.abc.com")
        html_node = node.text_node_to_html_node()
        self.assertEqual("<b>This is a text node</b>", html_node.to_html())

    def test_to_html_node_italic(self):
        node = TextNode("This is a text node", text_type_italic, "https://www.abc.com")
        html_node = node.text_node_to_html_node()
        self.assertEqual("<i>This is a text node</i>", html_node.to_html())

    def test_to_html_node_code(self):
        node = TextNode("This is a text node", text_type_code, "https://www.abc.com")
        html_node = node.text_node_to_html_node()
        self.assertEqual("<code>This is a text node</code>", html_node.to_html())

    def test_to_html_node_link(self):
        node = TextNode("This is a text node", text_type_link, "https://www.abc.com")
        html_node = node.text_node_to_html_node()
        self.assertEqual('<a href="https://www.abc.com">This is a text node</a>', html_node.to_html())

    def test_to_html_node_image(self):
        node = TextNode("This is a text node", text_type_image, "https://www.abc.com")
        html_node = node.text_node_to_html_node()
        self.assertEqual('<img src="https://www.abc.com" alt="This is a text node"></img>', html_node.to_html())


if __name__ == "__main__":
    unittest.main()
