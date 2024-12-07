from gai.lib.tools.scraper import Scraper
scraper=Scraper()
import os
from openai import OpenAI
from rich.console import Console
console=Console()

# Initialize TTT Client
if not os.environ.get("OPENAI_API_KEY",None):
    os.environ["OPENAI_API_KEY"]=""
client=OpenAI()
from gai.ttt.client.completions import Completions
client=Completions.PatchOpenAI(client)

def news(url="https://asiaone.com",category=None):

    if category == "world":
        url="https://www.bbc.com/news/world"
    if category == "local":
        url="https://asiaone.com"

    content=""
    with console.status("Working...",spinner="monkey") as status:
        result, links = scraper.scrape(url)
        inner_messages=[]
        inner_messages.append({"role":"user","content":f"scrape {url}"})
        inner_messages.append({"role":"assistant","content":result})
        inner_messages.append({"role":"user","content":"Remove meaningless sentences from the above result and organise them into coherent paragraphs. Excluding marketing information about the news portal."})
        inner_messages.append({"role":"assistant","content":""})
        #
        response=client.chat.completions.create(
            model="exllamav2-mistral7b",
            messages=inner_messages,
            stream=True,
            max_tokens=1000,
            stopping_conditions=[""]
            )
        for chunk in response:
            # Stop the spinner on the first iteration
            if 'status' in locals():
                status.stop()
                del status                
            chunk = chunk.extract()
            if chunk and isinstance(chunk, str):
                
                # Skip empty chunks
                if content is None and chunk==" ":
                    continue

                content += chunk
                console.print(f"[italic bright_white]{chunk}[/]",end="")
        print()
        inner_messages.append({"role": "assistant", "content": content})
        return inner_messages