from gai.lib.common.http_utils import http_post
from gai.lib.common.image_utils import base64_to_imageurl
from gai.lib.common.generators_utils import chat_string_to_list

from gai.lib.common.utils import get_gai_config, get_gai_url
from gai.lib.common.logging import getLogger
logger = getLogger(__name__)

from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
import json

class ITTClient:

    # config is either a string path or a component config
    def __init__(self, config=None):
        if config is str or config is None:
            self.config=get_gai_config(file_path=config)
            self.config = self.config["clients"]["gai-ttt"]
            self.url = get_gai_url("ttt")
        else:
            self.config = config
            self.url = config["url"]
                

    def __call__(self, 
                 messages:list, 
                 stream:bool=True,
                 max_new_tokens:int=None, 
                 max_tokens:int=None, 
                 temperature:float=None, 
                 top_p:float=None, 
                 top_k:float=None,
                 ):

        if not messages:
            raise Exception("Messages not provided")

        data = {
            "messages": messages,
            "stream": stream,
            "max_new_tokens": max_new_tokens,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k
        }

        response = http_post(get_gai_url("itt"), data)

        if stream:
            def streamer():
                for chunk in response.iter_lines():
                    chunk = chunk.decode("utf-8")
                    if type(chunk)==str:
                        yield ChatCompletionChunk(**json.loads(chunk))

                # for chunk in response:
                #     yield chunk
            return streamer()
        
        jsoned = response.json()
        completion = ChatCompletion(**jsoned)
        return completion

    # def openai_vision(self, messages=None, stream=True, **generator_params):
    #     import os
    #     import openai
    #     from openai import OpenAI
    #     from dotenv import load_dotenv
    #     load_dotenv()
    #     if not os.environ.get("OPENAI_API_KEY"):
    #         raise Exception(
    #             "OPENAI_API_KEY not found in environment variables")
    #     openai.api_key = os.environ["OPENAI_API_KEY"]
    #     client = OpenAI()

    #     if not messages:
    #         raise Exception("Messages not provided")

    #     def streamer(response):
    #         for chunk in response:
    #             yield OpenAIChunkWrapper(chunk)

    #     model = "gpt-4-vision-preview"
    #     if isinstance(messages, str):
    #         messages = chat_string_to_list(messages)

    #     response = client.chat.completions.create(
    #         model=model,
    #         messages=messages,
    #         stream=stream,
    #         **generator_params
    #     )

    #     if not stream:
    #         response.decode = lambda: response.choices[0].message.content
    #         return response
    #     return streamer(response)
