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
        markdown_parser = MarkdownParser()
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = markdown_parser.split_nodes_delimiter([node], markdown_code_delimiter, text_type_code)

        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]
        self.assertListEqual(new_nodes, expected)


    def test_split_nodes_delimiter_bold(self):
        markdown_parser = MarkdownParser()
        node = TextNode("This is text with a **bold block** word", text_type_text)
        new_nodes = markdown_parser.split_nodes_delimiter([node], markdown_bold_delimiter, text_type_bold)

        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("bold block", text_type_bold),
            TextNode(" word", text_type_text),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_delimiter_italic(self):
        markdown_parser = MarkdownParser()
        node = TextNode("This is text with a *italic block* word", text_type_text)
        new_nodes = markdown_parser.split_nodes_delimiter([node], markdown_italic_delimiter, text_type_italic)

        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("italic block", text_type_italic),
            TextNode(" word", text_type_text),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_delimiter_italic_and_bold(self):
        markdown_parser = MarkdownParser()
        node = TextNode("This is text with a *italic block* and **bold** word", text_type_text)
        bold_nodes = markdown_parser.split_nodes_delimiter([node], markdown_bold_delimiter, text_type_bold)

        expected_bold = [
            TextNode("This is text with a *italic block* and ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" word", text_type_text),
        ]
        self.assertListEqual(bold_nodes, expected_bold)

    def test_split_nodes_delimiter_italic_after_bold(self):
        markdown_parser = MarkdownParser()
        node = TextNode("This is text with a *italic block* and **bold** word", text_type_text)
        bold_nodes = markdown_parser.split_nodes_delimiter([node], markdown_bold_delimiter, text_type_bold)
        italic_nodes = markdown_parser.split_nodes_delimiter(bold_nodes, markdown_italic_delimiter, text_type_italic)

        expected_italic = [
            TextNode("This is text with a ", text_type_text),
            TextNode("italic block", text_type_italic),
            TextNode(" and ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" word", text_type_text),
        ]
        self.assertListEqual(expected_italic, italic_nodes)

    def test_split_nodes_delimiter_italic_before_bold(self):
        markdown_parser = MarkdownParser()
        node = TextNode("This is text with a *italic block* and **bold** word", text_type_text)
        with self.assertRaises(ValueError) as cm:
            markdown_parser.split_nodes_delimiter([node], markdown_italic_delimiter, text_type_italic)

        self.assertEqual(str(cm.exception), "Cannot process italic before processing bold")

    def test_split_nodes_delimiter_no_del_in_text(self):
        markdown_parser = MarkdownParser()
        node = TextNode("This is text with a *italic block* and **bold** word", text_type_text)

        result = markdown_parser.split_nodes_delimiter([node], markdown_code_delimiter, text_type_code)
        self.assertListEqual([node], result)

    def test_split_nodes_delimiter_missing_matching_delimiter(self):
        markdown_parser = MarkdownParser()
        node = TextNode("This is text with a `code block without a matching delimiter", text_type_text)

        with self.assertRaises(ValueError) as cm:
            markdown_parser.split_nodes_delimiter([node], markdown_code_delimiter, text_type_code)
        self.assertEqual(str(cm.exception), f"Tag {markdown_code_delimiter} is not closed")
