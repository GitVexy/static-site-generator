import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from functions import (
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type)


def log(function_name):
    print(f"{function_name}")


class TestHTMLNode(unittest.TestCase):
    def run(self, result=None):
        super().run(result)
        log(self._testMethodName)

    def setUp(self):
        child1, child2 = "", ""  # To avoid errors. Redundant
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
        self.node = TextNode("This is a text node",
                             TextType.TEXT, "https://www.boot.dev/")
        self.node2 = TextNode("This is a text node",
                              TextType.TEXT, "https://www.boot.dev/")
        self.node3 = TextNode("This is another text node",
                              TextType.TEXT)
        self.text = TextNode("text", TextType.TEXT, "boot.dev")
        self.bold = TextNode("bold", TextType.BOLD, "boot.dev")
        self.italic = TextNode("italic", TextType.ITALIC, "boot.dev")
        self.code = TextNode("code", TextType.CODE, "boot.dev")
        self.link = TextNode("link", TextType.LINK, "boot.dev")
        self.image = TextNode("image", TextType.IMAGE, "boot.dev")
        self.html_strings = {
            "text":     "text",
            "bold":     "<b>bold</b>",
            "italic":   "<i>italic</i>",
            "code":     "<code>code</code>",
            "link":     "<a href=boot.dev>link</a>",
            "image":    "<img src=boot.dev alt=image></img>"
        }

    def test_text_node_to_html_text(self):
        text = text_node_to_html_node(self.text)
        self.assertEqual(text.to_html(), self.html_strings["text"])

    def test_text_node_to_html_bold(self):
        bold = text_node_to_html_node(self.bold)
        self.assertEqual(bold.to_html(), self.html_strings["bold"])

    def test_text_node_to_html_italic(self):
        italic = text_node_to_html_node(self.italic)
        self.assertEqual(italic.to_html(), self.html_strings["italic"])

    def test_text_node_to_html_code(self):
        code = text_node_to_html_node(self.code)
        self.assertEqual(code.to_html(), self.html_strings["code"])

    def test_text_node_to_html_link(self):
        link = text_node_to_html_node(self.link)
        self.assertEqual(link.to_html(), self.html_strings["link"])

    def test_text_node_to_html_image(self):
        image = text_node_to_html_node(self.image)
        self.assertEqual(image.to_html(), self.html_strings["image"])

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


class TestParentNode(unittest.TestCase):
    def run(self, result=None):
        super().run(result)
        log(self._testMethodName)

    def setUp(self):
        self.child1 = LeafNode(tag="a", value="Child 1", props={
                               "href": "https://www.boot.dev/"})
        self.child2 = LeafNode(tag="p", value="Child 2")
        self.node = ParentNode(tag="h1", children=[
                               self.child1, self.child2], props={"boot": "dev"})
        self.node2 = ParentNode(
            tag="h1", children=[self.child1, self.child2], props={"boot": "dev"})
        self.node3 = ParentNode(tag="h1", children=[self.node, self.child2], props={
                                "boot": "dev"})  # Nested parents

    def test_parent_node_nested_parents(self):
        self.assertIsInstance(self.node3.to_html(), str)

    def test_parent_node_equal(self):
        self.assertEqual(self.node, self.node2)

    def test_parent_node_not_equal(self):
        self.assertNotEqual(self.node, self.node3)

    def test_parent_node_has_tag(self):
        self.assertIsNotNone(self.node.tag)

    def test_parent_node_has_children(self):
        self.assertIsNotNone(self.node.children)

    def test_parent_node_has_props(self):
        self.assertIsNotNone(self.node.props)

    def test_parent_node_has_repr(self):
        self.assertTrue(self.node.__repr__().__contains__("ParentNode"))


