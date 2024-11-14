from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btn1 = KeyboardButton(text='У меня уже есть текст 🎶')
btn2 = KeyboardButton(text='Генерация с нуля 🎹')
#btn3 = KeyboardButton(text='Генерация обложки')

keyboard_main = ReplyKeyboardMarkup(
    keyboard=[[btn1, btn2]],
    resize_keyboard=True
)

