
import os
from gigachat import GigaChat
from dotenv import load_dotenv



load_dotenv()
GIGACHAT_TOKEN = os.getenv("GIGACHAT_TOKEN")
async def music_text_generate(prompt:str)->str:
    """
    Функция для написания текста песни с помощью  нейросети Gigachat
    input: prompt
    output: music_text
    """

    giga = GigaChat(
        credentials=GIGACHAT_TOKEN,
        verify_ssl_certs=False, model="GigaChat")
    response = giga.chat(
        f"{prompt} -> Это наброски для текста песни, дополни, чтобы получились полноценные слова песни. Должно  быть не менее 3х куплетов!")
    response = response.choices[0].message.content
    return response


##print( music_text_generate("Дождь, ожидание холод, боль, снова я  расколот"))