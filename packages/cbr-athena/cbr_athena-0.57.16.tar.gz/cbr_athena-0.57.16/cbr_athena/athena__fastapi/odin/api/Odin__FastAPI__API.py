from cbr_athena.athena__fastapi.odin.Odin__FastAPI                  import Odin__FastAPI
from cbr_athena.athena__fastapi.odin.api.routes.Routes__Odin__Info  import Routes__Odin__Info
from cbr_athena.athena__fastapi.odin.api.routes.Routes__Security    import Routes__Security
from cbr_athena.llms.LLMs_API                                       import LLMs_API

FAST_API_ROUTES__ODIN__API = ['/llms-api.json']

class Odin__FastAPI__API(Odin__FastAPI):
    base_path :str = '/odin/api'
    title     :str = 'The Cyber Boardroom - Odin API'

    def __init__(self):
        super().__init__()
        self.llms_api = LLMs_API()
        self.routes   = [Routes__Odin__Info ,
                         Routes__Security   ]

    def add_root_routes(self):
        app = self.app()

        @app.get('/llms-api.json', include_in_schema=True, summary="Detailed list of methods available to Odin to call")
        def llms_api_json():
            return self.llms_api.create_from_fastapi_routes(self.app())

    def setup(self):
        super().setup()
        self.add_root_routes()
        return self
