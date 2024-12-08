from cbr_athena.athena__fastapi.routes.Fast_API_Route   import Fast_API__Routes
from cbr_athena.schemas.for_fastapi.Log_Entry   import Log_Entry
from cbr_athena.utils.Logging                   import Logging


class Routes__Logging(Fast_API__Routes):
    logging     : Logging
    path_prefix : str = "logging"

    def add_routes(self):

        @self.router.post('/add_log_entry')
        async def add_log_entry(log_entry: Log_Entry):
            return self.logging.add_log_entry(log_entry)


