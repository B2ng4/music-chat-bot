from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message,FSInputFile
from aiogram.filters import Command

from keyboards.main import keyboard_main
from module import generateVocal
from models.model import Form
from models.generateImage.kandinskiy import Text2ImageAPI

import base64
import os

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет! Я могу сгенерировать вокал!🎤🎧", reply_markup=keyboard_main)

@router.message(lambda message: message.text == "У меня уже есть текст🎶")
async def request_text(msg: Message, state: FSMContext):
    await msg.answer("Отправьте мне текст")

    await state.set_state(Form.waiting_for_text)

@router.message(Form.waiting_for_text)
async def generate(msg: Message, state: FSMContext):
    voice_file = await generateVocal(msg.text)
    await msg.answer("⚙️⚙️⚙️*Погодите*...*Я сочиняю*...⚙️⚙️️⚙️",parse_mode="Markdown")
    await msg.answer_voice(voice=FSInputFile(voice_file),caption="Сгенерированный вокал")
    await state.clear()

@router.message(lambda message: message.text == "Генерация")
async def request_text(msg: Message):
    await msg.answer("⚙️⚙️⚙️*Погодите*...*Я творю*...⚙️⚙️️⚙️", parse_mode="Markdown")

    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', api_key = os.getenv("api_key"), secret_key = os.getenv("secret_key"))
    model_id = api.get_model()
    uuid = api.generate("Cоздай обложку для песни, её первые слова:", model_id)
    images = api.check_generation(uuid)
    print("Image successfully generated")

    if images:
        directory = 'models/generateImage/images'

        for idx, img_base64 in enumerate(images):
            file_number = idx + 1
            file_path = os.path.join(directory, f"image_from_{msg.from_user.username}_#{file_number}.jpg")

            while os.path.exists(file_path):
                file_number += 1
                file_path = os.path.join(directory, f"image_from_{msg.from_user.username}_#{file_number}.jpg")

            with open(file_path, "wb") as file:
                file.write(base64.b64decode(img_base64))

                photo = FSInputFile(file_path)
                await msg.answer_photo(photo=photo, caption="Вот ваша обложка")
    else:
        await msg.answer("Упс. Не получилось")
