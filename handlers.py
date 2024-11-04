from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message,FSInputFile
from aiogram.filters import Command

from keyboards.main import keyboard_main
from module import generateVocal
from model import Form

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