
from pydantic import BaseModel


class Prompt(BaseModel):
    text: str


class MusText(BaseModel):
    text:str