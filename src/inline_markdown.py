import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
    text_node_to_html_node,
)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type == text_type_text:
            split_text = old_node.text.split(delimiter)
            # after splitting there should be an odd number of elements
            if len(split_text) % 2 == 0:
                raise Exception(f"Missing a corresponding {delimiter} tag")

            text_node = True
            for text_chunk in split_text:
                if text_chunk != "":
                    new_nodes.append(TextNode(text_chunk, text_type_text if text_node else text_type))
                text_node = not text_node
        else:
            new_nodes.append(old_node)
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type == text_type_text:
            old_node_text = old_node.text
            images = extract_markdown_images(old_node_text)
            if len(images) > 0:
                for image in images:
                    split_text = old_node_text.split(f"![{image[0]}]({image[1]})")
                    if split_text[0] != "":
                        new_nodes.append(TextNode(split_text[0], text_type_text))
                    new_nodes.append(TextNode(image[0], text_type_image, image[1]))
                    old_node_text = "".join(split_text[1:])
                if old_node_text != "":
                    new_nodes.append(TextNode(old_node_text, text_type_text))
            else:
                new_nodes.append(old_node)
        else:
            new_nodes.append(old_node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type == text_type_text:
            old_node_text = old_node.text
            links = extract_markdown_links(old_node_text)
            if len(links) > 0:
                for link in links:
                    split_text = old_node_text.split(f"[{link[0]}]({link[1]})")
                    if split_text[0] != "":
                        new_nodes.append(TextNode(split_text[0], text_type_text))
                    new_nodes.append(TextNode(link[0], text_type_link, link[1]))
                    old_node_text = "".join(split_text[1:])
                if old_node_text != "":
                    new_nodes.append(TextNode(old_node_text, text_type_text))
            else:
                new_nodes.append(old_node)
        else:
            new_nodes.append(old_node)
    return new_nodes

def text_to_textnodes(text):
    text_node = TextNode(text, text_type_text)
    nodes = split_nodes_delimiter([text_node], "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes

if __name__ == '__main__':
    text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) and following text."
    # [
    #     TextNode("This is ", text_type_text),
    #     TextNode("text", text_type_bold),
    #     TextNode(" with an ", text_type_text),
    #     TextNode("italic", text_type_italic),
    #     TextNode(" word and a ", text_type_text),
    #     TextNode("code block", text_type_code),
    #     TextNode(" and an ", text_type_text),
    #     TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
    #     TextNode(" and a ", text_type_text),
    #     TextNode("link", text_type_link, "https://boot.dev"),
    #     TextNode(" and following text.", text_type_text),
    # ]
    nodes = text_to_textnodes(text)
    for node in nodes:
        print(node)
