import unittest

from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    extract_title,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_olist,
    block_type_ulist,
    block_type_quote,
)

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """
            # This is a heading

            This is a paragraph of text. It has some **bold** and *italic* words inside of it.



            * This is the first list item in a list block
            * This is a list item
            * This is another list item

        """
        self.assertEqual(markdown_to_blocks(markdown),
            [
                '# This is a heading', 
                'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
                '* This is the first list item in a list block\n* This is a list item\n* This is another list item'
            ]
        )

    def test_markdown_to_blocks_again(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_block_type(self):
        md = """###### heading 6"""
        self.assertEqual(
            block_to_block_type(md),
            "heading",
        )

        md = """###### heading 5"""
        self.assertEqual(
            block_to_block_type(md),
            "heading",
        )

        md = """##### heading 4"""
        self.assertEqual(
            block_to_block_type(md),
            "heading",
        )

        md = """#### heading 3"""
        self.assertEqual(
            block_to_block_type(md),
            "heading",
        )

        md = """## heading 2"""
        self.assertEqual(
            block_to_block_type(md),
            "heading",
        )

        md = """# heading 1"""
        self.assertEqual(
            block_to_block_type(md),
            "heading",
        )

        md = """```this is a code block```"""
        self.assertEqual(
            block_to_block_type(md),
            "code",
        )

        md = """> quote 1
> quote 2"""
        self.assertEqual(
            block_to_block_type(md),
            "quote",
        )

        md = """* unordered list 1
* unordered list 2"""
        self.assertEqual(
            block_to_block_type(md),
            "unordered_list",
        )

        md = """- unordered list 1
- unordered list 2"""
        self.assertEqual(
            block_to_block_type(md),
            "unordered_list",
        )

        md = """1. ordered list 1
2. ordered list 2"""
        self.assertEqual(
            block_to_block_type(md),
            "ordered_list",
        )

        md = """1. ordered list 1
2. ordered list 2
4. paragraph"""
        self.assertEqual(
            block_to_block_type(md),
            "paragraph",
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), block_type_ulist)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), block_type_olist)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_extract_title(self):
        md = """
# This has a title

blah 
"""
        self.assertEqual(
            extract_title(md),
            "This has a title"
        )

    def test_extract_no_title(self):
        md = """
## This has a title

### no title in here! 
"""
        with self.assertRaises(Exception) as e:
            extract_title(md)
        self.assertEqual(str(e.exception), "No h1 header found!")

if __name__ == "__main__":
    unittest.main()
