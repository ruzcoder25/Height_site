from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_login_keyboard():
    """Login tugmasi"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔐 Login")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_main_menu_keyboard():
    """Asosiy menyu tugmalari"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🆕 Yangi leadlar")],
            [KeyboardButton(text="⏳ Keyinroq bog'laniladigan leadlar")],
            [KeyboardButton(text="🚪 Chiqish")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_back_keyboard():
    """Orqaga tugmasi"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⬅️ Orqaga")]
        ],
        resize_keyboard=True
    )
    return keyboard