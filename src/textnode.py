from enum import Enum
from htmlnode import *
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__ (self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__ (self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False
    def __repr__ (self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

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
            raise ValueError(f"invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    print ("split_nodes_delimiter old_nodes:", old_nodes) 
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        elif delimiter in node.text:
            delimiter_count = node.text.count(delimiter)
            if delimiter_count == 0:
                new_nodes.append(node)
                continue
            if delimiter_count % 2 == 0:
                inner_nodes = []
                inner_nodes.extend(node.text.split(delimiter))
                for i in range (0,len(inner_nodes)):
                    if len(inner_nodes[i])>0:
                        if i % 2 == 1:
                            new_nodes.append(TextNode(inner_nodes[i], text_type, ))
                        else:
                            new_nodes.append(TextNode(inner_nodes[i], TextType.TEXT,))
            else:
                raise Exception("Invalid Markdown Syntax")
        else:
            new_nodes.append(node)
    print ("split_nodes_delimiter delimiter:", delimiter, "new_nodes:", new_nodes)
    return new_nodes
    
def extract_markdown_images(text):
    result = []
    extract = re.findall(r"(\!\[.*?\]\(.*?\))",text)
    for link in extract:
        tupel = ((*re.findall(r"\!\[(.*?)\]",link),*re.findall(r"\((.*?)\)",link)))
        print (tupel)
        result.append(tupel)
    return result

def extract_markdown_links(text):
    result = []
    extract = re.findall(r"(\[.*?\]\(.*?\))",text)
    for link in extract:
        result.append((*re.findall(r"\[(.*?)\]",link),*re.findall(r"\((.*?)\)",link)))
    return result



# images
#r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"

# regular links
#r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

def split_nodes_image(old_nodes):
    result = []
    for nodes in old_nodes:
        if nodes.text_type != TextType.TEXT:
            result.append(nodes)
            continue
        extract = extract_markdown_images(nodes.text)
        if len(extract) == 0:
            result.append(nodes)
            continue
        for image in extract:
            md_image = f"![{image[0]}]({image[1]})"
            originalsplit = nodes.text.split(md_image, 1)
            if originalsplit[0] != "":
                node = TextNode(f"{originalsplit[0]}", TextType.TEXT,)
                result.append(node)
            result.append(TextNode(f"{image[0]}", TextType.IMAGE, image[1]))
            nodes.text = originalsplit[1]
        originalsplit = nodes.text.split(md_image, 1)
        if originalsplit[0] != "":
            result.append(TextNode(f"{originalsplit[0]}", TextType.TEXT,))
    return result      

def split_nodes_link(old_nodes):
    print("split_nodes_link: old_nodes:", old_nodes)
    result = []
    for nodes in old_nodes:
        if nodes.text_type != TextType.TEXT:
            result.append(nodes)
            continue
        extract = extract_markdown_links(nodes.text)
        if len(extract) == 0:
            result.append(nodes)
            continue
        for image in extract:
            md_image = f"[{image[0]}]({image[1]})"
            originalsplit = nodes.text.split(md_image, 1)
            if originalsplit[0] != "":
                node = TextNode(originalsplit[0], TextType.TEXT,)
                result.append(node)
            result.append(TextNode(image[0], TextType.LINK, image[1]))
            nodes.text = originalsplit[1]
        originalsplit = nodes.text.split(md_image, 1)
        if originalsplit[0] != "":
            result.append(TextNode(originalsplit[0], TextType.TEXT,))
    return result      

def text_to_textnodes(text):
    print("---------------------------")
    result = [TextNode(text, TextType.TEXT,)]
    print(result)
    result = split_nodes_image(result)
    print(result)
    result = split_nodes_link(result)
    print(result)
    print("---------------------------")
    for type in [('**', TextType.BOLD), ('_', TextType.ITALIC), ('`', TextType.CODE)]:
        result = split_nodes_delimiter(result, type[0], type[1])
        print(result)
    print(result)
    return result

def markdown_to_blocks(markdown):
    result = []
    for block in markdown.split("\n\n"):
        block = block.strip()
        print(block)
        if block != "":
            result.append(block)
        #print ("markdown_to_block:",result)
    return result

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"

def block_to_block_type(markdown):
    splitted = markdown.split("\n")
    nlines = len(splitted)
    #heading
    heading = True
    for lines in splitted:
        if re.findall("^#+ ",lines) == []:
            heading = False
    if heading == True:
        return BlockType.HEADING
    #code
    if re.findall("^```.*```$", "".join(markdown.split("\n"))) != []:
        return BlockType.CODE
    #quote
    quote = True
    for lines in splitted:
        if re.findall("^>",lines) == []:
            quote = False
    if quote == True:
        return BlockType.QUOTE
    #unordered
    unordered = True
    for lines in splitted:
        if re.findall("^- ",lines) == []:
            unordered = False
    if unordered == True:
        return BlockType.UNORDERED
    #ordered
    ordered = True
    n = 1
    for lines in splitted:
        if re.findall(f"^{n}\. ", lines) == []:
            ordered = False
        n += 1
    if ordered == True:
        return BlockType.ORDERED
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    print("Markdown_to_blocks:", blocks)
    children = []
    for block in blocks:
        html_block = block_to_html(block)
        children.append(html_block)
    return ParentNode("div", children)

def extract_title(markdown):
    lines=markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No title has been found")


def block_to_html(block):
    block_type = block_to_block_type(block)
    print("block_to_html:", block, block_type)
    match block_type:
        case BlockType.HEADING:
            return heading_block_to_html_node(block)
        case BlockType.CODE:
            return code_block_to_html_node(block)
        case BlockType.QUOTE:
            return quote_block_to_html_node(block)
        case BlockType.UNORDERED:
            return unordered_block_to_html_node(block)
        case BlockType.ORDERED:
            return ordered_block_to_html_node(block)
        case BlockType.PARAGRAPH:
            return paragraph_block_to_html_node(block)
        case _:
            raise Exception("Unknown Blocktype")

def heading_block_to_html_node(block):
    heading_level = len(re.findall("^#+",block)[0])
    heading = f"h{heading_level}"
    text = block [heading_level + 1:]
    children = text_to_children(text)
    return ParentNode(heading, children)
        

def code_block_to_html_node(block):
    text = block[4:-3]
    print(f"CodeBlockText: {text}")
    #children = text_to_children(text)
    text_node = TextNode(text, TextType.TEXT)
    children = text_node_to_html_node(text_node)
    print("code_block_to_html_node, children:",children)
    inner = ParentNode("code", [children])
    print("code_block_to_html_node, inner:",inner)
    outer = ParentNode("pre", [inner])
    print("code_block_to_html_node, outer:",outer)
    return outer
    

def quote_block_to_html_node(block):
    text_list = block.split('\n')
    changed_text = []
    for text in text_list:
        changed_text.append(text[1:].strip())
    text = " ".join(changed_text)
    children = text_to_children(text)
    return ParentNode("blockquote", children)


def unordered_block_to_html_node(block):
    text_list = block.split('\n')
    items = []
    for text in text_list:
        children = text_to_children(text[2:])
        items.append(ParentNode("li", children))
    return ParentNode("ul", items)
    

def ordered_block_to_html_node(block):
    text_list = block.split('\n')
    items = []
    for text in text_list:
        space = text.find(" ")
        children = text_to_children(text[space +1:])
        items.append(ParentNode("li", children))
    return ParentNode("ol", items)

def paragraph_block_to_html_node(block):
    text_list = block.split('\n')
    text = " ".join(text_list)
    children = text_to_children(text)
    return ParentNode("p", children)


def text_to_children(markdown):
    textnodes_children = text_to_textnodes(markdown)
    children = []
    for textnode in textnodes_children:
        children.append(text_node_to_html_node(textnode))
    print ("text_to_children:", textnodes_children, "result:", children)
    return children
            
