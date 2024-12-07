import json,os
from gai.lib.common.http_utils import http_post
from gai.lib.common.generators_utils import chat_string_to_list
from gai.lib.common.errors import ApiException
from gai.lib.common.logging import getLogger
logger = getLogger(__name__)
from gai.lib.common.utils import get_gai_config

from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk

# This class is used by the monkey patch to override the openai's chat.completions.create() function.
# This is also the class responsible for for GAI's text-to-text completion.
# The main driver is the create() function that can be used to generate or stream completions as JSON output.
# The output from create() should be indisguishable from the output of openai's chat.completions.create() function.
#
# Example:
# from openai import OpenAI
# client = OpenAI()
# from gai.ttt.client.completions import Completions
# client = Completions.PatchOpenAI(client)
# client.chat.completions.create(model="exllamav2-mistral7b",messages=[{"role":"user","content":"Tell me a one sentence story"}])

class Completions:

    def __init__(self):
        self.output = None

    @staticmethod
    def PatchOpenAI(openai_client, override_url=None):

        # We use "override_url" when Completions class is called by TTTClient directly instead of getting the URL from environment or config file.
        # This is useful when we want to test the completions locally.
        openai_client.override_url = override_url

        openai_create = openai_client.chat.completions.create

        """
        This is a convenient function for extracting the content of the response object.
        Example:
        - For generation.
        use `response.extract()` instead of using `response.choices[0].message.content`.
        - For stream.
            for chunk in response:
                if chunk:
                    chunk.extract()
        """
        def attach_extractor(response,is_stream):

            if not is_stream:
                # return message content
                if response.choices[0].message.content:
                    response.extract = lambda: {
                        "type":"content",
                        "content": response.choices[0].message.content
                    }
                    return response
                # return message toolcall
                if response.choices[0].message.tool_calls:
                    response.extract = lambda: {
                        "type":"function",
                        "name": response.choices[0].message.tool_calls[0].function.name,
                        "arguments": response.choices[0].message.tool_calls[0].function.arguments
                    }
                    return response
                raise Exception("completions.attach_extractor: Response is neither content nor toolcall. Please verify the API response.")
            
            def streamer():

                for chunk in response:

                    if chunk.choices[0].delta.content or chunk.choices[0].delta.role:
                        chunk.extract = lambda: chunk.choices[0].delta.content

                    if chunk.choices[0].delta.tool_calls:

                        if chunk.choices[0].delta.tool_calls[0].function.name:
                            chunk.extract = lambda: {
                                "type":"function",
                                "name": chunk.choices[0].delta.tool_calls[0].function.name,
                            }

                        if chunk.choices[0].delta.tool_calls[0].function.arguments:
                            chunk.extract = lambda: {
                                "type":"function",
                                "arguments": chunk.choices[0].delta.tool_calls[0].function.arguments,
                            }

                    if chunk.choices[0].finish_reason:
                        chunk.extract = lambda: {
                            "type":"finish_reason",
                            "finish_reason": chunk.choices[0].finish_reason
                        }

                    if not chunk.extract:
                        raise Exception(f"completions.streamer: Chunk response contains unexpected data that cannot be processed. chunk: {chunk.__dict__}")
                    yield chunk

            return (chunk for chunk in streamer())

        # Replace openai.completions.create with patched_create depending on the model specified
        def patched_create(**kwargs):
            model = kwargs.get("model", None)

            if not model:
                raise Exception("completions.patched_create: Model not provided")
            
            if model=="exllamav2-mistral7b":
                # call locally

                # "messages": required
                messages=kwargs.get("messages")

                # "stream"
                stream=kwargs.get("stream",None)

                # "tools": array of tool call objects
                tools=kwargs.get("tools",None)

                # "max_tokens": 
                max_tokens=kwargs.pop("max_tokens",None)

                # "temperature"
                temperature=kwargs.get("temperature",None)

                # "top_p"
                top_p=kwargs.get("top_p",None)

                # "top_k"
                top_k=kwargs.get("top_k",None)

                # "json_schema"
                json_schema=kwargs.get("json_schema",None)

                # "tool_choice"
                tool_choice=kwargs.get("tool_choice","auto")

                # "stop_conditions"
                stop_conditions=kwargs.get("stop_conditions",None)

                # "timeout"
                timeout=kwargs.get("timeout",30.0)

                # By default, the URL is taken from the config file if the Completion class is used as a library
                if os.environ.get("TTT_URL",False):
                    url = os.environ["TTT_URL"]
                else:
                    url = get_gai_config()["clients"]["gai-ttt"]["url"]

                # "self" refers to the patched client.
                # And if it contains override_url, that means the Completion Class is not used directly but is called via TTTClient with a custom URL, probably for testing.
                if override_url:
                    url = override_url    

                response = Completions()._create(
                    url=url,
                    messages=messages, 
                    stream=stream, 
                    tools=tools, 
                    max_tokens = max_tokens,
                    temperature=temperature, 
                    top_p=top_p, 
                    top_k=top_k, 
                    json_schema=json_schema, 
                    tool_choice=tool_choice,
                    stop_conditions=stop_conditions,
                    timeout=timeout)
                
                response = attach_extractor(response,stream)
            else:
                # fallback to openai's completions.create
                stream=kwargs.get("stream",False)
                response = openai_create(**kwargs)
                response = attach_extractor(response,stream)

            return response


        openai_client.chat.completions.create = patched_create    
        return openai_client    

    # Generate non stream dictionary response for easier unit testing
    def _generate_dict(self, **kwargs):
        response=None
        url = kwargs.pop("url")
        timeout = kwargs.pop("timeout",30.0)
        try:
            response = http_post(url, data={**kwargs},timeout=timeout)
            jsoned=response.json()
            completion = ChatCompletion(**jsoned)
        except ApiException as he:
                raise he
        except Exception as e:
            logger.error(f"completions._generate_dict: error={e} response={response}")
            raise e

        return completion

    # Generate streamed dictionary response for easier unit testing
    def _stream_dict(self, **kwargs):
        response=None
        url = kwargs.pop("url")
        timeout = kwargs.pop("timeout",30.0)
        try:
            response = http_post(url, data={**kwargs},timeout=timeout)
        except ApiException as he:
                raise he
        except Exception as e:
            logger.error(f"completions._stream_dict: error={e}")
            raise e

        for chunk in response.iter_lines():
            try:
                chunk = chunk.decode("utf-8")
                if type(chunk)==str:
                    yield ChatCompletionChunk(**json.loads(chunk))
            except Exception as e:
                # Report the error and continue
                logger.error(f"completions._stream_dict: error={e}")
                pass


    """
    Description:
    This function is a monkey patch for openai's chat.completions.create() function.
    It will override the default completions.create() function to call the local llm instead of gpt-4.
    Example:
    openai_client.chat.completions.create = create
    """
    def _create(self, url:str, messages:list, stream:bool, max_tokens:int, temperature:float=None, top_p:float=None, top_k:float=None, json_schema:dict=None, tools:list=None, tool_choice:str=None, stop_conditions:list=None,timeout:float=30.0):

        # Prepare messages
        if not messages:
            raise Exception("Messages not provided")
        if isinstance(messages, str):
            messages = chat_string_to_list(messages)
        if messages[-1]["role"] != "assistant":
            messages.append({"role": "assistant", "content": ""})

        # Prepare payload
        kwargs = {
            "url": url,
            "messages": messages,
            "stream": stream,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "json_schema": json_schema,
            "tools": tools,
            "tool_choice": tool_choice,
            "stop_conditions": stop_conditions,
            "timeout":timeout
        }
        if not stream:
            response = self._generate_dict(**kwargs)
            return response
        return (chunk for chunk in self._stream_dict(**kwargs))


