from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message,FSInputFile
from aiogram.filters import Command

from keyboards.main import keyboard_main
from modules.generateVocal import generateVocal
from models.ModelForm import Form
from models.ModelText2ImageAPI import Text2ImageAPI

from modules.generateImage import generateImage
from apiRequests.generateText import generateText
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

@router.message(lambda message: message.text == "Генерация с нуля🎹")
async def request_text(msg: Message):
    await msg.answer("Напишите, о чем должен быть текст?", parse_mode="Markdown")
    @router.message()
    async def receive_text(msg: Message):
        text = msg.text
        genText = f'{generateText(text)}'
        await msg.answer(genText, parse_mode="Markdown")


@router.message(lambda message: message.text == "Генерация")
async def request_text(msg: Message):
    await msg.answer("⚙️⚙️⚙️*Погодите*...*Я творю*...⚙️⚙️️⚙️", parse_mode="Markdown")

    api_kandinsky = Text2ImageAPI('https://api-key.fusionbrain.ai/',
                                  api_key=os.getenv("api_key"),
                                  secret_key=os.getenv("secret_key"))
    model_id = api_kandinsky.get_model()
    prompt = api_kandinsky.generate("Cоздай обложку для песни, её первые слова:", model_id)
    generated_images = api_kandinsky.check_generation(prompt)
    photos = await generateImage(generated_images, msg.from_user.username)
    if photos:
        await msg.answer_photo(photo=photos[0], caption="Вот ваша обложка")
