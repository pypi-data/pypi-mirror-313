from os                                             import getenv
from unittest                                       import TestCase
from fastapi                                        import FastAPI
from starlette.testclient                           import TestClient
from cbr_athena.athena__fastapi.odin.Odin__FastAPI  import Odin__FastAPI
from osbot_utils.utils.Env import load_dotenv


class TestCase__Odin__FastAPI(TestCase):
    odin_fast_api_class : type
    odin_fast_api       : Odin__FastAPI
    app                 : FastAPI
    client              : TestClient
    api_key             : str

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.odin_fast_api = cls.odin_fast_api_class().setup()
        cls.app           = cls.odin_fast_api.app()
        cls.client        = TestClient(cls.app)
        cls.api_key       = getenv('ODIN_AUTH_TOKEN')
        cls.client.headers.update({'Authorization': cls.api_key})