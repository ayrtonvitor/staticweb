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
                self.blocks.append(curr.strip())
                curr = ""
        self.blocks.append(curr.strip())
