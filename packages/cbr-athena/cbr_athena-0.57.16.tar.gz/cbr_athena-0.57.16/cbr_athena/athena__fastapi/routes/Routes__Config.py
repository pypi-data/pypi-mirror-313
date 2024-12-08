from cbr_athena.config.CBR__Config__Athena              import cbr_config_athena
from cbr_athena.utils.Version                           import Version
from osbot_fast_api.api.Fast_API_Routes                 import Fast_API_Routes

ROUTES_PATHS__CONFIG = ['/cbr_config_athena', '/version']

class Routes__Config(Fast_API_Routes):
    tag: str = "config"

    def version(self):
        return {"version": Version().version()}

    def cbr_config_athena(self):
        return cbr_config_athena.cbr_config_athena()

    def setup_routes(self):
        self.router.get("/cbr_config_athena")(self.cbr_config_athena)
        self.router.get("/version"          )(self.version)
        return self