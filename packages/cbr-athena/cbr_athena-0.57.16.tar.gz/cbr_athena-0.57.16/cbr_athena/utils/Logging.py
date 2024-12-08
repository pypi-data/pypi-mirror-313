from decimal import Decimal

from cbr_athena.aws.dynamo_db.DyDB__CBR_Logging     import dydb_cbr_logging
from cbr_athena.schemas.CBR_Logging                 import CBR_Logging
from cbr_athena.schemas.for_fastapi.Log_Entry       import Log_Entry
from osbot_utils.utils.Misc                         import is_guid


class Logging:
    # def __init__(self):
    #     self.dydb_cbr_logging = DyDB__CBR_Logging()


    def add_log_entry(self, log_entry: Log_Entry):
        document_id = dydb_cbr_logging.add_log_entry(log_entry)
        if is_guid(document_id):
            return {'status':'ok', 'data': 'data logged ok', 'document_id': document_id}
        return {'status': 'error', 'data': 'data could not be logged'}

    def add_open_ai_create_completions(self, kwargs, source='Athena'):
        extra_data = {}
        for key,value in kwargs.items():
            if type(value) is float:
                value = Decimal(value)
            extra_data[key] = value
        level   = 'DEBUG'
        message = 'open_ai_create_completions'
        topic   = 'ws-athena'
        logging_kwargs = dict(level       = level       ,
                              message     = message     ,
                              source      = source      ,
                              topic       = topic       ,
                              extra_data  = extra_data  )
        cbr_logging = CBR_Logging(**logging_kwargs)
        return dydb_cbr_logging.add_log_document(cbr_logging)

    # def add_prompt_request(self, gpt_prompt_with_system_and_history: GPT_Prompt_With_System_And_History, gtp_response:str, request_headers:dict):
    #     prompt_data = json_parse(gpt_prompt_with_system_and_history.json())
    #     extra_data = dict(user_prompt     = prompt_data.get('user_prompt') ,
    #                       gtp_response    = gtp_response                   ,
    #                       prompt_data     = prompt_data                    ,
    #                       request_headers = request_headers                )
    #     level   = 'DEBUG'
    #     message = 'prompt_request'
    #     source  = 'Athena'
    #     topic   = 'ws-athena'
    #     logging_kwargs = dict(level       = level       ,
    #                           message     = message     ,
    #                           source      = source      ,
    #                           topic       = topic       ,
    #                           extra_data  = extra_data  )
    #     cbr_logging = CBR_Logging(**logging_kwargs)
    #     return self.dydb_cbr_logging.add_log_document(cbr_logging)

    #
    # def log_data(self, data, level=None, topic=None, user=None):
    #     kwargs = dict(data          = data                  ,
    #                   data_class    = type_full_name(data)  ,
    #                   level         = level or 'NA'         ,
    #                   topic         = topic or 'NA'         ,
    #                   user          = user  or 'NA'         )
    #     log_entry = Log_Entry(**kwargs)
    #     return self.add_log_entry(log_entry)
