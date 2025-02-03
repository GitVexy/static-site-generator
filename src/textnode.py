from enum import Enum

class TextType (Enum):
    TEXT  = "normal"
    BOLD    = "bold"
    ITALIC  = "italic"
    CODE    = "code"
    LINK    = "link"
    IMAGE   = "image"

class TextNode ():
    def __init__(self, text: str, text_type, url=None):
        self.text       = str(text)
        self.text_type  = text_type
        self.url        = url
    
    def __eq__(self, target):
        return (
            self.text       == target.text      and
            self.text_type  == target.text_type and
            self.url        == target.url
        )
    
    def __repr__(self):
        return (f"TextNode({str(self.text)}, {str(self.text_type.value)}, {str(self.url)})")

# print()
# meme    = TextNode("Hello World", TextType.BOLD, "https://meme.com/")
# meme2   = TextNode("Hello World", TextType.BOLD, "https://meme.com/")
# print(meme)