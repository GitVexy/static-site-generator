# Runs from ./main.sh
from textnode import *

def main():
    meme    = TextNode("Hello World", TextType.BOLD, "https://meme.com/")
    print(meme)

main()