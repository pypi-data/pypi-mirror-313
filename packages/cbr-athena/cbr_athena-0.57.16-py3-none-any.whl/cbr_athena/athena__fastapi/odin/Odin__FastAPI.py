from fastapi                                        import FastAPI
from osbot_utils.base_classes.Type_Safe             import Type_Safe
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self

FAST_API_ROUTES__ODIN__DEFAULT = ['/openapi.json'          ,
                                  '/docs'                  ,
                                  '/docs/oauth2-redirect'  ,
                                  '/redoc'                 ]

class Odin__FastAPI(Type_Safe):
    base_path : str = '/odin'
    title     : str = 'The Cyber Boardroom - Odin'
    routes    : list

    @cache_on_self
    def app(self):
        return FastAPI(title=self.title)

    def mount(self, parent_app):
        parent_app.mount(self.base_path, self.app())

    def routes__paths(self):
        return [route.path for route in self.app().routes]

    def setup(self):
        app  = self.app()

        for route in self.routes:
            route().setup(app)
        return self