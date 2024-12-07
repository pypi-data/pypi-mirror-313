import os
from gai.lib.common.TextSplitter import TextSplitter

"""
file_utils.split_text(): This function uses TextSplitter class internally.
TextSplitter class: This function is lifted from langchain's RecursiveCharacterTextSplitter class.
"""

from rich.console import Console
console=Console()

sample_text = ""
here=os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(here,"./pm_long_speech_2023.txt")) as f:
    sample_text = f.read()

def test_split_text_without_overlap():
    chunk_size = 500
    chunk_overlap = 0
    splitter = TextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
    chunks = splitter.split_text(sample_text)
    console.print("[yellow italic]Chunks[/]")
    total = 0
    for i,chunk in enumerate(chunks):
        assert len(chunk) <= 500
        console.print(f"Chunk({i}):[yellow italic]{len(chunk)}[/]")
        console.print(chunk)
        total += len(chunk)
    console.print(f"Length of text size: [yellow italic]{len(sample_text)}[/]")
    console.print(f"Total sum of chunk size: [yellow italic]{total}[/]")

def test_split_text_with_overlap():
    chunk_size = 500
    chunk_overlap = 50
    splitter = TextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
    chunks = splitter.split_text(sample_text)
    console.print("[yellow italic]Chunks[/]")
    total = 0
    for i,chunk in enumerate(chunks):
        assert len(chunk) <= 500
        console.print(f"Chunk({i}):[yellow italic]{len(chunk)}[/]")
        console.print(chunk)
        total += len(chunk)
    console.print(f"Length of text size: [yellow italic]{len(sample_text)}[/]")
    console.print(f"Total sum of chunk size: [yellow italic]{total}[/]")
    
if __name__ == "__main__":
    print("Original Text")
    print(sample_text)
    test_split_text_with_overlap()