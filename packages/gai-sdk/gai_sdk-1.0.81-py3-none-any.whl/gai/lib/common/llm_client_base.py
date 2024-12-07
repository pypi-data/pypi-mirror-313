from gai.lib.common.utils import get_gai_config, get_gai_url

class LLMClientBase:

    def __init__(self, category_name, config_path=None):
        self.config = get_gai_config(file_path=config_path)
        self.url = self._get_gai_url(category_name)