class TestFunctions(unittest.TestCase):
    def run(self, result=None):
        super().run(result)
        log(self._testMethodName)

    def setUp(self):
        self.bold = TextNode(
            "Text with a **bolded** word", TextType.TEXT)
        self.bold_double = TextNode(
            "Text with a **bolded** word and **another**", TextType.TEXT)
        self.bold_multiword = TextNode(
            "Text with a **bolded word** and **another**", TextType.TEXT)
        self.italic = TextNode(
            "Text with an *italic* word", TextType.TEXT)
        self.bold_and_italic = TextNode("**bold** and *italic*", TextType.TEXT)
        self.code = TextNode(
            "Text with a `code block` word", TextType.TEXT)
        self.img = TextNode(
            "Text with an ![image](IMAGINE)", TextType.TEXT)
        self.imgs = TextNode(
            "![image](IMAGINE) and ![image2](damn)", TextType.TEXT)
        self.link = TextNode(
            "Text with a [link](boot.dev)", TextType.TEXT)
        self.links = TextNode(
            "[link](boot.dev) and ![nlink](boot.dev)", TextType.TEXT)

    def test_delim_bold(self):
        new_nodes = split_nodes_delimiter([self.bold], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("Text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        new_nodes = split_nodes_delimiter(
            [self.bold_double], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("Text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        new_nodes = split_nodes_delimiter(
            [self.bold_multiword], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("Text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        new_nodes = split_nodes_delimiter([self.italic], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("Text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        new_nodes = split_nodes_delimiter(
            [self.bold_and_italic], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        new_nodes = split_nodes_delimiter([self.code], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("Text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_extract_img(self):
        img = extract_markdown_images(self.img.text)
        self.assertListEqual(
            [('image', 'IMAGINE')],
            img
        )

    def test_extract_link(self):
        link = extract_markdown_links(self.link.text)
        self.assertListEqual(
            [('link', 'boot.dev')],
            link
        )

    def test_extract_img_multi(self):
        imgs = extract_markdown_images(self.imgs.text)
        self.assertListEqual(
            [('image', 'IMAGINE'), ('image2', 'damn')],
            imgs
        )

    def test_extract_link_multi(self):
        links = extract_markdown_links(self.links.text)
        self.assertListEqual(
            [('link', 'boot.dev')],
            links
        )

    def test_split_image(self):
        node = TextNode(
            "Text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE,
                         "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            ("Text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
             " and another ![second image](https://i.imgur.com/3elNhQu.png)"),
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            ("Text with a [link](https://boot.dev) and"
             " [another link](https://blog.boot.dev) with text that follows"),
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK,
                         "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            ("This is **text** with an *italic* word and a `code block` and an"
             " ![image](https://i.imgur.com/zjjcJKZ.png) and"
             " a [link](https://boot.dev)")
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_markdown_to_blocks(self):
        markdown_string = ("""
# This is a heading\n\n
This is a paragraph of text. It has some **bold** and *italic* words.


* This is the first list item in a list block
* This is a list item
* This is another list item\n\n\n
* This is difficult
""")
        blocks = markdown_to_blocks(markdown_string)
        self.assertListEqual(
            [
                '# This is a heading',
                'This is a paragraph of text. It has some **bold** '
                'and *italic* words.',
                '* This is the first list item in a list block\n'
                '* This is a list item\n'
                '* This is another list item',
                '* This is difficult'
            ], blocks
        )

    def test_block_to_block_type(self):
        tests = [
            "This is a paragraph.\nNothing special",
            "## This is a heading",
            "```\nThis is code\n```",
            ">This is a quote",
            "* This\n- is an unordered\n* list",
            "1. This\n2. is an ordered\n3. list",
            "```\n1. This is chaos\n# and will be\n* a paragraph"
        ]
        results = []
        expected_result = [
            "paragraph",
            "heading",
            "code",
            "quote",
            "unordered_list",
            "ordered_list",
            "paragraph"
        ]
        for test in tests:
            results.append(block_to_block_type(test))
            print(f"{test} = {block_to_block_type(test)}")
        self.assertEqual(results, expected_result)


if __name__ == "__main__":
    unittest.main()
