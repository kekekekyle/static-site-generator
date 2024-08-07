class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html is not implemented")

    def props_to_html(self):
        if self.props:
            html_string = list(map(lambda x: f' {x[0]}="{x[1]}"', self.props.items()))
            return "".join(html_string)
        return None

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("value is None")
        if self.tag is None:
            return self.value

        return f"<{self.tag}{super().props_to_html() or ''}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is None")
        if self.children is None:
            raise ValueError("ParentNode has no children!")

        return f"<{self.tag}{super().props_to_html() or ''}>{''.join(list(map(lambda x: x.to_html(), self.children)))}</{self.tag}>"

