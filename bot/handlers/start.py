from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from bot.keyboards import get_login_keyboard
from bot.services import is_authenticated
from bot.keyboards import get_main_menu_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Bot ishga tushganda /start komandasi"""
    user_id = message.from_user.id

    if is_authenticated(user_id):
        await message.answer(
            "🏠 Asosiy menyu",
            reply_markup=get_main_menu_keyboard()
        )
    else:
        await message.answer(
            "👋 Assalomu alaykum!\n\n"
            "Botdan foydalanish uchun tizimga kirishingiz kerak.",
            reply_markup=get_login_keyboard()
        )