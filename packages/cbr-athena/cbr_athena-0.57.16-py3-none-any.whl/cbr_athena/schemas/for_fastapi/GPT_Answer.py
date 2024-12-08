from typing     import Optional
from pydantic   import BaseModel

class GPT_Answer(BaseModel):
    model  : Optional[str] = None
    answer: str