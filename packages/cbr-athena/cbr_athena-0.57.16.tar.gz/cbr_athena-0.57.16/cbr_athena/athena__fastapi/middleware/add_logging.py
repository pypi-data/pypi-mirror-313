import time
from decimal import Decimal

from fastapi                                     import Request
from starlette.responses                         import Response
from starlette.middleware.base                   import BaseHTTPMiddleware
from starlette.middleware.base                   import RequestResponseEndpoint
from cbr_athena.aws.dynamo_db.DyDB__CBR_Requests import dydb_cbr_requests


class Middleware_Logging(BaseHTTPMiddleware):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.cbr_requests = DyDB__CBR_Requests()
        #self.cbr_requests.log_message('Middleware_Logging object was created')

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = Decimal(time.time())
        response   = await call_next(request)
        end_time   = Decimal(time.time())
        duration   = end_time - start_time
        duration   = duration.quantize(Decimal('0.001'))

        dydb_cbr_requests.log_request_response(request=request, response=response, duration=duration)
        #from cbr_website_beta.config.CBR_Config import cbr_config  # todo: find a way to access this cbr_config.aws_enabled() config mapping
        #if cbr_config.aws_enabled():
        #

        return response


# from pydantic import BaseModel, Field
# from typing import Dict, Any
#
# class RequestData(BaseModel):
#     method: str
#     path: str
#     query: Dict[str, Any]
#     client_ip: str
#     headers: Dict[str, str]
#     timestamp: int
#
# class ResponseData(BaseModel):
#     status_code: int
#     duration: str
#
# class LogDocument(BaseModel):
#     request_data: RequestData
#     response_data: ResponseData