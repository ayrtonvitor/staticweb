import unittest
from markdownblockparser import MarkdownBlockParser

class TestMarkdownBlockParser(unittest.TestCase):
    def test_markdown_to_blocks(self):
        raw_markdown = (
            'This is **bolded** paragraph\n\n'
            + 'This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n\n'
            + '* This is a list\n* with items')
        parser = MarkdownBlockParser(raw_markdown)
        parser.markdown_to_blocks()

        expected = [
            "This is **bolded** paragraph",

            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",

            "* This is a list\n* with items"
        ]

        self.assertListEqual(expected, parser.blocks)
