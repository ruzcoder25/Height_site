from aiogram.fsm.state import State, StatesGroup

class LeadStates(StatesGroup):
    """Lead bilan ishlash uchun holatlar"""
    viewing_lead = State()
    waiting_for_comment = State()
    waiting_for_date = State()

class LeadUpdateStates(StatesGroup):
    """Lead yangilash uchun holatlar"""
    add_comment = State()
    add_date = State()
    add_call_date = State()
    add_status = State()