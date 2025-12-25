from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.keyboards import get_main_menu_keyboard, get_login_keyboard
from bot.services import is_authenticated, clear_user_session

router = Router()


@router.message(F.text == "⬅️ Orqaga")
async def back_to_main_menu(message: Message, state: FSMContext):
    """Asosiy menyuga qaytish"""
    user_id = message.from_user.id

    if not is_authenticated(user_id):
        await message.answer(
            "Tizimga kirmagansiz. Iltimos, login qiling.",
            reply_markup=get_login_keyboard()
        )
        return

    await state.clear()
    await message.answer(
        "🏠 Asosiy menyu",
        reply_markup=get_main_menu_keyboard()
    )


@router.message(F.text == "🚪 Chiqish")
async def logout(message: Message, state: FSMContext):
    """Tizimdan chiqish"""
    user_id = message.from_user.id
    clear_user_session(user_id)
    await state.clear()

    await message.answer(
        "👋 Tizimdan chiqdingiz. Yana kutib qolamiz!",
        reply_markup=get_login_keyboard()
    )