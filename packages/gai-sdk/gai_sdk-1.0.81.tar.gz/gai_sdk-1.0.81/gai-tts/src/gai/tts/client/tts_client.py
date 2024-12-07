from gai.lib.common.http_utils import http_post
from gai.lib.common.logging import getLogger
logger = getLogger(__name__)
from gai.lib.common.utils import get_gai_config, get_gai_url

class TTSClient:

    def __init__(self,config=None):
        if config is str or config is None:
            self.config=get_gai_config(file_path=config)
            self.config = self.config["clients"]["gai-tts"]
            self.base_url = get_gai_url("tts")
        else:
            self.config = config
            self.base_url = config["url"]        

    def __call__(self, input, stream=True, voice=None, language=None):
        data = {
            "input": input,
            "stream": stream,
            "voice": voice,
            "language": language
        }
        response = http_post(self.base_url, data)
        return response


