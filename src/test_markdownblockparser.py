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

    def test_markdown_to_blocks_removes_leading_and_trailing_whitespaces(self):
        raw_markdown = (
            'This is a paragraph\n'
            + 'and its continuation\n\n'

            + '\tAnother paragraph, but with\n'
            + '   extra\n'
            + 'space  '
        )
        parser = MarkdownBlockParser(raw_markdown)
        parser.markdown_to_blocks()

        expected = [
            'This is a paragraph\n'
            + 'and its continuation',

            'Another paragraph, but with\n'
            + 'extra\n'
            + 'space'
        ]
        self.assertListEqual(expected, parser.blocks)

    def test_markdown_to_blocks_removes_excessive_new_lines(self):
        raw_markdown = (
            'This is a paragraph\n'
            + 'that continues with a bunch of new lines\n\n\n\n\n'

            + 'New lines are really fun!\n\n\n'

            + 'Enough!'
        )
        parser = MarkdownBlockParser(raw_markdown)
        parser.markdown_to_blocks()

        expected = [
            'This is a paragraph\n'
            + 'that continues with a bunch of new lines',

            'New lines are really fun!',

            'Enough!'
        ]
        self.assertListEqual(expected, parser.blocks)
