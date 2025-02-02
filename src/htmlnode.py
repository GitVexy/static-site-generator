

class HTMLNode():
    def __init__(self,
                    tag: str = None,
                    value: str = None,
                    children: list = None,
                    props: dict = None):
        
        self.tag        = tag
        self.value      = value
        self.children   = children
        self.props      = props

    def __repr__(self):
        return f"HTMLNode('{self.tag}', '{self.value}', '{self.children}', '{self.props}')"

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        output = ""
        
        for key in self.props.keys():
            output += key + "=" + f"{self.props[key]} "
        output = " " + output.rstrip(" ")
        return output

class LeafNode(HTMLNode):
    def __init__(self,
                    tag: str,
                    value: str,
                    props: dict = None):
        
        super().__init__(tag=tag, value=value, props=props)
    
    def __repr__(self):
        return super().__repr__().replace("HTMLNode", "LeafNode")

    def to_html(self):
        if not self.value:
            raise ValueError(f"Node missing value. Value is {self.value}")
        if not self.tag:
            return self.value
        props = ""
        if self.props:
            props = self.props_to_html()
        
        output = f"<{self.tag}{props}>{self.value}</{self.tag}>"
        return output



"""Tests
test = LeafNode("a",
                "Hello 2",
                {   "href": "https://www.google.com/",
                    "target": "_blank"})
print(test)
print(str(test.to_html()))
test.tag, test.props = "p", None
print(str(test.to_html()))
assignment_test = LeafNode("p", "This is a paragraph of text.")
assignment_test2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
print(assignment_test.to_html())
print(assignment_test2.to_html())

meme = HTMLNode(tag="p", value="Hello world", children=[test, test2], props={"href": "https://www.google.com", "target": "_blank"})
print(HTMLNode.props_to_html(meme))
print(meme)
"""
