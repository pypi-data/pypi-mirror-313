from os import getenv

import requests

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Env import get_env

from cbr_athena.llms.providers.LLM__Chat_Completion import LLM__Chat_Completion

ENV_NAME__GROQ_API_KEY = 'GROQ_API_KEY'
LLM_BASE_URL__GROQ     = 'https://api.groq.com/openai/v1/chat/completions'

class LLM__Groq(LLM__Chat_Completion):

    def __init__(self) -> None:
        self.api_key  = getenv(ENV_NAME__GROQ_API_KEY)
        self.base_url = LLM_BASE_URL__GROQ
        super().__init__()

