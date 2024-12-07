import pytest, json, os
from unittest.mock import patch, MagicMock
from gai.ttt.client.ttt_client import TTTClient
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk

# Test Generation

def get_mock_json(file_name):
    with open(os.path.join(os.path.dirname(__file__),"mock", file_name)) as f:
        return json.load(f)

def test_ttt_client_generation():

    client = TTTClient({
        "type": "ttt",
        "url": "http://localhost:12031/gen/v1/chat/completions"
    })

    # Mock exllamav2 model output
    client.client = MagicMock()
    mock_response=get_mock_json("2a_generate_text_gai.json")
    client.client.chat.completions.create.return_value = ChatCompletion(**mock_response)
    
    # Act
    response=client(messages=[{"role":"user","content":"hello"},{"role":"assistant","content":""}],stream=False)

    # Assert
    assert response.choices[0].finish_reason == "stop"
    assert response.choices[0].message.content == "Under a tree, a little boy shared his last bread with a hungry crow. They became friends, teaching him that kindness can feed more than just Hunger."

# Test Streaming

def get_mock_stream(file_name):
    # Simulating a stream of responses
    responses=[]
    with open(os.path.join(os.path.dirname(__file__),"mock", file_name)) as f:
        responses=json.load(f)
        for response in responses:
            yield ChatCompletionChunk(**response)

def test_ttt_client_streaming():

    client = TTTClient({
        "type": "ttt",
        "url": "http://localhost:12031/gen/v1/chat/completions"
    })


    # Mock exllamav2 model output
    client.client = MagicMock()
    mock_stream=get_mock_stream("1b_stream_text_openai.json")
    client.client.chat.completions.create.return_value = (chunk for chunk in mock_stream)
    
    # Act
    response=client(messages=[{"role":"user","content":"hello"},{"role":"assistant","content":""}],stream=True)
    content=""
    for chunk in response:
        if chunk.choices[0].delta.content:
            content+=chunk.choices[0].delta.content
    assert content=='"Once upon a time, a tiny, curious frog set on a journey to reach the top of the mountain, and against all odds, found a kingdom of thriving frogs living beautifully above the clouds."'

if __name__ == "__main__":
    test_ttt_client_streaming()    
