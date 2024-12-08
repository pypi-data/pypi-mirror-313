from osbot_utils.base_classes.Type_Safe import Type_Safe

class CBR_Logging(Type_Safe):
    # auto populated
    id          : str           # to be set by Dynamo_DB__Table
    timestamp   : int           # to be set by the request
    # indexes
    date        : str   = 'NA'
    level       : str   = 'NA'
    message     : str   = 'NA'
    source      : str   = 'NA'
    topic       : str   = 'NA'

    # other
    city        : str   = 'NA'
    country     : str   = 'NA'
    user_id     : str   = 'NA'
    extra_data  : dict
