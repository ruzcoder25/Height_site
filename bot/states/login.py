from aiogram.fsm.state import State, StatesGroup

class LoginStates(StatesGroup):
    """Login uchun holatlar"""
    waiting_for_username = State()
    waiting_for_password = State()