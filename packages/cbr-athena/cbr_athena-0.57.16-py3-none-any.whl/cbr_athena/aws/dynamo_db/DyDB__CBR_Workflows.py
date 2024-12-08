from cbr_athena.aws.dynamo_db.DyDB__CBR_Logging                 import DYNAMO_DB__TABLE___REGION_NAME
from cbr_athena.llms.tasks.LLM__Task                            import LLM__Task
from cbr_athena.config.CBR__Config__Athena                      import cbr_config_athena
from cbr_athena.utils.Utils                                     import Utils
from osbot_aws.apis.Session                                     import Session
from osbot_aws.aws.dynamo_db.domains.DyDB__Table_With_Timestamp import DyDB__Table_With_Timestamp
from osbot_utils.decorators.methods.cache_on_self               import cache_on_self

DYNAMO_DB__TABLE_NAME__CBR_WORKFLOWS = 'arn:aws:dynamodb:eu-west-2:470426667096:table/{env}__cbr_workflows'     # todo: refactor so that the region_name and account_id are not hardcoded
TABLE_CBR_WORKFLOWS__INDEXES_NAMES   = [ 'date']                                                                # todo: add the workflow_id, action_id and task_id indexes

class DyDB__CBR_Workflows(DyDB__Table_With_Timestamp):
    env : str = Utils.current_execution_env()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table_name            = DYNAMO_DB__TABLE_NAME__CBR_WORKFLOWS.format(env=self.env)
        self.table_indexes         = TABLE_CBR_WORKFLOWS__INDEXES_NAMES
        self.dynamo_db.region_name = DYNAMO_DB__TABLE___REGION_NAME
    #     self.dynamo_db.client = self.client
    #
    # @cache_on_self
    # def client(self):
    #     return Session().client('dynamodb', region_name=DYNAMO_DB__TABLE___REGION_NAME)

    def add_document(self, document):
        if cbr_config_athena.aws_disabled():
            return None
        # todo refactor this to DyDB__Table_With_Timestamp or further down (since this 'add and get document_id' is a very common pattern)
        response = super().add_document(document)
        if response.get('document'):
            return response.get('document', {}).get('id')                   # todo add logging to capture scenario when response returns an error
        return response

    def add_task(self, llm_task: LLM__Task):
        document = llm_task.json()
        return document