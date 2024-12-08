from enum import Enum
from os import getenv
from urllib.parse import urljoin

import requests

from cbr_athena.llms.providers.LLM__Chat_Completion import LLM__Chat_Completion
from osbot_utils.utils.Dev import pprint

ENV_KEY__OLLAMA__SERVER = 'OLLAMA__SERVER'                  # todo: add support for defining the IP and port and schema of the ollama server
LLM_BASE_URL__OLLAMA = "http://localhost:11434"

class LLM__Models__OLLAMA(str, Enum):
    LLAMA3    = 'llama3'
    PHI3      = "phi3"
    GEMMA_2B  = "gemma"



class LLM__Ollama(LLM__Chat_Completion):
    model    : str = LLM__Models__OLLAMA.GEMMA_2B
    base_url : str =  LLM_BASE_URL__OLLAMA

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def api_generate(self, prompt, model="llama3", stream=False, format=None):
        path      = 'api/generate'
        json_data = { 'model'  :  model,
                      'prompt' : prompt   ,
                      'stream' : stream   ,
                      "options": {
                          "seed"          : 42,
                          "temperature"   : 0 }}
        if format:
            json_data['format'] = format
        return self.post_request(path, json_data, stream=stream)

    def model_details(self, model_name):
        return self.post_request('/api/show', { 'name' : model_name })

    def models(self):
        return self.get_request('/api/tags').get('models')

    # def post_request(self, path, json_data):
    #     url       = urljoin(self.base_url, path)
    #     headers   = {"Content-Type": "application/json"}
    #     post_data = dict(url=url, headers=headers, json=json_data)
    #     return self.make_request(post_data)

    def post_request(self, path, json_data, stream=False):
        url = urljoin(self.base_url, path)
        headers = {"Content-Type": "application/json"}
        if stream:
            return self.post_request__stream(url, headers, json_data)
        response = requests.post(url, headers=headers, json=json_data, stream=stream)
        return response.json()

    def post_request__stream(self, url, headers, json_data):
        with requests.post(url, headers=headers, json=json_data, stream=True) as response:
            for line in response.iter_lines():
                if line:
                    yield line.decode('utf-8')
    def get_request(self, path='/'):
        url = urljoin(self.base_url, path)
        response = requests.get(url)
        if response.headers['Content-Type'] == 'text/plain; charset=utf-8':
            return response.text
        return response.json()

    def post_data(self):
        post_data = super().post_data()
        post_data['url'] += '/api/chat'
        post_data['json']['stream'] = False
        return post_data