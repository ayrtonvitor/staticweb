import unittest
from htmlnode import (
    HTMLNode,
    LeafNode
    )

class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            'div',
            'Hello, world!',
            None,
            {'class': 'greeting', 'href': 'https://abc.com'})
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://abc.com"'
        )

    def test_raise_if_to_html(self):
        node = HTMLNode(
            'div',
            'Hello, world!',
            None,
            {'class': 'greeting', 'href': 'https://abc.com'})
        self.assertRaises(NotImplementedError, node.to_html)

class TestLeafNode(unittest.TestCase):
    def test_to_html_no_props(self):
        leaf = LeafNode("p", "This is a paragraph of text.")

        self.assertEqual(
            '<p>This is a paragraph of text.</p>',
            leaf.to_html())

    def test_to_html_props(self):
        leaf = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(
            '<a href="https://www.google.com">Click me!</a>',
            leaf.to_html())

    def test_to_html_no_tag(self):
        leaf = LeafNode(None, "Hello, world!")

        self.assertEqual(
            'Hello, world!',
            leaf.to_html())

    def test_to_html_no_value(self):
        leaf = LeafNode('a', None)
        self.assertRaises(ValueError, leaf.to_html)

if __name__ == "__main__":
    unittest.main()
