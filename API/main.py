
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.vocal_generate import vocal_get_wav
from models.text_generate import music_text_generate
from  FastAPImodels import *
from starlette.requests import Request


#uvicorn main:app
app = FastAPI(title="Музыкальный чат-бот")


origins = [
    "*",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def home():
   return {"response": "API для взаимодействия с AI моделями"}


@app.post("/api/v1/get_music_text" )
async def music_text(prompt:Prompt):
    all_music_text = await music_text_generate(prompt.json())
    return {"music_text": all_music_text}


@app.post("/api/v1/get_vocal")
async def vocal(musictext:MusText):
    wav_vocal = await vocal_get_wav(musictext.json())
    return {"path_ti_vocal":wav_vocal}


