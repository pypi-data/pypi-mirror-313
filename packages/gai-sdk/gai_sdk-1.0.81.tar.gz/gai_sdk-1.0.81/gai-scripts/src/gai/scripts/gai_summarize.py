import os
from openai import OpenAI
from rich.console import Console
console=Console()

from gai.lib.tools.googler import Googler
googler = Googler()

from gai.lib.tools.scraper import Scraper
scraper=Scraper()

# Initialize TTT Client
if not os.environ.get("OPENAI_API_KEY",None):
    os.environ["OPENAI_API_KEY"]=""
client=OpenAI()
from gai.ttt.client.completions import Completions
client=Completions.PatchOpenAI(client)

def summarize(file_path):
    # Read the file
    with open(file_path, "r") as file:
        text = file.read()

    inner_messages=[]
    inner_messages.append({ "role":"user", "content":f"summarize {file_path}"})

    # Summarize the summaries
    messages=[
        {"role": "user", "content": f"Extact, proofread and summarize <content>{str(text)}</content> into point forms."},
        {"role": "assistant", "content": ""},
    ]
    content=""
    for chunk in client.chat.completions.create(model="exllamav2-mistral7b",messages=messages):
        chunk = chunk.extract()
        if (chunk) and type(chunk)==str:            
            content+=chunk
            console.print(f"[italic bright_white]{chunk}[/]",end="")

    print()
    inner_messages.append({ "role":"assistant", "content":content})
    return inner_messages
