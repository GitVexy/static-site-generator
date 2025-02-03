# Runs from ./main.sh
from textnode import *
from htmlnode import *

def main():
    nodes = [
        LeafNode("h1", "Hello world"),
        LeafNode("p", "This is a test"),
        LeafNode("p", "This is test 2"),
        LeafNode("a", "Recursion is cool", props={"href": "http://127.0.0.1:8888"})
    ]
    output = ""
    
    for node in nodes:
        output += node.to_html()
    print(output)

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Unsupported TextType: {text_node.text_type}")

main()