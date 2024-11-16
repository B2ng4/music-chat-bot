from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    waiting_for_text = State()
    waiting_for_promt = State()