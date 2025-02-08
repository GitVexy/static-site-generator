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

link_node = TextNode("[links](link1) like [this](link2) right here", TextType.TEXT,)
node = TextNode("Raw text node", TextType.TEXT)
image_node = TextNode("These are two ![images](image1) like ![this](image2)", TextType.TEXT,)



#Regex shenannigans
#image = "This is text with an image ![look at me](https://i.imgur.com/aKaOqIh.gif)"
#print(extract_markdown_images(image))
## Outputs: [('look at me', 'https://i.imgur.com/aKaOqIh.gif')]
#
#link = "This is text with a link [click me](https://i.imgur.com/aKaOqIh.gif)"
#print(extract_markdown_links(link))
## Outputs: [('click me', 'https://i.imgur.com/aKaOqIh.gif')] 