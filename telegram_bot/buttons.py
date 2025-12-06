from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



lead_buttons = ReplyKeyboardMarkup(
        keyboard=[

            [
                KeyboardButton(text="New Leads"),
                KeyboardButton(text="Laret Leads"),

            ]
    ],
    resize_keyboard=True
)

def lead_inline_kb(lead_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="Comment va Vaqt", callback_data=f"later:{lead_id}"),
            InlineKeyboardButton(text="Xizmat kerak emas", callback_data=f"failed:{lead_id}")
        ]]
    )
