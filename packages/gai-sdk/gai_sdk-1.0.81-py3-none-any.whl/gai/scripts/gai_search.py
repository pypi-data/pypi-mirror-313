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

def search(search_term,max_results):
    results = googler.google(search_term)
    inner_messages=[]
    inner_messages.append({ "role":"user", "content":f"gg {search_term}"})
    inner_messages.append({ "role":"assistant", "content":results})
    
    n_results = 0
    summaries = []
    for result in results:
        if n_results > max_results:
            break
        try:
            # Summarize the page
            console.print(f"[yellow]Scraping {result['url']}...[/]")
            content, links = scraper.scrape(result["url"])
            messages= [
                    {"role": "system", "content": """You are an expert in summarizing <content> provided by the user that is scraped from the web and convert into point form summaries.
                    Follow this steps:
                    1) Ignore non-relevant, advertisements contents as well as content that describes the website instead of relevant to the user's query. 
                    2) Proofread and summarise the content relevant to the user's search.
                    3) Present the summary in point form."""},
                    {"role": "user",
                        "content": f"Summarize this <content>{content}</content>"},
                    {"role": "assistant", "content": ""},
                ]
            console.print(f"[yellow]Summarizing {result['url']}...[/]")
            summaries.append( client.chat.completions.create(model="exllamav2-mistral7b",messages=messages,stream=False).extract() )
            n_results += 1
        except:
            continue        
    
    # Summarize the summaries
    messages=[
        {"role": "user", "content": f"Extact, proofread and summarize <content>{str(summaries)}</content> that is relevant to {search_term} into point forms."},
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
