class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        if self.props == None:
            return ""
        print("self.props:", self.props)
        result = ""
        for option in self.props:
            print (option)
            result += f' {option}="{self.props[option]}"'
            print("self.props.html.result:", result)
        return result
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        result = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        print ("LeafNode.to_html result:", result)
        return result

    def __repr__(self):
        result = f"LeafNode: (tag:{self.tag}, value:{self.value}, props:{self.props})"
        return result  #f"LeafNode: (tag={self.tag}, value={self.value}, props={self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError
        if self.children == None:
            raise ValueError("children missing")
        html = ""
        for c in self.children:
            html += c.to_html()
        result = f"<{self.tag}{self.props_to_html()}>{html}</{self.tag}>"
        print (result)
        return result # f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        result = f"ParentNode: (tag:{self.tag}, children:{self.children}, props:{self.props})"
        return result
