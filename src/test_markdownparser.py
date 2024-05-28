from types import new_class
import unittest
from markdownparser import (
    MarkdownParser,
    markdown_bold_delimiter,
    markdown_code_delimiter,
    markdown_italic_delimiter,
)

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)

class TestMarkdownParser(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        markdown_parser = MarkdownParser(node)
        markdown_parser.split_nodes_delimiter(markdown_code_delimiter, text_type_code)

        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]
        self.assertListEqual(markdown_parser.nodes, expected)


    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold block** word", text_type_text)
        markdown_parser = MarkdownParser(node)
        markdown_parser.split_nodes_delimiter(markdown_bold_delimiter, text_type_bold)

        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("bold block", text_type_bold),
            TextNode(" word", text_type_text),
        ]
        self.assertListEqual(markdown_parser.nodes, expected)

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with a *italic block* word", text_type_text)
        markdown_parser = MarkdownParser(node)
        markdown_parser.split_nodes_delimiter(markdown_italic_delimiter, text_type_italic)

        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("italic block", text_type_italic),
            TextNode(" word", text_type_text),
        ]
        self.assertListEqual(markdown_parser.nodes, expected)

    def test_split_nodes_delimiter_italic_and_bold(self):
        node = TextNode("This is text with a *italic block* and **bold** word", text_type_text)
        markdown_parser = MarkdownParser(node)
        markdown_parser.split_nodes_delimiter(markdown_bold_delimiter, text_type_bold)

        expected_bold = [
            TextNode("This is text with a *italic block* and ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" word", text_type_text),
        ]
        self.assertListEqual(markdown_parser.nodes, expected_bold)

    def test_split_nodes_delimiter_italic_after_bold(self):
        node = TextNode("This is text with a *italic block* and **bold** word", text_type_text)
        markdown_parser = MarkdownParser(node)
        markdown_parser.split_nodes_delimiter(markdown_bold_delimiter, text_type_bold)
        markdown_parser.split_nodes_delimiter(markdown_italic_delimiter, text_type_italic)

        expected_italic = [
            TextNode("This is text with a ", text_type_text),
            TextNode("italic block", text_type_italic),
            TextNode(" and ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" word", text_type_text),
        ]
        self.assertListEqual(expected_italic, markdown_parser.nodes)

    def test_split_nodes_delimiter_italic_before_bold(self):
        node = TextNode("This is text with a *italic block* and **bold** word", text_type_text)
        markdown_parser = MarkdownParser(node)
        with self.assertRaises(ValueError) as cm:
            markdown_parser.split_nodes_delimiter(markdown_italic_delimiter, text_type_italic)

        self.assertEqual(str(cm.exception), "Cannot process italic before processing bold")

    def test_split_nodes_delimiter_no_del_in_text(self):
        node = TextNode("This is text with a *italic block* and **bold** word", text_type_text)
        markdown_parser = MarkdownParser(node)

        markdown_parser.split_nodes_delimiter(markdown_code_delimiter, text_type_code)
        self.assertListEqual([node], markdown_parser.nodes)

    def test_split_nodes_delimiter_missing_matching_delimiter(self):
        node = TextNode("This is text with a `code block without a matching delimiter", text_type_text)
        markdown_parser = MarkdownParser(node)

        with self.assertRaises(ValueError) as cm:
            markdown_parser.split_nodes_delimiter(markdown_code_delimiter, text_type_code)
        self.assertEqual(str(cm.exception), f"Tag {markdown_code_delimiter} is not closed")

    def test_split_nodes_images(self):
        node = TextNode(
                "This is text with an ![image](https://storage.googleapis.com/"
                + "qvault-webapp-dynamic-assets/course_assets/zzjjcJKZ.png) and another"
                + " ![second image](https://storage.googleapis.com/qvault-webapp-"
                + "dynamic-assets/course_assets/3elNhQu.png)",
                text_type_text)
        markdown_parser = MarkdownParser(node)
        markdown_parser.split_nodes_image()

        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zzjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
            ),
        ]
        self.assertListEqual(expected, markdown_parser.nodes)

    def test_split_nodes_links(self):
        node = TextNode(
                "This is text with a [link](https://www.abc.com) and another"
                + " [second link](https://www.google.com)",
                text_type_text)
        markdown_parser = MarkdownParser(node)
        markdown_parser.split_nodes_link()

        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("link", text_type_link, "https://www.abc.com"),
            TextNode(" and another ", text_type_text),
            TextNode("second link", text_type_link, "https://www.google.com"
            ),
        ]
        self.assertListEqual(expected, markdown_parser.nodes)

    def test_text_to_textnodes(self):
        node = TextNode(
            "This is **text** with an *italic* word and a `code block` and an"
            + " ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets"
            + "/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)",
            text_type_text
        )
        markdown_parser = MarkdownParser(node)
        new_nodes = markdown_parser.text_to_textnodes()

        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        self.assertListEqual(new_nodes, expected)
