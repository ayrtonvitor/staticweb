import re

class MarkdownBlockParser:

    def __init__(self, raw_markdown):
        self.raw_markdown = raw_markdown
        self.blocks = []

    def markdown_to_blocks(self):
        curr = ""
        for line in self.raw_markdown.split('\n'):
            line, curr = self.add_to_blocks_list_if_heading(line, curr)
            if line:
                curr += line.strip() + '\n'
            elif curr:
                self.add_to_blocks_list(curr)
                curr = ""
        if re.search(r'\S', curr) is not None:
            self.add_to_blocks_list(curr)

    def add_to_blocks_list(self, line):
        self.blocks.append({ 'content': line.strip() })

    def add_to_blocks_list_if_heading(self, line, curr):
        if self.is_heading({ 'content': line.strip() }):
            if re.search(r'\S', curr) is not None:
                self.add_to_blocks_list(curr)
                curr = ""
            self.add_to_blocks_list(line)
            line = ""
        return line, curr

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
