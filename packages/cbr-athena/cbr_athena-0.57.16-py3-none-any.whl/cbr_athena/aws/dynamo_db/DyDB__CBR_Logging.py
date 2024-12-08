from cbr_athena.schemas.CBR_Logging                             import CBR_Logging
from osbot_aws.aws.dynamo_db.domains.DyDB__Table_With_Timestamp import DyDB__Table_With_Timestamp

#DYNAMO_DB__TABLE_NAME__CBR_LOGGING = '{env}__cbr_logging'
DYNAMO_DB__TABLE___ACCOUNT_ID      = '470426667096'                                                                         # todo: refactor so that the region_name and account_id are not hardcoded
DYNAMO_DB__TABLE___REGION_NAME     = 'eu-west-2'
DYNAMO_DB__TABLE_NAME__CBR_LOGGING = f'arn:aws:dynamodb:{DYNAMO_DB__TABLE___REGION_NAME}:{DYNAMO_DB__TABLE___ACCOUNT_ID}:table/{{env}}__cbr_logging'

TABLE_CBR_LOGGING__INDEXES_NAMES   = [ 'date', 'level', 'message', 'source', 'topic']

class DyDB__CBR_Logging(DyDB__Table_With_Timestamp):
    def __init__(self, **kwargs):
        from cbr_athena.utils.Utils import Utils

        super().__init__(**kwargs)
        self.table_name             = DYNAMO_DB__TABLE_NAME__CBR_LOGGING.format(env=Utils.current_execution_env())
        self.table_indexes          = TABLE_CBR_LOGGING__INDEXES_NAMES
        self.dynamo_db.region_name  = DYNAMO_DB__TABLE___REGION_NAME            # todo: find better way to handle the target region of the CBR tables
        #self.dynamo_db.client = self.cbr_client

    #@cache_on_self
    #def cbr_client(self):
    #    return Session().client('dynamodb', region_name=DYNAMO_DB__TABLE___REGION_NAME)

    def add_document(self, document):
        from cbr_athena.config.CBR__Config__Athena import cbr_config_athena

        if cbr_config_athena.aws_disabled():
            return None
        response = super().add_document(document)
        if response.get('document'):
            return response.get('document', {}).get('id')                  # todo add logging to capture scenario when response returns an error
        return response

    def add_log_document(self, cbr_logging: CBR_Logging):
        return self.log_request(cbr_logging)

    def add_log_message(self, message, **kwargs):
        cbr_logging = CBR_Logging(message=message, **kwargs)
        return self.log_request(cbr_logging)

    def add_log_entry(self, log_entry):                 # todo: auto add the date and source fields
        kwargs      = log_entry.dict()
        cbr_logging = CBR_Logging(**kwargs)
        return self.log_request(cbr_logging)

    def log_request(self, cbr_logging: CBR_Logging):
        if type(cbr_logging) is not CBR_Logging:            # only allow cbr_request
            return {'error': f'document to log must of type CBR_Logging and it was of type {type(cbr_logging)}'}
        cbr_logging.date = self.date_today()
        document         = cbr_logging.json()
        document_id      = self.add_document(document)
        return document_id

    def date_today(self):
        from osbot_utils.utils.Misc import date_time_now

        return date_time_now(date_time_format='%Y-%m-%d')       # force the correct value of date

dydb_cbr_logging = DyDB__CBR_Logging()
