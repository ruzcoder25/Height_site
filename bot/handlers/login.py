from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.states import LoginStates
from bot.services import login_user, save_user_session
from bot.keyboards import get_main_menu_keyboard

router = Router()


@router.message(F.text == "🔐 Login")
async def start_login(message: Message, state: FSMContext):
    """Login jarayonini boshlash"""
    await state.set_state(LoginStates.waiting_for_username)
    await message.answer("👤 Login (username) kiriting:")


@router.message(LoginStates.waiting_for_username)
async def process_username(message: Message, state: FSMContext):
    """Username qabul qilish"""
    username = message.text.strip()
    await state.update_data(username=username)
    await state.set_state(LoginStates.waiting_for_password)
    await message.answer("🔑 Parolni kiriting:")


@router.message(LoginStates.waiting_for_password)
async def process_password(message: Message, state: FSMContext):
    """Parol qabul qilish va login"""
    password = message.text.strip()
    data = await state.get_data()
    username = data.get('username')

    # Login qilish
    result = await login_user(username, password)
    print("handlers/login.py  result : ", result)
    if result.get('success') and result.get('token'):
        # Session saqlash
        save_user_session(
            message.from_user.id,
            result['token'],
            result['role']
        )

        await message.answer(
            f"✅ Muvaffaqiyatli login qilindi!\n\n"
            f"Sizning rolingiz: {result['role']}",
            reply_markup=get_main_menu_keyboard()
        )
        await state.clear()
    else:
        await message.answer(
            f"❌ {result['message']}\n\n"
            "Qaytadan urinib ko'ring."
        )
        await state.set_state(LoginStates.waiting_for_username)
        await message.answer("👤 Login (username) kiriting:")