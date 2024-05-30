import unittest
from markdownblockparser import (
    MarkdownBlockParser,
    block_type_code,
    block_type_heading,
    block_type_ordered_list,
    block_type_paragraph,
    block_type_quote,
    block_type_unordered_list
)

class TestMarkdownBlockParser(unittest.TestCase):
    def test_markdown_to_blocks(self):
        raw_markdown = (
            'This is **bolded** paragraph\n\n'
            + 'This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n\n'
            + '* This is a list\n* with items')
        parser = MarkdownBlockParser(raw_markdown)
        parser.markdown_to_blocks()

        expected = [
            { 'content': "This is **bolded** paragraph" },
            { 'content': "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line" },
            { 'content': "* This is a list\n* with items" }
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
            { 'content': 'This is a paragraph\nand its continuation' },

            { 'content': 'Another paragraph, but with\nextra\nspace' }
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
            { 'content': 'This is a paragraph\nthat continues with a bunch of new lines' },
            { 'content': 'New lines are really fun!' },
            { 'content': 'Enough!' }
        ]
        self.assertListEqual(expected, parser.blocks)

    def test_markdown_to_block_type_paragraph(self):
        raw_markdown = (
            'This is a paragraph\n\n'

            + 'And another paragraph\n\n'

            + 'Nothing special about any of us'
        )
        parser = MarkdownBlockParser(raw_markdown)
        parser.markdown_to_blocks()
        parser.blocks_to_block_type()

        expected = [
            block_type_paragraph,
            block_type_paragraph,
            block_type_paragraph
        ]
        self.assertListEqual(expected, list(map(lambda x: x['type'], parser.blocks)))