from htmlnode import LeafNode, ParentNode
from inlinemarkdownparser import InlineMarkDownParser
from markdownblockparser import (
    MarkdownBlockParser,
    block_type_code,
    block_type_heading,
    block_type_ordered_list,
    block_type_paragraph,
    block_type_quote,
    block_type_unordered_list,
)
from textnode import TextNode, text_type_text


class MarkdownToHtml:
    def md_paragraph_to_p(self, block):
        inline_md_parser = InlineMarkDownParser(TextNode(block['content'], text_type_text))

        text_nodes = inline_md_parser.text_to_textnodes()
        leaf_nodes = [node.text_node_to_html_node() for node in text_nodes]

        return ParentNode(tag='p', children=leaf_nodes)

    def md_header_to_h(self, block):
        return LeafNode(tag=f"h{block['level']}", value=block['content'])

    def md_code_to_pre_code(self, block):
        code = LeafNode(tag='code', value=block['content'])
        return ParentNode(tag='pre', children = [code])

    def md_quote_to_blockquote(self, block):
        quote = LeafNode(tag='p', value=block['content'])
        return ParentNode(tag='blockquote', children=[quote])

    def md_unordered_list_to_ul(self, block):
        list_items = [LeafNode(tag='li', value=cont) for cont in block['content'].split('\n')]
        return ParentNode(tag='ul', children=list_items)

    def md_ordered_list_to_ol(self, block):
        list_items = [LeafNode(tag='li', value=cont) for cont in block['items']]
        return ParentNode(tag='ol', children=list_items)

    def markdown_to_html_node(self, md_block):
        md_block_type_to_converter = {
            block_type_paragraph: self.md_paragraph_to_p,
            block_type_heading: self.md_header_to_h,
            block_type_code: self.md_code_to_pre_code,
            block_type_quote: self.md_quote_to_blockquote,
            block_type_unordered_list: self.md_unordered_list_to_ul,
            block_type_ordered_list: self.md_ordered_list_to_ol
        }
        return ParentNode(tag='div', children=[md_block_type_to_converter[md_block['type']](md_block)])

    def markdown_to_html(self, markdown_text):
        block_parser = MarkdownBlockParser(markdown_text)
        block_parser.markdown_to_blocks()
        block_parser.process_block_type()

        final_html = ""
        for block in block_parser.blocks:
            final_html += self.markdown_to_html_node(block).to_html()

        return final_html
