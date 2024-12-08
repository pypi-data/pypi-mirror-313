from osbot_utils.base_classes.Type_Safe import Type_Safe


class Chat_Thread(Type_Safe):
    # auto populated
    id              : str           # to be set by Dynamo_DB__Table
    timestamp       : int           # to be set by the request
    # indexes
    date            : str
    user_name       : str
    chat_thread_id  : str

    # other
    session_id      : str   = 'NA'
    user_prompt     : str   = 'NA'
    gpt_response    : str   = 'NA'
    source          : str   = 'NA'
    prompt_data     : dict
    request_headers : dict