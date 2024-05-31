import re

class MarkdownBlockParser:
    '''
    This largely assumes that the markdown is well formated
    and does not make too much effort in trying to correct problems
    so there is no guarantee that this parser handles well cases
    like simple new lines after special blocks
    '''
    def __init__(self, raw_markdown):
        self.raw_markdown = self.pre_process_md(raw_markdown)
        self.blocks = []

    def pre_process_md(self, raw_markdown):
        raw_markdown = '\n' + raw_markdown + '\n'

        special_patterns = r'(\n(?:```|#{1,6} ).*?)\n'
        replacement = r'\n\1\n\n'
        raw_markdown = re.sub(special_patterns, replacement, raw_markdown)

        tokens = ['*', '-', '>', r'[1-9]\.']
        for token in tokens:
            special_patterns = rf'(\n(?:{token} ).*?\n)(?!\* )'
        raw_markdown = re.sub(special_patterns, replacement, raw_markdown)

        return raw_markdown

    def markdown_to_blocks(self):
        for block in self.raw_markdown.split('\n\n'):
            curr = ""
            for line in block.split('\n'):
                line = line.rstrip().lstrip('\n')
                if line:
                    if re.match(r'^(?:\t| {4})\w+', line) is None:
                        line = line.lstrip()
                    curr += line + '\n'
            if curr:
                self.blocks.append({ 'content': curr[:-1] })

    def blocks_to_block_type(self):
        for block in self.blocks:
            self.set_block_type_from_content(block)

    def set_block_type_from_content(self, block):
        if self.is_heading(block):
            block['type'] = block_type_heading
        else:
            block['type'] = block_type_paragraph

    def is_heading(self, block):
        heading_pattern = r'^#{1,6} \S.*'
        return re.match(heading_pattern, block['content']) is not None

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"
