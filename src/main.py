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
        output += node.to_html() + "\n"
    print(output)

main()