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

    def test_markdown_to_blocks_new_line_ending(self):
        raw_markdown = "This md ends with new lines\n\n\n"
        parser = MarkdownBlockParser(raw_markdown)
        parser.markdown_to_blocks()

        expected = [ { 'content' : 'This md ends with new lines' } ]

        self.assertListEqual(expected, parser.blocks)

        raw_markdown += '\n'
        parser = MarkdownBlockParser(raw_markdown)
        parser.markdown_to_blocks()
        self.assertListEqual(expected, parser.blocks)

    def test_markdown_to_blocks_removes_leading_and_trailing_whitespaces(self):
        raw_markdown = (
            'This is a paragraph\n'
            + 'and its continuation\n\n'

            + 'Another paragraph, but with\n'
            + '   extra\n'
            + 'space  \n\n'
            + '\tTABs and 4 spaces are tolerated at the beginning\n'
            + '    because the block can be code, so we need indentation\n\n'
            + '\nBut not new lines or other spaces\n'
        )
        parser = MarkdownBlockParser(raw_markdown)
        parser.markdown_to_blocks()

        expected = [
            { 'content': 'This is a paragraph\nand its continuation' },

            { 'content': 'Another paragraph, but with\nextra\nspace' },

            { 'content': '\tTABs and 4 spaces are tolerated at the beginning\n' \
                        '    because the block can be code, so we need indentation' },
            { 'content': 'But not new lines or other spaces' }
        ]
        self.assertListEqual(expected, parser.blocks)

    def test_markdown_to_blocks_removes_excessive_new_lines(self):
        raw_markdown = (
            'This is a paragraph\n'
            + 'that continues with a bunch of new lines\n\n\n\n'

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
        parser.process_block_type()

        expected = [
            { 'content': 'This is a paragraph', 'type': block_type_paragraph },
            { 'content': 'And another paragraph', 'type': block_type_paragraph },
            { 'content': 'Nothing special about any of us', 'type': block_type_paragraph },
        ]
        self.assertListEqual(expected, parser.blocks)

    def test_markdown_to_block_type_heading(self):
        raw_markdown = (
            '# This is a heading 1\n\n'
            + '## This is a heading 2\n\n'
            + '### This is a heading 3\n\n'
            + '#### This is a heading 4\n\n'
            + '##### This is a heading 5\n\n'
            + '###### This is a heading 6'
        )
        parser = MarkdownBlockParser(raw_markdown)
        parser.markdown_to_blocks()
        parser.process_block_type()

        expected = [
            { 'content': 'This is a heading 1', 'type': block_type_heading, 'level': '1' },
            { 'content': 'This is a heading 2', 'type': block_type_heading, 'level': '2' },
            { 'content': 'This is a heading 3', 'type': block_type_heading, 'level': '3' },
            { 'content': 'This is a heading 4', 'type': block_type_heading, 'level': '4' },
            { 'content': 'This is a heading 5', 'type': block_type_heading, 'level': '5' },
            { 'content': 'This is a heading 6', 'type': block_type_heading, 'level': '6' },
        ]
        self.assertListEqual(expected, parser.blocks)

    def test_markdown_to_block_type_heading_simple_new_line(self):
        raw_markdown = (
            '# This is a heading 1\n'
            + '## This is a heading 2\n'
            + '### This is a heading 3\n'
            + '#### This is a heading 4\n'
            + '##### This is a heading 5\n'
            + '###### This is a heading 6'
        )
        parser = MarkdownBlockParser(raw_markdown)
        parser.markdown_to_blocks()
        parser.process_block_type()

        expected = [
            { 'content': 'This is a heading 1', 'type': block_type_heading, 'level': '1' },
            { 'content': 'This is a heading 2', 'type': block_type_heading, 'level': '2' },
            { 'content': 'This is a heading 3', 'type': block_type_heading, 'level': '3' },
            { 'content': 'This is a heading 4', 'type': block_type_heading, 'level': '4' },
            { 'content': 'This is a heading 5', 'type': block_type_heading, 'level': '5' },
            { 'content': 'This is a heading 6', 'type': block_type_heading, 'level': '6' },
        ]
        self.assertListEqual(expected, parser.blocks)

    def test_markdown_to_block_type_heading_and_paragraphs(self):
        raw_markdown = (
            '# This is a heading 1\n'
            + 'This is a paragraph with a simple new line\n'
            + '## This is a heading 2\n'
            + 'Another paragraph\n'
            + '### This is a heading 3\n\n'
            + '#### This is a heading 4\n'
            + 'And this is a paragraph with two new lines\n\n'
            + '##### This is a heading 5\n'
            + '###### This is a heading 6\n\n'
        )
        parser = MarkdownBlockParser(raw_markdown)
        parser.markdown_to_blocks()
        parser.process_block_type()

        expected = [
            { 'content': 'This is a heading 1', 'type': block_type_heading, 'level': '1' },
            { 'content': 'This is a paragraph with a simple new line', 'type': block_type_paragraph },
            { 'content': 'This is a heading 2', 'type': block_type_heading, 'level': '2' },
            { 'content': 'Another paragraph', 'type': block_type_paragraph },
            { 'content': 'This is a heading 3', 'type': block_type_heading, 'level': '3' },
            { 'content': 'This is a heading 4', 'type': block_type_heading, 'level': '4' },
            { 'content': 'And this is a paragraph with two new lines', 'type': block_type_paragraph },
            { 'content': 'This is a heading 5', 'type': block_type_heading, 'level': '5' },
            { 'content': 'This is a heading 6', 'type': block_type_heading, 'level': '6' },
        ]
        self.assertListEqual(expected, parser.blocks)

    def test_markdown_to_block_type_code(self):
        raw_markdown = '```This is a code block```'
        parser = MarkdownBlockParser(raw_markdown)
        parser.markdown_to_blocks()
        parser.process_block_type()

        expected = [
            { 'content': 'This is a code block', 'type': block_type_code },
        ]
        self.assertListEqual(expected, parser.blocks)

    def test_markdown_to_block_type_code_enclosed_simple_new_line(self):
        raw_markdown = (
            '# Something previously\n'
            + '```This is a code block```\n'
            + 'But this is not'
        )
        parser = MarkdownBlockParser(raw_markdown)
        parser.markdown_to_blocks()
        parser.process_block_type()

        expected = [
            { 'content': 'Something previously', 'type': block_type_heading, 'level': "1" },
            { 'content': 'This is a code block', 'type': block_type_code },
            { 'content': 'But this is not', 'type': block_type_paragraph }
        ]
        self.assertListEqual(expected, parser.blocks)

    def test_markdown_to_block_type_code_open_block(self):
        raw_markdown = '```This is a proper code block```\n\n```this code block is not closed.\n\n Raise error``'
        parser = MarkdownBlockParser(raw_markdown)
        parser.markdown_to_blocks()

        with self.assertRaises(ValueError) as cm:
            parser.process_block_type()
        self.assertEqual(str(cm.exception), 'Could not find proper closing of code block')

    def test_markdown_to_block_type_code_inner_blank_line(self):
        raw_markdown = '```this is a code block with\n\nempty lines inside\n\n\nends here```'
        parser = MarkdownBlockParser(raw_markdown)
        parser.markdown_to_blocks()
        parser.process_block_type()
        expected = [ { 'content': 'this is a code block with\n\nempty lines inside\n\n\nends here',
                      'type': block_type_code } ]

        self.assertListEqual(expected, parser.blocks)

    def test_markdown_to_block_type_code_new_line_after_token(self):
        raw_markdown = '```\nthis is a code block with\n\nempty lines inside\n\n\nends here\n```'
        parser = MarkdownBlockParser(raw_markdown)
        parser.markdown_to_blocks()
        parser.process_block_type()
        expected = [ { 'content': 'this is a code block with\n\nempty lines inside\n\n\nends here',
                      'type': block_type_code } ]

        self.assertListEqual(expected, parser.blocks)

    def test_markdown_to_block_type_unordered_list(self):
        raw_markdown = ('This is a paragraph\n\n'
            + '* followed by an unordered list\n\n'
            + 'Then another paragraph\n'
            + '* Then another list\n'
            + '# Leading to a header\n'
            + '* followed by a \n'
            + '*  multi line list\n\n'
            + '* and another one')
        parser = MarkdownBlockParser(raw_markdown)
        parser.markdown_to_blocks()
        parser.process_block_type()

        expected = [
            { 'content': 'This is a paragraph', 'type': block_type_paragraph },
            { 'content': 'followed by an unordered list', 'type': block_type_unordered_list },
            { 'content': 'Then another paragraph', 'type': block_type_paragraph },
            { 'content': 'Then another list', 'type': block_type_unordered_list},
            { 'content': 'Leading to a header', 'type': block_type_heading, 'level': "1" },
            { 'content': 'followed by a\n multi line list', 'type': block_type_unordered_list },
            { 'content': 'and another one', 'type': block_type_unordered_list },
        ]
        self.assertListEqual(expected, parser.blocks)

    def test_markdown_to_block_type_ordered_list(self):
        raw_markdown = ('This is a paragraph\n\n'
            + '1. followed by an ordered list\n\n'
            + 'Then another paragraph\n'
            + '1. Then another list\n'
            + '# Leading to a header\n'
            + '1. followed by a \n'
            + '2.  multi line list\n\n'
            + '1. and another one\n'
            + '2. and another two\n'
            + '3. and another three\n'
            + '4. and another four\n'
            + '5. and another five\n'
        )
        parser = MarkdownBlockParser(raw_markdown)
        parser.markdown_to_blocks()
        parser.process_block_type()

        expected = [
            { 'content': 'This is a paragraph', 'type': block_type_paragraph },
            {
                'content': '1. followed by an ordered list',
                'type': block_type_ordered_list,
                'items': [ 'followed by an ordered list' ]
            },
            { 'content': 'Then another paragraph', 'type': block_type_paragraph },
            {
                'content': '1. Then another list',
                'type': block_type_ordered_list,
                'items': [ 'Then another list' ]
            },
            { 'content': 'Leading to a header', 'type': block_type_heading, 'level': "1" },
            {
                'content': '1. followed by a\n2.  multi line list',
                'type': block_type_ordered_list,
                'items': [ 'followed by a', ' multi line list' ]
            },
            {
                'content': ('1. and another one\n2. and another two\n'
                    + '3. and another three\n4. and another four\n'
                    + '5. and another five'),
                'type': block_type_ordered_list,
                'items': [
                    'and another one',
                    'and another two',
                    'and another three',
                    'and another four',
                    'and another five'
                ]
            },
        ]
        self.assertListEqual(expected, parser.blocks)

    def test_markdown_to_block_type_quote(self):
        raw_markdown = ('This is a paragraph\n\n'
            + '> followed by a quote\n\n'
            + 'Then another paragraph\n'
            + '> Then another quote\n'
            + '# Leading to a header\n'
            + '> followed by a \n'
            + '>  multi line quote\n\n'
            + '> and another one')
        parser = MarkdownBlockParser(raw_markdown)
        parser.markdown_to_blocks()
        parser.process_block_type()

        expected = [
            { 'content': 'This is a paragraph', 'type': block_type_paragraph },
            { 'content': 'followed by a quote', 'type': block_type_quote },
            { 'content': 'Then another paragraph', 'type': block_type_paragraph },
            { 'content': 'Then another quote', 'type': block_type_quote},
            { 'content': 'Leading to a header', 'type': block_type_heading, 'level': '1' },
            { 'content': 'followed by a\n multi line quote', 'type': block_type_quote },
            { 'content': 'and another one', 'type': block_type_quote },
        ]
        self.assertListEqual(expected, parser.blocks)

    def test_markdown_to_block_type_broken_ordered_list(self):
        raw_markdown = "1. list 1\n2. list 2\n5. list 5"
        parser = MarkdownBlockParser(raw_markdown)
        parser.markdown_to_blocks()

        with self.assertRaises(ValueError) as cm:
            parser.process_block_type()
        self.assertEqual(str(cm.exception), 'Ordered list not in order')
