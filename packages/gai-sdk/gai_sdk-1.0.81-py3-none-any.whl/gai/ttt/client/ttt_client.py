from gai.lib.common.generators_utils import chat_string_to_list
from gai.lib.common.logging import getLogger
logger = getLogger(__name__)

import os
from gai.lib.common.utils import get_gai_config, get_gai_url
from dotenv import load_dotenv
load_dotenv()
from gai.ttt.client.completions import Completions

class TTTClient:

    # config is either a string path or a component config
    def __init__(self, config=None):
        if config is str or config is None:
            self.config=get_gai_config(file_path=config)
            self.config = self.config["clients"]["gai-ttt"]
            self.url = get_gai_url("ttt")
        else:
            self.config = config
            self.url = config["url"]
            # override the environment variable for Completion to use
            os.environ["TTT_URL"] = self.url

        from openai import OpenAI
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
        self.client = Completions.PatchOpenAI(client, override_url=self.url)

    def __call__(self, 
                 messages:str|list, 
                 stream:bool=True, 
                 max_tokens:int=None, 
                 temperature:float=None, 
                 top_p:float=None, 
                 top_k:float=None,
                 json_schema:dict=None,
                 tools:list=None,
                 tool_choice:str=None,
                 stop_conditions:list=None,
                 timeout:float=None,
                 model:str="exllamav2-mistral7b"
                 ):

        if isinstance(messages, str):
            messages = chat_string_to_list(messages)

        if not max_tokens and self.config.get("max_tokens",None):
            max_tokens = self.config["max_tokens"]

        if not temperature and self.config.get("temperature",None):
            temperature = self.config["temperature"]

        if not top_p and self.config.get("top_p",None):
            top_p = self.config["top_p"]

        if not top_k and self.config.get("top_k",None):
            top_k = self.config["top_k"]

        if not stop_conditions and self.config.get("stop_conditions",None):
            stop_conditions = self.config["stop_conditions"]

        response = self.client.chat.completions.create(model=model,
                    messages=messages,
                    stream=stream,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    top_k=top_k,
                    json_schema=json_schema,
                    tools=tools,
                    tool_choice=tool_choice,
                    stop_conditions=stop_conditions,
                    timeout=timeout)
        if stream:
            def streamer():
                for chunk in response:
                    yield chunk
            return streamer()
        return response

