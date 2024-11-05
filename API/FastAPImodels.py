from click import prompt
from pydantic import BaseModel


class Prompt(BaseModel):
    text: str


class MusText(BaseModel):
    str