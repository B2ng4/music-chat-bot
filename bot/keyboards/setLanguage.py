from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

rus = KeyboardButton(text="English 🇬🇧")
eng = KeyboardButton(text="Russian 🇷🇺")

languagekb = ReplyKeyboardMarkup(keyboard=[[rus,eng]], resize_keyboard=True,
                                           input_field_placeholder="Choose your language")