from decimal                                                 import Decimal
from typing                                                  import Optional
from pydantic                                                import BaseModel
from osbot_utils.helpers.Random_Guid                         import Random_Guid
from cbr_shared.schemas.base_models.chat_threads.GPT_History import GPT_History


DEFAULT_MAX_TOKENS      = 4092
#DEFAULT_MODEL          = GPT_Modules.gpt_3_5_turbo
DEFAULT_MODEL_PROVIDER = 'OpenAI'
DEFAULT_SEED           = 42
DEFAULT_TEMPERATURE    = 0.0
DEFAULT_USER_PROMPT    = 'Hi'


class LLM_Prompt(BaseModel):
    chat_thread_id: Optional[str]               = Random_Guid()
    histories     : Optional[list[GPT_History]] = []
    images        : list[str]                   = []
    max_tokens    : Optional[int]               = DEFAULT_MAX_TOKENS
    #model         : GPT_Modules                 = DEFAULT_MODEL
    model_provider: str                         = DEFAULT_MODEL_PROVIDER       # rename due to this pydantic conflict: UserWarning: Field "model_provider" has conflict with protected namespace "model_".
    seed          : int                         = DEFAULT_SEED
    system_prompts: Optional[list[str]]         = []
    temperature   : Decimal                     = Decimal(DEFAULT_TEMPERATURE)
    user_data     : Optional[dict]              = {}
    user_prompt   : str                         = DEFAULT_USER_PROMPT

    def json(self, *args, **kwargs):
        from osbot_utils.utils.Json import from_json_str

        json_str = self.json_str(*args, **kwargs)
        return from_json_str(json_str)

    def json_str(self, *args, **kwargs):
        return super().json(*args, **kwargs)