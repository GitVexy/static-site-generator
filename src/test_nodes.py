import unittest

from htmlnode import *
from textnode import *

def log(function_name):
    print(f"{function_name}: OK")

class TestHTMLNode(unittest.TestCase):
    def run(self, result=None):
        super().run(result)
        log(self._testMethodName)
    
    def setUp(self):
        child1, child2 = "", "" # To avoid errors. Redundant
        self.node = HTMLNode(tag="p",
                        value="Hello world",
                        children=[child1, child2],
                        props={
                            "href": "https://www.boot.dev/",
                            "target": "_blank"})
        self.empty_node = HTMLNode()
    
    def test_htmlnode_empty(self):
        for property in [self.empty_node.tag,
                        self.empty_node.value,
                        self.empty_node.children,
                        self.empty_node.props]:
            self.assertIsNone(property)
    
    def test_htmlnode_has_tag(self):
        self.assertIsNotNone(self.node.tag)
    
    def test_htmlnode_has_value(self):
        self.assertIsNotNone(self.node.value)
    
    def test_htmlnode_has_children(self):
        self.assertIsNotNone(self.node.children)
    
    def test_htmlnode_has_props(self):
        self.assertIsNotNone(self.node.props)
    
    def test_htmlnode_has_repr(self):
        self.assertTrue(self.node.__repr__().__contains__("HTMLNode"))

class TestLeafNode(unittest.TestCase):
    def run(self, result=None):
        super().run(result)
        log(self._testMethodName)
    
    def setUp(self):
        self.node = LeafNode(tag="p",
                        value="Hello world",
                        props={
                            "href": "https://www.boot.dev/",
                            "target": "_blank"})
    
    def test_leafnode_has_tag(self):
        self.assertIsNotNone(self.node.tag)
    
    def test_leafnode_has_value(self):
        self.assertIsNotNone(self.node.value)
    
    def test_leafnode_has_props(self):
        self.assertIsNotNone(self.node.props)
    
    def test_leafnode_has_repr(self):
        self.assertTrue(self.node.__repr__().__contains__("LeafNode"))

class TestTextNode(unittest.TestCase):
    def run(self, result=None):
        super().run(result)
        log(self._testMethodName)
    
    def setUp(self):
        self.node =  TextNode("This is a text node",        TextType.NORMAL, "https://www.boot.dev/") # Original
        self.node2 = TextNode("This is a text node",        TextType.NORMAL, "https://www.boot.dev/") # Same
        self.node3 = TextNode("This is another text node",  TextType.NORMAL)                      # Different
    
    def test_text_node_equal(self):
        self.assertEqual(self.node, self.node2)
    
    def test_text_node_not_equal(self):
        self.assertNotEqual(self.node, self.node3)
    
    def test_text_node_type_text_string(self):
        self.assertIsInstance(self.node.text, str)
    
    def test_text_node_type_text_type_class(self):
        self.assertIsInstance(self.node.text_type, TextType)
    
    def test_text_node_type_url_string(self):
        self.assertIsInstance(self.node.url, str)
    
    def test_text_node_type_url_none(self):
        self.assertIsInstance(self.node3.url, type(None))

if __name__ == "__main__":
    unittest.main()
