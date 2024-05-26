class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        html = ""
        for prop, val in self.props.items():
            html += f' {prop}="{val}"'
        return html

    def __repr__(self):
        return f' HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        self.tag = tag
        self.value = value
        self.props = props
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        self.tag = tag
        self.children = children
        self.props = props
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent node requires a tag")
        if not self.children:
            raise ValueError(
                """No children provided
                   A node with no children is a leaf node""")

        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        return f'<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>'
