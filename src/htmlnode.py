

class HTMLNode():
    def __init__(self,
                 tag: str = None,
                 value: str = None,
                 children: list = None,
                 props: dict = None):

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return (
            f"HTMLNode('{self.tag}', '{self.value}', '{
                self.children}', '{self.props}')"
        )

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        output = ""

        for key in self.props.keys():
            output += key + "=" + f"{self.props[key]} "
        output = " " + output.rstrip(" ")
        return output


class ParentNode(HTMLNode):
    def __init__(self,
                 tag: str,
                 children: list,
                 props: dict = None
                 ):
        super().__init__(tag=tag, children=children, props=props)

    def __repr__(self):
        return super().__repr__().replace("HTMLNode", "ParentNode")

    def __eq__(self, other):
        if not isinstance(other, ParentNode):
            return False
        return (
            self.tag == other.tag and
            self.props == other.props and
            self.children == other.children)

    def to_html(self):
        if not self.tag:
            raise ValueError(f"Missing values in {
                             self}. Expecting tag, children, props")
        if not self.children:
            raise ValueError(f"Missing values in {
                             self}. Expecting tag, children, props")

        output = f"<{self.tag}"

        if self.props:
            output += f"{self.props_to_html()}>"
        else:
            output += ">"

        for child in self.children:
            output += child.to_html()
        output += f"</{self.tag}>"

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
        if not type(self.value) is str:
            raise ValueError("Node missing value. Expecting populated string")
        if not self.tag:
            return self.value
        props = ""
        if self.props:
            props = self.props_to_html()

        output = f"<{self.tag}{props}>{self.value}</{self.tag}>"
        return output
