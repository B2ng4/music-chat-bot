from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message,FSInputFile,ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup

from keyboards.keyboards import get_main_keyboard
from keyboards.setLanguage import languagekb
from modules.generateVocal import generateVocal
from models.ModelForm import Form
from models.ModelText2ImageAPI import Text2ImageAPI

import modules.translateText as TF

from modules.generateImage import generateImage
from apiRequests.generateText import generateText
import os


router = Router()

class LanguageState(StatesGroup):
    CHOSENLANGUAGE = State()

@router.message(Command("start"))
async def cmd_start(msg: Message, state: FSMContext):
    await msg.delete()
    await msg.answer("Hello, setup my language!", reply_markup=languagekb)
    await state.set_state(LanguageState.CHOSENLANGUAGE)

@router.message(LanguageState.CHOSENLANGUAGE)
async def choose_language(msg: Message,state: FSMContext):
    if msg.text == "English 🇬🇧":
        lang = 'en'
        await msg.answer(await TF.translation("Вы успешно установили язык!",lang),reply_markup=ReplyKeyboardRemove())
        await state.update_data(Lang = lang)
        await start_handler(msg, state)

    elif msg.text in "Russian 🇷🇺":
        lang = 'ru'
        await msg.answer(await TF.translation("Вы успешно установили язык!",lang),reply_markup=ReplyKeyboardRemove())
        await state.update_data(Lang = lang)
        await start_handler(msg, state)

@router.message(LanguageState.CHOSENLANGUAGE)
async def start_handler(msg: Message,state: FSMContext):
    data = await state.get_data()
    lang = data.get('Lang')
    await msg.answer(await TF.translation("Привет! Я могу сгенерировать вокал!🎤🎧", lang), reply_markup=get_main_keyboard(lang))
    await state.clear()
    await state.update_data(Lang=lang)

@router.message(lambda message: message.text in ["У меня уже есть текст🎶", "I already have text🎶"])
async def request_text(msg: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('Lang')
    await msg.answer(await TF.translation("Отправьте мне текст", lang))
    await state.update_data(Lang=lang)
    await state.set_state(Form.waiting_for_text)

@router.message(Form.waiting_for_text)
async def generate(msg: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('Lang')
    voice_file = await generateVocal(msg.text)
    await msg.answer(await TF.translation("⚙️⚙️⚙️*Погодите*...*Я сочиняю*...⚙️⚙️️⚙️",lang),parse_mode="Markdown")
    await msg.answer_voice(voice=FSInputFile(voice_file),caption= await TF.translation("Cгенерированный вокал",lang))
    await state.update_data(Lang=lang)
    await state.clear()

@router.message(lambda message: message.text in ["Генерация с нуля🎹", "Generation from scratch🎹"])
async def request_text(msg: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('Lang')
    await msg.answer(await TF.translation("Напишите, о чем должен быть текст?", lang), parse_mode="Markdown")
    await state.update_data(Lang=lang)
    @router.message()
    async def receive_text(msg: Message):
        text = msg.text
        genText = f'{generateText(text)}'
        await msg.answer(genText, parse_mode="Markdown")


@router.message(lambda message: message.text in ["Генерация", "Generation"])
async def request_text(msg: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('Lang')
    await msg.answer(await TF.translation("⚙️⚙️⚙️*Погодите*...*Я творю*...⚙️⚙️️⚙️", lang), parse_mode="Markdown")

    api_kandinsky = Text2ImageAPI('https://api-key.fusionbrain.ai/',
                                  api_key=os.getenv("api_key"),
                                  secret_key=os.getenv("secret_key"))
    model_id = api_kandinsky.get_model()
    prompt = api_kandinsky.generate("Cоздай обложку для песни, её первые слова:", model_id)
    generated_images = api_kandinsky.check_generation(prompt)
    photos = await generateImage(generated_images, msg.from_user.username)
    if photos:
        await msg.answer_photo(photo=photos[0], caption= await TF.translation("Вот ваша обложка",lang))
    await state.update_data(Lang=lang)
