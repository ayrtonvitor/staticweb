class MarkdownBlockParser:
    def __init__(self, raw_markdown):
        self.raw_markdown = raw_markdown
        self.blocks = []

    def markdown_to_blocks(self):
        curr = ""
        for par in self.raw_markdown.split('\n'):
            if par:
                curr += par.strip() + '\n'
            elif curr:
                self.blocks.append({ 'content': curr.strip() })
                curr = ""
        self.blocks.append({ 'content': curr.strip() })

    def blocks_to_block_type(self):
        for block in self.blocks:
            self.set_block_type_from_content(block)

    def set_block_type_from_content(self, block):
        block['type'] = block_type_paragraph

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"
