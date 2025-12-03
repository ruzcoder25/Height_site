from aiogram import types, Router
from aiogram.filters import CommandStart

from telegram_bot.buttons import lead_buttons

router = Router()


@router.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer("Hello! I'm Ruzimukhammad", reply_markup=lead_buttons)

