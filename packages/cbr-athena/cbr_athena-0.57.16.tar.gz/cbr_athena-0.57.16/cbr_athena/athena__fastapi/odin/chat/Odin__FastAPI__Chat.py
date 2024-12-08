from cbr_athena.athena__fastapi.odin.Odin__FastAPI             import Odin__FastAPI
from cbr_athena.athena__fastapi.odin.chat.routes.Routes__LLMs  import Routes__LLMs, FAST_API_ROUTES__ODIN__CHAT__LLMS

FAST_API_ROUTES__ODIN__CHAT = FAST_API_ROUTES__ODIN__CHAT__LLMS

class Odin__FastAPI__Chat(Odin__FastAPI):

    base_path :str = '/odin/chat'
    title     :str = 'The Cyber Boardroom - Odin Chat'

    def __init__(self):
        super().__init__()
        self.routes = [Routes__LLMs]

