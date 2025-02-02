import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    
    def test_empty_htmlnode(self):
        empty_node = HTMLNode()
        self.assertIsNone(empty_node.tag)
        self.assertIsNone(empty_node.value)
        self.assertIsNone(empty_node.children)
        self.assertIsNone(empty_node.props)
    
    def test_htmlnode_has_tag(self):
        node = HTMLNode(tag="p")
        self.assertIsNotNone(node.tag,
                             "node.tag is NoneType")
    
    def test_htmlnode_has_value(self):
        node = HTMLNode(value="Hello world")
        self.assertIsNotNone(node.value,
                             "node.value is NoneType")
    
    def test_htmlnode_has_children(self):
        test = HTMLNode()
        test2 = HTMLNode()
        node = HTMLNode(children=[test, test2])
        self.assertIsNotNone(node.children,
                             "node.children is NoneType")
    
    def test_htmlnode_has_props(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertIsNotNone(node.props,
                             "node.props is NoneType")
    
    def test_htmlnode_has_repr(self):
        test = HTMLNode()
        test2 = HTMLNode()
        node = HTMLNode(tag="p", vaue="Hello world", children=[test, test2], props={"href": "https://www.google.com", "target": "_blank"})
        self.assertTrue(node.__repr__().__contains__("HTMLNode"),
                        "Node __repr__ output does not contain 'HTMLNode'")

class TestLeafNode(unittest.TestCase):
    def generate_node(self):
        node = LeafNode(tag="p",
                        value="Hello world",
                        props={
                            "href": "https://www.google.com",
                            "target": "_blank"})
        return node

    def test_leafnode_has_tag(self):
        node = self.generate_node()
        self.assertIsNotNone(node.tag,
                             "node.tag is NoneType")

    def test_leafnode_has_value(self):
        node = self.generate_node()
        self.assertIsNotNone(node.value,
                             "node.value is NoneType")

    def test_leafnode_has_props(self):
        node = self.generate_node()
        self.assertIsNotNone(node.props,
                             "node.props is NoneType")
    
    def test_leafnode_has_repr(self):
        node = self.generate_node()
        self.assertTrue(node.__repr__().__contains__("LeafNode"),
                        "Node __repr__ output does not contain 'LeafNode'")
    

if __name__ == "__main__":
    unittest.main()
