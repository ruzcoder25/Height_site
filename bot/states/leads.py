# bot/states/leads.py
from aiogram.fsm.state import State, StatesGroup


class LeadStates(StatesGroup):
    """Lead bilan ishlash uchun holatlar"""
    viewing_lead = State()
    waiting_for_comment = State()
    waiting_for_status = State()
    confirming = State()
    navigating = State()


class LeadUpdateStates(StatesGroup):
    """(Agar kerak bo‘lsa keyin ishlatasiz)"""
    add_comment = State()
    add_status = State()
