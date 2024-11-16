from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message,FSInputFile
from aiogram.filters import Command

from keyboards.accept import keyboard_accept
from keyboards.main import keyboard_main

from models.ModelForm import Form
from models.ModelText2ImageAPI import Text2ImageAPI

from apiRequests.generateVocal import generateVocal
from apiRequests.generateText import generateText

from modules.generateImage import generateImage

import os

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет! Я помогу сгенерировать вокал!🎤🎧", reply_markup=keyboard_main)
    await msg.answer("Я пока еще учусь петь, поэтому могу нестабильно работать. 🙏", reply_markup=keyboard_main)

@router.message(lambda message: message.text == "У меня уже есть текст 🎶")
async def request_text(msg: Message, state: FSMContext):
    await msg.answer("Отправьте мне свой текст")
    await state.set_state(Form.waiting_for_text)

@router.message(Form.waiting_for_text)
async def generate(msg: Message, state: FSMContext):
    user_text = msg.text
    await state.update_data(user_text=user_text)
    await msg.answer("Отправьте промт 📜\n \n(Например: Мужчина с бунтарским, резким духом в стиле панк, с агрессивным тоном)", parse_mode="Markdown")
    await state.set_state(Form.waiting_for_promt)


@router.message(Form.waiting_for_promt)
async def generate_promt(msg: Message, state: FSMContext):
    user_data = await state.get_data()
    user_text = user_data.get('user_text')
    promt = msg.text
    await msg.answer("Получил промт 👌", parse_mode="Markdown")
    await msg.answer("⚙️⚙️⚙️*Погодите*...*Я сочиняю*...⚙️⚙️️⚙️", parse_mode="Markdown")
    voice_file = generateVocal(user_text)
    api_kandinsky = Text2ImageAPI('https://api-key.fusionbrain.ai/',
                                  api_key=os.getenv("api_key"),
                                  secret_key=os.getenv("secret_key"))
    model_id = api_kandinsky.get_model()
    prompt = api_kandinsky.generate("Cоздай обложку для песни, её первые слова:", model_id)
    generated_images = api_kandinsky.check_generation(prompt)
    photos = await generateImage(generated_images, msg.from_user.username)
    await msg.answer_voice(voice=FSInputFile(voice_file),caption="Сгенерированный вокал", reply_markup=keyboard_main)
    await msg.answer_photo(photo=photos[0], caption="Вот ваша обложка")
    await state.clear()

@router.message(lambda message: message.text == "Генерация с нуля 🎹")
async def request_text(msg: Message):
    await msg.answer("Напишите, о чем должен быть текст?", parse_mode="Markdown")
    @router.message()
    async def receive_text(msg: Message):
        await msg.answer("⚙️⚙️⚙️*Погодите*...*Сочиняю*...⚙️⚙️⚙️", parse_mode="Markdown")
        text = msg.text
        genText = f'{generateText(text)}'
        await msg.answer(genText, reply_markup=keyboard_accept)

@router.message(lambda message: message.text == "Нет! Перегенерируй ⛔")
async def request_text(msg: Message):
    await msg.answer("Хорошо, понял вас! 😼\nДобавьте больше деталей! 🖊️", parse_mode="Markdown")
    @router.message()
    async def receive_text(msg: Message):
        text = msg.text
        genText = f'{generateText(text)}'
        await msg.answer(genText, reply_markup=keyboard_accept)

@router.message(lambda message: message.text == "Да, все классно! 😇")
async def request_text(msg: Message, state: FSMContext):
    await msg.answer("Я пока еще учусь петь! 🥺\nМожете просто переотправить те строки, которые вам понравились больше 😞")

    await state.set_state(Form.waiting_for_text)
