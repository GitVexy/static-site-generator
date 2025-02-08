from htmlnode import *
from textnode import *
import re as regex

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag = None,   value=text_node.text)
        
        case TextType.BOLD:
            return LeafNode(tag = "b",    value=text_node.text)
        
        case TextType.ITALIC:
            return LeafNode(tag = "i",    value=text_node.text)
        
        case TextType.CODE:
            return LeafNode(tag = "code", value=text_node.text)
        
        case TextType.LINK:
            return LeafNode(tag = "a",    value=text_node.text, props={"href": text_node.url})
        
        case TextType.IMAGE:
            return LeafNode(tag = "img",  value = "", props = {"src": text_node.url, "alt": text_node.text})
        
        case _:
            raise ValueError(f"Unsupported TextType: {text_node.text_type}")

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType) -> list:
    new_nodes = []
    
    for node in old_nodes:
        
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        sectioned_nodes = []
        sections: list = node.text.split(delimiter)
        
        if len(sections) % 2 == 0:
            raise ValueError(f"Invalid markdown. Missing closing delimiter\nValue: {node.text}")
        
        for i in range(len(sections)):
            if not sections[i]:
                continue
            
            if i % 2 == 0:
                sectioned_nodes.append(TextNode(sections[i], TextType.TEXT))
            
            else:
                sectioned_nodes.append(TextNode(sections[i], text_type))
        
        new_nodes.extend(sectioned_nodes)
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple]:
    return regex.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text: str) -> list[tuple]:
    return regex.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []
    
    for old_node in old_nodes:
        
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            
            original_text = sections[1]
        
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
            
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
        
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    delimiters = [
        ("**", TextType.BOLD),
        ("*", TextType.ITALIC),
        ("`", TextType.CODE)
        ]
    
    for delimiter in delimiters:
        nodes = split_nodes_delimiter(nodes, delimiter[0], delimiter[1])
    
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    output_blocks = []
    
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:
            output_blocks.append(stripped_block)
    
    return output_blocks

markdown_string = (
"""# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item


* This is difficult""")

print(markdown_to_blocks(markdown_string))