import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_to_html_props_none(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
        )
        self.assertEqual(
            node.props_to_html(),
            None,
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

class TestLeafNode(unittest.TestCase):
    def test_values(self):
        node = LeafNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_to_html_text(self):
        node = LeafNode(
            None,
            "Hello, world!",
        )
        self.assertEqual(
            node.to_html(),
            "Hello, world!",
        )

    def test_to_html_no_props(self):
        node = LeafNode(
            "div",
            "Hello, world!",
        )
        self.assertEqual(
            node.to_html(),
            "<div>Hello, world!</div>",
        )

    def test_to_html_props(self):
        node = LeafNode(
            "a",
            "Click me!",
            { "href": "https://www.google.com" },
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

class TestParentNode(unittest.TestCase):
    def test_to_html_nested_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode("p", [
                    ParentNode("div", [
                        LeafNode(None, "Deep nested child"),
                        LeafNode("i", "Deep italic child"),
                    ]),
                    LeafNode(None, "Nested child")
                ]),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b><p><div>Deep nested child<i>Deep italic child</i></div>Nested child</p><i>italic text</i>Normal text</p>"
        )

    def test_to_html_no_children(self):
        node = ParentNode(
            "p",
            [],
        )
        self.assertEqual(
            node.to_html(),
            "<p></p>"
        )

    def test_to_html_flat(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

if __name__ == "__main__":
    unittest.main()
