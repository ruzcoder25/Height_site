# bot/keyboards/leads.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# ================== TEXT CONSTANTS ==================
BTN_NEW_COUNT = "📊 Barcha yangi leadlar soni"
BTN_LATER_COUNT = "📊 Barcha later leadlar soni"

BTN_NEW_SECTION = "🆕 Yangi leadlar bo‘limi"
BTN_LATER_SECTION = "🆕 later leadlar bo‘limi"

BTN_START_CALL = "▶️ Aloqani boshlash"

BTN_LATER = "⏳ Later"
BTN_FAILED = "❌ Failed"
BTN_SUCCESS = "✅ Success"

BTN_CONFIRM = "✅ Tasdiqlash"
BTN_EDIT = "✏️ Tahrirlash"

BTN_PREV = "⬅️ Oldingi lead"
BTN_NEXT = "➡️ Keyingi lead"

BTN_BACK = "⬅️ Orqaga"


# ================== KEYBOARDS ==================
def get_new_leads_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_NEW_COUNT)],
            [KeyboardButton(text=BTN_NEW_SECTION)],
            [KeyboardButton(text=BTN_BACK)],
        ],
        resize_keyboard=True
    )


def get_later_leads_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_LATER_COUNT)],
            [KeyboardButton(text=BTN_LATER_SECTION)],
            [KeyboardButton(text=BTN_BACK)],
        ],
        resize_keyboard=True
    )


def get_lead_action_keyboard() -> ReplyKeyboardMarkup:
    """
    Lead ko‘rsatilganda ham shu keyboard turadi:
    - ▶️ Aloqani boshlash (comment yozish bosqichini ochadi)
    - ⬅️ Orqaga
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_START_CALL)],
            [KeyboardButton(text=BTN_BACK)],
        ],
        resize_keyboard=True
    )


def get_status_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=BTN_LATER),
                KeyboardButton(text=BTN_FAILED),
                KeyboardButton(text=BTN_SUCCESS),
            ],
            [KeyboardButton(text=BTN_BACK)],
        ],
        resize_keyboard=True
    )


def get_confirm_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_CONFIRM), KeyboardButton(text=BTN_EDIT)],
            [KeyboardButton(text=BTN_BACK)],
        ],
        resize_keyboard=True
    )


def get_nav_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_PREV), KeyboardButton(text=BTN_NEXT)],
            [KeyboardButton(text=BTN_BACK)],
        ],
        resize_keyboard=True
    )
