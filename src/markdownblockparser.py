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

    def process_block_type(self):
        processed = []
        curr = {}
        for block in self.blocks:
            block_type = curr['type'] if curr else self.get_block_processing_type(block)
            block['type'] = block_type

            if block_type == block_type_code:
                self.process_code_block(curr, block, processed)
            else:
                processed.append(block)

        self.blocks = processed

    def process_code_block(self, curr, new, processed):
        curr['content'] = curr.get('content', '') + new['content']
        if 'type' not in curr:
            curr['type'] = new['type']
        if self.block_ends_code(curr):
            if len(curr['content']) < 6:
                raise ValueError("Could not find proper closing of the code block")
            curr['content'] = curr['content'][3:-3]
            processed.append(curr.copy())
            curr.clear()

    def get_block_processing_type(self, block):
        if self.is_heading(block):
            return block_type_heading
        elif self.block_starts_code(block):
            return block_type_code
        else:
            return block_type_paragraph

    def is_heading(self, block):
        heading_pattern = r'^#{1,6} \S.*'
        return re.match(heading_pattern, block['content']) is not None

    def block_starts_code(self, block):
        return block['content'][:3] == '```'

    def block_ends_code(self, block):
        return block['content'][-3:] == '```'

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"
