from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

btn1 = KeyboardButton(text="У меня уже есть текст🎶")
btn2 = KeyboardButton(text="Генерация с нуля🎹")
btn3 = KeyboardButton(text="Генерация")

btn4 = KeyboardButton(text="I already have the text🎶")
btn5 = KeyboardButton(text="Generation from scratch🎹")
btn6 = KeyboardButton(text="Generation")

keyboard_main_ru = ReplyKeyboardMarkup(
    keyboard=[[btn1, btn2, btn3]],
    resize_keyboard=True,
),
keyboard_main_eng = ReplyKeyboardMarkup(
    keyboard=[[btn4, btn5, btn6]],
    resize_keyboard=True,
)

def get_main_keyboard(lang='ru'):
    if lang == 'en':
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="I already have text🎶")],
                [KeyboardButton(text="Generation from scratch🎹")],
                [KeyboardButton(text="Generation")],
            ],
            resize_keyboard=True
        )
    else:  # Russian by default
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="У меня уже есть текст🎶")],
                [KeyboardButton(text="Генерация с нуля🎹")],
                [KeyboardButton(text="Генерация")],
            ],
            resize_keyboard=True
        )
