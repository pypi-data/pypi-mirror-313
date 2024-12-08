from cbr_athena.aws.dynamo_db.DyDB__CBR_Logging                 import DYNAMO_DB__TABLE___REGION_NAME
from cbr_athena.schemas.CBR_Request                             import CBR_Request
from cbr_athena.config.CBR__Config__Athena                      import cbr_config_athena
from cbr_athena.utils.Utils                                     import Utils
from osbot_aws.apis.Session                                     import Session
from osbot_aws.aws.dynamo_db.domains.DyDB__Table_With_Timestamp import DyDB__Table_With_Timestamp
from osbot_aws.testing.TestCase__Dynamo_DB__Local               import URL_DOCKER__DYNAMODB__LOCAL
from osbot_utils.decorators.methods.cache_on_self               import cache_on_self
from osbot_utils.utils.Dev                                      import pprint
from osbot_utils.utils.Misc                                     import date_time_now

DYNAMO_DB__TABLE_NAME__CBR_REQUESTS = 'arn:aws:dynamodb:eu-west-2:470426667096:table/{env}__cbr_requests'       # todo: refactor so that the region_name and account_id are not hardcoded
TABLE_CBR_REQUESTS__INDEXES_NAMES   = [ 'date'      , 'ip_address', 'host'      , 'level'      , 'method'     ,
                                        'path'      , 'referer'   , 'req_id'    , 'session_id' , 'status_code',
                                        'source'    , 'user'      , 'user_role' , 'user_status'               ]


class DyDB__CBR_Requests(DyDB__Table_With_Timestamp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table_name            = DYNAMO_DB__TABLE_NAME__CBR_REQUESTS.format(env=Utils.current_execution_env())
        self.table_indexes         = TABLE_CBR_REQUESTS__INDEXES_NAMES
        self.dynamo_db.region_name = DYNAMO_DB__TABLE___REGION_NAME            # todo: find better way to handle the target region of the CBR tables
    #     self.dynamo_db.client = self.cbr_client
    #
    # @cache_on_self
    # def cbr_client(self):
    #     return Session().client('dynamodb', region_name=DYNAMO_DB__TABLE___REGION_NAME)


    def log_request(self, cbr_request: CBR_Request):
        if cbr_config_athena.aws_disabled():
            return None
        if type(cbr_request) is not CBR_Request:            # only allow cbr_request
            return
        document = cbr_request.json()
        return self.add_document(document)

    def log_request_response(self, request, response, duration):
        if cbr_config_athena.aws_disabled():
            return None
        try:
            headers     = {key: value for key, value in request.headers.items()}        # todo: see if we shouldn't be changing all headers names to lower case
            cbr_request = CBR_Request()
            # indexes
            cbr_request.date        = date_time_now(date_time_format='%Y-%m-%d')
            cbr_request.host        = headers.get('host')
            cbr_request.ip_address  = request.client.host
            cbr_request.level       = 'DEBUG'
            cbr_request.method      = request.method
            cbr_request.path        = request.url.path
            cbr_request.source      = 'odin'
            cbr_request.status_code = str(response.status_code)
            cbr_request.city        = headers.get('cloudfront-viewer-city'        , '')
            cbr_request.country     = headers.get('cloudfront-viewer-country-name', '')

            # other
            cbr_request.duration    = duration
            cbr_request.headers     = headers
            cbr_request.query       = dict(request.query_params)

            document = cbr_request.json()
            self.add_document(document)

        except Exception as e:
            pprint(e)               # todo: add to logging



    # def log_message(self, message):
    #     #if self.enabled:
    #         stack           = inspect.stack()
    #         caller_frame    = stack[1]
    #         caller_module   = inspect.getmodule(caller_frame[0])
    #         module_name     = caller_module.__name__ if caller_module else "Unknown module"
    #         function_name   = caller_frame.function
    #
    #         log_entry = dict(source        = 'code'         ,
    #                          module_name   = module_name    ,
    #                          function_name = function_name  ,
    #                          message       = message        )
    #         extra_gsi_data = dict(data_class = str(type(log_entry)),
    #                               level      = 'DEBUG'      ,
    #                               source     = 'log_message',
    #                               topic      = 'Message'    ,
    #                               user       = 'Athena'     )
    #         return self.add_document(data=log_entry,extra_gsi_data=extra_gsi_data)

dydb_cbr_requests = DyDB__CBR_Requests()