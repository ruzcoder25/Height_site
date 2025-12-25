from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.states import LeadStates
from bot.keyboards import (
    get_new_leads_keyboard,
    get_later_leads_keyboard,
    get_lead_action_keyboard,
    get_login_keyboard,
    get_main_menu_keyboard
)
from bot.services import (
    is_authenticated,
    get_user_session,
    get_new_leads_count,
    get_later_leads_count,
    get_new_leads,
    get_later_leads,
    update_lead
)
from bot.utils import format_lead_info, validate_date, format_date

router = Router()

# =====================================================
# YANGI LEADLAR
# =====================================================

@router.message(F.text == "🆕 Yangi leadlar")
async def new_leads_section(message: Message):
    if not is_authenticated(message.from_user.id):
        await message.answer("Iltimos, login qiling.", reply_markup=get_login_keyboard())
        return

    await message.answer("🆕 Yangi leadlar bo‘limi", reply_markup=get_new_leads_keyboard())


@router.message(F.text == "📊 Barcha yangi leadlar soni")
async def new_leads_count(message: Message):
    session = get_user_session(message.from_user.id)
    count = await get_new_leads_count(session['token'])
    await message.answer(f"📊 Yangi leadlar soni: {count} ta")


@router.message(F.text == "📞 Yangi lead bilan bog'lanish")
async def start_new_leads(message: Message, state: FSMContext):
    session = get_user_session(message.from_user.id)
    leads = await get_new_leads(session['token'])

    if not leads:
        await message.answer("❌ Yangi leadlar yo‘q", reply_markup=get_new_leads_keyboard())
        return

    session['leads_list'] = leads
    session['current_lead_index'] = 0
    session['current_lead_type'] = 'new'
    print(f"handlers/leads.py session : {session}")
    await show_lead(message, state, leads[0])


# =====================================================
# LATER LEADLAR
# =====================================================

@router.message(F.text == "⏳ Keyinroq bog'laniladigan leadlar")
async def later_leads_section(message: Message):
    if not is_authenticated(message.from_user.id):
        await message.answer("Iltimos, login qiling.", reply_markup=get_login_keyboard())
        return

    await message.answer("⏳ Later leadlar", reply_markup=get_later_leads_keyboard())


@router.message(F.text == "📊 Barcha later leadlar soni")
async def later_leads_count(message: Message):
    session = get_user_session(message.from_user.id)
    count = await get_later_leads_count(session['token'])
    await message.answer(f"📊 Later leadlar soni: {count} ta")


@router.message(F.text == "📞 Later lead bilan bog'lanish")
async def start_later_leads(message: Message, state: FSMContext):
    session = get_user_session(message.from_user.id)
    leads = await get_later_leads(session['token'])

    if not leads:
        await message.answer("❌ Later leadlar yo‘q", reply_markup=get_later_leads_keyboard())
        return

    session['leads_list'] = leads
    session['current_lead_index'] = 0
    session['current_lead_type'] = 'later'

    await show_lead(message, state, leads[0])


# =====================================================
# LEAD KO‘RSATISH
# =====================================================

async def show_lead(message: Message, state: FSMContext, lead: dict):
    await state.set_state(LeadStates.viewing_lead)
    await state.update_data(
        current_lead=lead,
        commented=False,
        dated=False,
        status_set=False
    )

    await message.answer(
        format_lead_info(lead),
        reply_markup=get_lead_action_keyboard()
    )


async def go_next_lead(message: Message, state: FSMContext):
    session = get_user_session(message.from_user.id)
    idx = session['current_lead_index']
    leads = session['leads_list']

    if idx + 1 < len(leads):
        session['current_lead_index'] += 1
        await show_lead(message, state, leads[session['current_lead_index']])
    else:
        await state.clear()
        session['leads_list'] = []
        session['current_lead_index'] = 0
        await message.answer("✅ Barcha leadlar tugadi", reply_markup=get_main_menu_keyboard())


