from osbot_fast_api.api.Fast_API                                    import Fast_API
from osbot_utils.decorators.methods.cache_on_self                   import cache_on_self
#

class FastAPI_Athena(Fast_API):

    def __enter__(self                           ): return self
    def __exit__ (self, exc_type, exc_val, exc_tb): return

    # @cache_on_self
    # def app(self):
    #     return FastAPI()

    def router(self):
        return self.app().router

    def setup(self):
        self.setup_routes()
        return self

    def add_middlewares(self, app):
        from cbr_athena.athena__fastapi.middleware.add_logging import Middleware_Logging
        app.add_middleware(Middleware_Logging)
    #     if os.getenv('ENVIRONMENT') == 'Dev':
    #         app.add_middleware(
    #             CORSMiddleware,
    #             allow_origins    = ["*"],  # Allows all origins
    #             allow_credentials= True ,
    #             allow_methods    = ["*"],  # Allows all methods
    #             allow_headers    = ["*"],  # Allows all headers
    #         )
    #

    def setup_routes(self):
        from cbr_athena.athena__fastapi.routes.Routes__Config   import Routes__Config
        from cbr_athena.athena__fastapi.routes.Routes__Dev      import Routes__Dev
        from cbr_athena.athena__fastapi.routes.Routes__Logging  import Routes__Logging
        from cbr_athena.athena__fastapi.routes.Routes__Ollama   import Routes__Ollama
        from cbr_athena.athena__fastapi.routes.Routes__OpenAI   import Routes__OpenAI


        self.router().get("/")(self.redirect_to_docs)
        app = self.app()

        self.add_middlewares(app)
        self.add_routes (Routes__Config)
        Routes__Dev     ().setup(app)           # todo: refactor these out into the new Fast_API structure
        Routes__Logging ().setup(app)
        Routes__OpenAI  ().setup(app)
        Routes__Ollama  ().setup(app)

        self.mount__fast_apis()

    def mount__fast_apis(self):
        self.odin__fastAPI__api    ().setup().mount(self.app())
        self.odin__fastAPI__chat   ().setup().mount(self.app())
        self.llms__fast_api        ().setup().mount(self.app())
        self.user_data__fast_api   ().setup().mount(self.app())
        self.user_session__fast_api().setup().mount(self.app())
        pass

    @cache_on_self
    def odin__fastAPI__api(self):
        from cbr_athena.athena__fastapi.odin.api.Odin__FastAPI__API import Odin__FastAPI__API
        return Odin__FastAPI__API()

    @cache_on_self
    def odin__fastAPI__chat(self):
        from cbr_athena.athena__fastapi.odin.chat.Odin__FastAPI__Chat import Odin__FastAPI__Chat
        return Odin__FastAPI__Chat()

    @cache_on_self
    def user_data__fast_api(self):
        from cbr_user_data.fast_api.User_Data__Fast_API import User_Data__Fast_API
        return User_Data__Fast_API()

    @cache_on_self
    def user_session__fast_api(self):
        from cbr_user_session.fast_api.User_Session__Fast_API import User_Session__Fast_API
        return User_Session__Fast_API()

    @cache_on_self
    def llms__fast_api(self):
        from cbr_athena.athena__fastapi.llms.LLMs__Fast_API import LLMs__Fast_API
        return LLMs__Fast_API()

    # def setup_middleware(self):
    #     if Utils.current_execution_env() == 'LOCAL':
    #         # Configure CORS for local server manually since this is done automatically by AWS Lambda
    #         self.app().add_middleware(CORSMiddleware,
    #                                   allow_origins     = ["*"]                         ,
    #                                   allow_credentials = True                          ,
    #                                   allow_methods     = ["GET", "POST", "HEAD"]       ,
    #                                   allow_headers     = ["Content-Type", "X-Requested-With", "Origin", "Accept", "Authorization"],
    #                                   expose_headers    = ["Content-Type", "X-Requested-With", "Origin", "Accept", "Authorization"])

    def run_in_lambda(self):
        import uvicorn                      # moved here for performance reasons
        lambda_host = '127.0.0.1'
        lambda_port = 8080
        self.setup()
        kwargs = dict(app  =  self.app(),
                      host = lambda_host,
                      port = lambda_port)
        uvicorn.run(**kwargs)

    # default routes
    async def redirect_to_docs(self):
        from starlette.responses import RedirectResponse
        return RedirectResponse(url="/docs")
