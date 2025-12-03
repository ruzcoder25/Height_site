from aiogram.fsm.state import StatesGroup, State

class LeadLaterStates(StatesGroup):
    waiting_for_comment = State()