async def go_prev_lead(message: Message, state: FSMContext):
    session = get_user_session(message.from_user.id)
    idx = session['current_lead_index']

    if idx > 0:
        session['current_lead_index'] -= 1
        await show_lead(message, state, session['leads_list'][session['current_lead_index']])
    else:
        await message.answer("⛔ Bu birinchi lead")


# =====================================================
# COMMENT
# =====================================================

@router.message(LeadStates.viewing_lead, F.text == "📝 Comment yozish")
async def start_comment(message: Message, state: FSMContext):
    await state.set_state(LeadStates.waiting_for_comment)
    await message.answer("📝 Comment yozing:")


@router.message(LeadStates.waiting_for_comment)
async def save_comment(message: Message, state: FSMContext):
    data = await state.get_data()
    lead = data['current_lead']
    session = get_user_session(message.from_user.id)
    print("handlers/leads.py ")
    if await update_lead(session['token'], lead['id'], comment=message.text):
        lead['user_comment'] = message.text
        await state.update_data(current_lead=lead, commented=True)
        await message.answer("✅ Comment saqlandi")
    else:
        await message.answer("❌ Comment saqlanmadi")

    await state.set_state(LeadStates.viewing_lead)
    await message.answer(format_lead_info(lead), reply_markup=get_lead_action_keyboard())


# =====================================================
# SANA
# =====================================================

@router.message(LeadStates.viewing_lead, F.text == "📅 Sana belgilash")
async def start_date(message: Message, state: FSMContext):
    await state.set_state(LeadStates.waiting_for_date)
    await message.answer("📅 Sana kiriting (YYYY.MM.DD) yoki skip")


@router.message(LeadStates.waiting_for_date)
async def save_date(message: Message, state: FSMContext):
    if not validate_date(message.text):
        await message.answer("❌ Sana formati noto‘g‘ri")
        return

    data = await state.get_data()
    lead = data['current_lead']
    session = get_user_session(message.from_user.id)
    date = format_date(message.text)

    await update_lead(session['token'], lead['id'], call_date=date)
    await state.update_data(dated=True)

    await state.set_state(LeadStates.viewing_lead)
    await message.answer("📅 Sana saqlandi", reply_markup=get_lead_action_keyboard())


# =====================================================
# STATUS (BITTASI)
# =====================================================

async def set_status(message: Message, state: FSMContext, status: str):
    data = await state.get_data()
    lead = data['current_lead']
    session = get_user_session(message.from_user.id)

    await update_lead(session['token'], lead['id'], status=status)
    await state.update_data(status_set=True)
    await message.answer(f"✅ Status: {status}")
    await go_next_lead(message, state)


@router.message(LeadStates.viewing_lead, F.text == "⏳ Later")
async def status_later(message: Message, state: FSMContext):
    await set_status(message, state, "LATER")


@router.message(LeadStates.viewing_lead, F.text == "❌ Failed")
async def status_failed(message: Message, state: FSMContext):
    await set_status(message, state, "FAILED")


@router.message(LeadStates.viewing_lead, F.text == "✅ Success")
async def status_success(message: Message, state: FSMContext):
    await set_status(message, state, "SUCCESS")


# =====================================================
# MANUAL NAVIGATION
# =====================================================

@router.message(LeadStates.viewing_lead, F.text == "➡️ Keyingi lead")
async def manual_next(message: Message, state: FSMContext):
    data = await state.get_data()
    print(f"handlers/leads.py data : {data}")
    if not (data['commented'] and data['dated'] and data['status_set']):
        await message.answer("❗ Avval comment, sana va statusni belgilang")
        return

    await go_next_lead(message, state)


@router.message(LeadStates.viewing_lead, F.text == "⬅️ Oldingi lead")
async def manual_prev(message: Message, state: FSMContext):
    await go_prev_lead(message, state)
