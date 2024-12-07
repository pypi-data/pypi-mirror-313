from gai.lib.common import file_utils
import os,sys

"""
file_utils.split_text(): This function uses TextSplitter class internally.
TextSplitter class: This function is lifted from langchain's RecursiveCharacterTextSplitter class.
"""

from rich.console import Console
console=Console()

sample_text = ""
here=os.path.dirname(os.path.realpath(__file__))
path=sys.path
with open(os.path.join(here,"./pm_long_speech_2023.txt")) as f:
    sample_text = f.read()

def test_split_text():
    chunk_size = 500
    chunk_overlap = 50
    chunk_names = file_utils.split_text(
        text=sample_text,
        sub_dir=None,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap)
    console.print("[yellow italic]Chunks[/]")
    for i,chunk in enumerate(chunk_names):
        console.print(f"Chunk({i}):[yellow italic]{chunk}[/]")
    
if __name__ == "__main__":
    print("Original Text")
    print(sample_text)
    test_split_text()