from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btn1 = KeyboardButton(text='Да, все классно! 😇')
btn2 = KeyboardButton(text='Нет! Перегенерируй ⛔')

keyboard_accept = ReplyKeyboardMarkup(
    keyboard=[[btn1, btn2]],
    resize_keyboard=True
)

