from htmlnode import LeafNode

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        self.setup_html_conversor()

    def __eq__(self, other):
        return (self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url)

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'

    def text_node_to_html_node(self):
        if not self.text_type:
            raise ValueError("A text node must have a text type")
        if not self.text_type in self.html_node_conversor_by_text_type:
            raise ValueError(f"Text type {self.text_type} is not supported")
        return self.html_node_conversor_by_text_type[self.text_type]()

    def setup_html_conversor(self):
        self.html_node_conversor_by_text_type = {
            text_type_text: self.to_text_html,
            text_type_bold: self.to_bold_html,
            text_type_italic: self.to_italic_html,
            text_type_code: self.to_code_html,
            text_type_image: self.to_image_html,
            text_type_link: self.to_link_html,
        }

    def to_text_html(self):
        return LeafNode(None, self.text)

    def to_bold_html(self):
        return LeafNode('b', self.text)

    def to_italic_html(self):
        return LeafNode('i', self.text)

    def to_code_html(self):
        return LeafNode('code', self.text)

    def to_image_html(self):
        return LeafNode('img', '', {'src': self.url, 'alt': self.text})

    def to_link_html(self):
        return LeafNode('a', self.text, {'href': self.url})


text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_image = "image"
text_type_link = "link"
