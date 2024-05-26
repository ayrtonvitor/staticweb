import unittest
from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()
