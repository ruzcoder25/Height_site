from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# ================== TEXT CONSTANTS ==================

BTN_NEW_COUNT = "📊 Barcha yangi leadlar soni"
BTN_NEW_CALL = "📞 Yangi lead bilan bog'lanish"

BTN_LATER_COUNT = "📊 Barcha later leadlar soni"
BTN_LATER_CALL = "📞 Later lead bilan bog'lanish"

BTN_COMMENT = "📝 Comment yozish"
BTN_DATE = "📅 Sana belgilash"

BTN_LATER = "⏳ Later"
BTN_FAILED = "❌ Failed"
BTN_SUCCESS = "✅ Success"

BTN_PREV = "⬅️ Oldingi lead"
BTN_NEXT = "➡️ Keyingi lead"
BTN_BACK = "⬅️ Orqaga"


# ================== KEYBOARDS ==================

def get_new_leads_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_NEW_COUNT)],
            [KeyboardButton(text=BTN_NEW_CALL)],
            [KeyboardButton(text=BTN_BACK)],
        ],
        resize_keyboard=True
    )


def get_later_leads_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_LATER_COUNT)],
            [KeyboardButton(text=BTN_LATER_CALL)],
            [KeyboardButton(text=BTN_BACK)],
        ],
        resize_keyboard=True
    )


def get_lead_action_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_COMMENT)],
            [KeyboardButton(text=BTN_DATE)],
            [
                KeyboardButton(text=BTN_LATER),
                KeyboardButton(text=BTN_FAILED),
                KeyboardButton(text=BTN_SUCCESS),
            ],
            [
                KeyboardButton(text=BTN_PREV),
                KeyboardButton(text=BTN_NEXT),
            ],
            [KeyboardButton(text=BTN_BACK)],
        ],
        resize_keyboard=True
    )


def get_start_update_lead():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Lead malumotlarini yangilash")],
            [KeyboardButton(text="⬅️ Orqaga")],
            [KeyboardButton(text="❌ Cancel")],

        ],
        resize_keyboard=True
    )