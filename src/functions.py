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
        
        else:
            sectioned_nodes = []
            sections: list = node.text.split(delimiter)
            
            if len(sections) % 2 == 0:
                raise ValueError("invalid markdown, formatted section not closed")
            
            for i in range(len(sections)):
                if not sections[i]:
                    continue
                
                if i % 2 == 0:
                    sectioned_nodes.append(TextNode(sections[i], TextType.TEXT))
                
                else:
                    sectioned_nodes.append(TextNode(sections[i], text_type))
            
            new_nodes.extend(sectioned_nodes)
        
        return new_nodes

