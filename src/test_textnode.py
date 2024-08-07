import unittest

from textnode import TextNode, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_diff(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is another text node", "italic")
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node", "bold", "localhost")
        node2 = TextNode("This is a text node", "bold", "localhost")
        self.assertEqual(node, node2)

class TestTextToHTMLNode(unittest.TestCase):
    def test_text(self):
        text_node = TextNode("hello", "text")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "hello")

    def test_bold(self):
        text_node = TextNode("hello", "bold")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<b>hello</b>")

    def test_italic(self):
        text_node = TextNode("hello", "italic")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<i>hello</i>")

    def test_code(self):
        text_node = TextNode("hello", "code")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<code>hello</code>")

    def test_link(self):
        text_node = TextNode("hello", "link", "www.google.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<a href="www.google.com">hello</a>')

    def test_image(self):
        text_node = TextNode("hello", "image", "www.google.com/logo.png")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<img src="www.google.com/logo.png" alt="hello"></img>')

if __name__ == "__main__":
    unittest.main()
