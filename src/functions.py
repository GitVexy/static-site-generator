from htmlnode import LeafNode
from textnode import TextType, TextNode
import re as regex


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None,
                            value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b",
                            value=text_node.text)

        case TextType.ITALIC:
            return LeafNode(tag="i",
                            value=text_node.text)

        case TextType.CODE:
            return LeafNode(tag="code",
                            value=text_node.text)

        case TextType.LINK:
            return LeafNode(tag="a",
                            value=text_node.text,
                            props={"href": text_node.url})

        case TextType.IMAGE:
            return LeafNode(tag="img",
                            value="",
                            props={"src": text_node.url,
                                   "alt": text_node.text})

        case _:
            raise ValueError(f"Unsupported TextType: {text_node.text_type}")


def split_nodes_delimiter(old_nodes: list,
                          delimiter: str,
                          text_type: TextType) -> list:
    new_nodes = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        sectioned_nodes = []
        sections: list = node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise ValueError(
                f"Invalid markdown. Missing closing delimiter\nValue: {node.text}")

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


def block_to_block_type(markdown: str) -> str:
    split_lines = markdown.split("\n")
    # print(f"split_lines: {split_lines}")
    line_lens = []
    for line in split_lines:
        line_lens.append(len(line))
    line_lens = sorted(line_lens)
    # print(f"line_lens: {line_lens}")
    shortest_line_len = line_lens[0]
    # print(f"shortest_line_len: {shortest_line_len}")

    # ORDERED LIST
    if (shortest_line_len >= 3
            and split_lines[0][:3] == "1. "):
        o_list_check = True
        for i in range(1, len(split_lines)):
            if split_lines[i][:3] != f"{i + 1}. ":
                o_list_check = False
        if o_list_check:
            return "ordered_list"

    # UNORDERED LIST
    if (shortest_line_len >= 2
            and (split_lines[0][:2] == "* "
                 or split_lines[0][:2] == "- ")):
        u_list_check = True
        for line in split_lines:
            if (line[:2] == "* " or
                    line[:2] == "- "):
                continue
            else:
                u_list_check = False
        if u_list_check:
            return "unordered_list"

    # QUOTE
    if (shortest_line_len >= 1
            and split_lines[0][0] == ">"):
        q_list_check = True
        for line in split_lines:
            if line[0] == ">":
                continue
            else:
                q_list_check = False
        if q_list_check:
            return "quote"

    # CODE
    if (shortest_line_len >= 6
            and len(markdown) >= 4
            and "```" == markdown[:3]
            and "```" == markdown[-3:]):
        return "code"

    # HEADING
    if (shortest_line_len >= 3
            and markdown[0] == "#"):
        for i in range(1, len(markdown) + 1):
            if (markdown[i] == "#"
                    and i <= 5):
                continue
            elif (markdown[i] == "#"
                    and i > 5):
                break
            elif (markdown[i] == " "
                  and len(markdown) >= i + 1):
                return "heading"

    # PARAGRAPH
    return "paragraph"


# paragraph = "This is just normal text in a paragraph\nNothing special about it"
# heading = "# BIG TITLE"
# code = "```return to_sender\nmore_core```"
# quote = ">quotes\n> and dat\n> fam"
# u_list = "* Testing\n- One two three\n* Everything alright"
# o_list = "1. Test\n2. Test\n3. Meme"
#
# print(block_to_block_type(paragraph))
# print(block_to_block_type(heading))
# print(block_to_block_type(code))
# print(block_to_block_type(quote))
# print(block_to_block_type(u_list))
# print(block_to_block_type(o_list))
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
