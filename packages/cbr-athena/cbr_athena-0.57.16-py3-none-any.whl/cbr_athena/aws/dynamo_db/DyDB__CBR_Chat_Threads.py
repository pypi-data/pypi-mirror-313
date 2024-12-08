from cbr_shared.schemas.base_models.chat_threads.GPT_Prompt_With_System_And_History import GPT_Prompt_With_System_And_History
from osbot_aws.aws.dynamo_db.domains.DyDB__Table_With_Timestamp                     import DyDB__Table_With_Timestamp



from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cbr_athena.schemas.Chat_Thread                                                 import Chat_Thread



DYNAMO_DB__TABLE_NAME__CHAT_THREADS = 'arn:aws:dynamodb:eu-west-2:470426667096:table/{env}__cbr_chat_threads'           # todo: refactor so that the region_name and account_id are not hardcoded
TABLE_CHAT_THREADS__INDEXES_NAMES   = [ 'date', 'user_name', 'chat_thread_id']

class DyDB__CBR_Chat_Threads(DyDB__Table_With_Timestamp):

    def __init__(self, **kwargs):
        from cbr_athena.aws.dynamo_db.DyDB__CBR_Logging import DYNAMO_DB__TABLE___REGION_NAME
        from cbr_athena.utils.Utils                     import Utils

        super().__init__(**kwargs)
        self.table_name             = DYNAMO_DB__TABLE_NAME__CHAT_THREADS.format(env=Utils.current_execution_env())
        self.table_indexes          = TABLE_CHAT_THREADS__INDEXES_NAMES
        self.dynamo_db.region_name  = DYNAMO_DB__TABLE___REGION_NAME                # todo: find better way to handle the target region of the CBR tables
#        self.dynamo_db.client = self.cbr_client                                     # this overides the dynamodb object with noe that is CBR specific

    # @cache_on_self
    # def cbr_client(self):
    #     return Session().client('dynamodb', region_name=DYNAMO_DB__TABLE___REGION_NAME)

    def add_chat_thread(self, chat_thread : 'Chat_Thread'):
        from cbr_athena.config.CBR__Config__Athena import cbr_config_athena

        if cbr_config_athena.aws_disabled():                                        # todo: find better place to do this
            return None
        chat_thread.date = self.date_today()                                        # make sure date field is set
        document         = chat_thread.json()
        response         = super().add_document(document)
        if response.get('document'):
            return response.get('document', {}).get('id')
        return response

    def add_prompt_request(self, gpt_prompt_with_system_and_history: GPT_Prompt_With_System_And_History, gpt_response:str, request_headers:dict, source='Athena'):
        from cbr_athena.schemas.Chat_Thread import Chat_Thread
        from osbot_utils.utils.Misc         import is_guid

        prompt_data = gpt_prompt_with_system_and_history.dict()

        user_prompt    = prompt_data.get('user_prompt'   ) or 'NA'
        user_data      = prompt_data.get('user_data'     ) or {}
        session_id     = user_data.get('session_id'      ) or 'NA'
        chat_thread_id = prompt_data.get('chat_thread_id') or 'NA'
        user_name      = 'NA'
        chat_kwargs = dict(user_prompt     = user_prompt     ,
                           session_id      = session_id      ,
                           user_name       = user_name       ,
                           chat_thread_id  = chat_thread_id  ,
                           gpt_response    = gpt_response    ,
                           source          = source          ,
                           prompt_data     = prompt_data     ,
                           request_headers = request_headers )

        cbr_logging = Chat_Thread(**chat_kwargs)

        response = self.add_chat_thread(cbr_logging)

        if type(response) is str and is_guid(response):
            return response
        return ''


    def date_today(self):
        from osbot_utils.utils.Misc import date_time_now

        return date_time_now(date_time_format='%Y-%m-%d')       # force the correct value of date

dydb_cbr_chat_threads = DyDB__CBR_Chat_Threads

dydb_chat_threads = DyDB__CBR_Chat_Threads()

def log_llm_chat(gpt_prompt_with_system_and_history, gpt_response, request_headers):

    kwargs = dict(gpt_prompt_with_system_and_history=gpt_prompt_with_system_and_history,
                  gpt_response=gpt_response,
                  request_headers=request_headers,
                  source='Athena')
    dydb_chat_threads.add_prompt_request(**kwargs)