from textnode import TextNode
from textnode import text_type_italic
import re

class MarkdownParser:
    def split_nodes_delimiter(self, old_nodes, delimiter, text_type):
        new_nodes = []
        for node in old_nodes:
            new_nodes.extend(self.get_inner_nodes(node, delimiter, text_type))

        return new_nodes

    def get_inner_nodes(self, node, delimiter, text_type):
        if text_type == text_type_italic and markdown_bold_delimiter in node.text:
            raise ValueError("Cannot process italic before processing bold")
        blocks = node.text.split(delimiter)
        if len(blocks) % 2 == 0:
            raise ValueError(
                f'Tag {delimiter} is not closed')

        for i, block in enumerate(blocks):
            if i % 2 == 1:
                yield TextNode(block, text_type)
            else:
                yield TextNode(block, node.text_type)

    def extract_markdown_images(self, text):
        image_pattern = r"!\[(.*?)\]\((.*?)\)"
        return re.findall(image_pattern, text)

markdown_code_delimiter = '`'
markdown_bold_delimiter = '**'
markdown_italic_delimiter = '*'
