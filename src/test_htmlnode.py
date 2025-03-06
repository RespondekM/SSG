import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a","TextType",props={"abc": "def"})
        node1 = HTMLNode("a1",children=["cef"],props={"abc": "def"})
        node2 = HTMLNode("a2","TextType")
        node3 = HTMLNode("a3","NewType",{"abc": "def"})
        lnode = LeafNode("p", "This is a paragraph of text.")
        lnode1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"}) 
        pnode = ParentNode("p", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text")])
        #print(node)
        #print(node1)
        #print(node2)
        #print(node3)
        #print(lnode)
        #print(lnode1)
        #print(pnode)
        #print(lnode.to_html())
        #print(lnode1.to_html())
        #print(pnode.to_html())
        


if __name__ == "__main__":
    unittest.main()
