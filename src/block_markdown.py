from inline_markdown import (
    split_nodes_delimiter, 
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)

from textnode import TextNode, text_node_to_html_node
from htmlnode import LeafNode, ParentNode

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

def markdown_to_blocks(markdown):
    lines = markdown.split("\n")
    blocks = []
    curr_block = []
    for line in lines:
        if line.strip() == "":
            if len(curr_block) > 0:
                blocks.append("\n".join(curr_block))
            curr_block = []
        else:
            curr_block.append(line.strip())
    if len(curr_block) > 0:
        blocks.append("\n".join(curr_block))

    return blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith("###### "):
        return block_type_heading
    if block.startswith("##### "):
        return block_type_heading
    if block.startswith("#### "):
        return block_type_heading
    if block.startswith("### "):
        return block_type_heading
    if block.startswith("## "):
        return block_type_heading
    if block.startswith("# "):
        return block_type_heading
    if block.startswith("```") and block.endswith("```"):
        return block_type_code
    if all(list(map(lambda x: x.startswith(">"), lines))):
        return block_type_quote
    if all(list(map(lambda x: x.startswith("* "), lines))):
        return block_type_ulist
    if all(list(map(lambda x: x.startswith("- "), lines))):
        return block_type_ulist

    line_number = 0
    for line in lines:
        if not line.startswith(f"{line_number + 1}. "):
            break
        line_number += 1
    if line_number == len(lines):
        return block_type_olist

    return block_type_paragraph

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == block_type_paragraph:
            replaced_markdown = block.replace("\n", " ")
            text_nodes = text_to_textnodes(replaced_markdown)
            html_nodes = list(map(text_node_to_html_node, text_nodes))
            children.append(ParentNode("p", html_nodes))
        if block_type == block_type_heading:
            split_markdown = block.split("# ")
            heading_size = len(split_markdown[0]) + 1
            text_nodes = text_to_textnodes(split_markdown[-1])
            html_nodes = list(map(text_node_to_html_node, text_nodes))
            children.append(ParentNode(f"h{heading_size}", html_nodes))
        if block_type == block_type_code:
            stripped_markdown = block.strip("```")
            text_nodes = text_to_textnodes(stripped_markdown)
            html_nodes = list(map(text_node_to_html_node, text_nodes))
            children.append(ParentNode("pre", ParentNode("code", html_nodes)))
        if block_type == block_type_quote:
            replaced_markdown = block.replace("\n", " ").replace("> ", "")
            text_nodes = text_to_textnodes(replaced_markdown)
            html_nodes = list(map(text_node_to_html_node, text_nodes))
            children.append(ParentNode("blockquote", html_nodes))
        if block_type == block_type_olist:
            split_markdown = block.split("\n")
            text_nodes = list(map(lambda x: text_to_textnodes(x.split(". ", 1)[1]), split_markdown))
            html_nodes = list(map(lambda x: ParentNode("li", list(map(lambda y: text_node_to_html_node(y), x))), text_nodes))
            children.append(ParentNode("ol", html_nodes))
        if block_type == block_type_ulist:
            split_markdown = block.split("\n")
            text_nodes = list(map(text_to_textnodes, list(map(lambda x: x.split("* ", 1)[1] if x.startswith("* ") else x.split("- ", 1)[1], split_markdown))))
            html_nodes = list(map(lambda x: ParentNode("li", list(map(lambda y: text_node_to_html_node(y), x))), text_nodes))
            children.append(ParentNode("ul", html_nodes))
    html_node = ParentNode("div", children)
    return html_node

if __name__ == "__main__":
        md = """
* This is a list
* with items
* and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        print(html)
        print("<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>")
