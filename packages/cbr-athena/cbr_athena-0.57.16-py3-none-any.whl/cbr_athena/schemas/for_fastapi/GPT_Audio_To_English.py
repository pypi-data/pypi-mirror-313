from fastapi import  UploadFile
from pydantic import BaseModel


class GPT_Audio_To_English(BaseModel):
    audio_base_64  : str
    prompt         : str
    temperature    : float
    response_format: str