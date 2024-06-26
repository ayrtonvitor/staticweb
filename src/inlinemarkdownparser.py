from textnode import (
    TextNode,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    text_type_text
)
import re

class InlineMarkDownParser:
    def __init__(self, node):
        self.nodes = [node]

    def split_nodes_delimiter(self, delimiter, text_type):
        new_nodes = []
        for node in self.nodes:
            if node.text_type in (text_type_code, text_type_link, text_type_image):
                new_nodes.append(node)
            else:
                new_nodes.extend(self.get_inner_nodes(node, delimiter, text_type))

        self.nodes = new_nodes

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

    def split_nodes_long_pattern(self, text_type):
        new_nodes = []
        for node in self.nodes:
            if node.text_type != text_type_text:
                new_nodes.append(node)
            else:
                new_nodes.extend(
                    self.get_inner_nodes_single_delimeter(node, text_type))
        self.nodes = new_nodes

    def split_nodes_link(self):
        self.split_nodes_long_pattern(text_type_link)

    def split_nodes_image(self):
        self.split_nodes_long_pattern( text_type_image)

    def get_inner_nodes_single_delimeter(self, node, text_type):
        matches = self._get_matches(text_type, node.text)

        to_split = node.text
        for body, ref in matches:
            delimiter = self._get_delimiter(body, ref, text_type)
            split = to_split.split(delimiter, 1)

            yield TextNode(split[0], text_type_text)
            yield TextNode(body, text_type, ref)

            to_split = split[1] if len(split) > 1 else ''

        if to_split:
            yield TextNode(to_split, text_type_text)

    def text_to_textnodes(self):
        self.split_nodes_image()
        self.split_nodes_link()
        self.split_nodes_delimiter(markdown_bold_delimiter, text_type_bold)
        self.split_nodes_delimiter(markdown_code_delimiter, text_type_code)
        self.split_nodes_delimiter(markdown_italic_delimiter, text_type_italic)
        return self.nodes

    def _get_delimiter(self, body, ref, text_type):
        if text_type == text_type_image:
            return self._as_image(body, ref)
        if text_type == text_type_link:
            return self._as_link(body, ref)


    def _get_matches(self, text_type, text):
        image_pattern = r"!\[(.*?)\]\((.*?)\)"
        link_pattern = r"\[(.*?)\]\((.*?)\)"
        pattern = image_pattern if text_type == text_type_image else link_pattern
        return re.findall(pattern, text)

    def _as_image(self, body, ref):
        return f'![{body}]({ref})'

    def _as_link(self, body, ref):
        return f'[{body}]({ref})'

markdown_code_delimiter = '`'
markdown_bold_delimiter = '**'
markdown_italic_delimiter = '*'
