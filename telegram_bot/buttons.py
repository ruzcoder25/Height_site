from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



lead_buttons = ReplyKeyboardMarkup(
        keyboard=[

            [
                KeyboardButton(text="New Leads"),
                KeyboardButton(text="Later Leads"),

            ]
    ],
    resize_keyboard=True
)

new_inline_button = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="Barcha buyurtmalar ro'yhati", callback_data="new"),
        InlineKeyboardButton(text="Buyurtmalarni donalab chiqarish", callback_data="a_lead")
    ]]
)