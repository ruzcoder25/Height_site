# bot/handlers/leads.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.states import LeadStates
from bot.keyboards import (
    get_new_leads_keyboard,
    get_later_leads_keyboard,
    get_lead_action_keyboard,
    get_login_keyboard,
    get_main_menu_keyboard,
    get_status_keyboard,
    get_confirm_keyboard,
    get_nav_keyboard,
)
from bot.services import (
    is_authenticated,
    get_user_session,
    get_new_leads_count,
    get_later_leads_count,
    get_new_leads,
    get_later_leads,
    update_lead,
)
from bot.utils import format_lead_info

from bot.keyboards.leads import (
    BTN_NEW_SECTION, BTN_LATER_SECTION, BTN_BACK, BTN_START_CALL,
    BTN_LATER, BTN_FAILED, BTN_SUCCESS,
    BTN_CONFIRM, BTN_EDIT,
    BTN_NEXT, BTN_PREV,
)

router = Router()


# =====================================================
# 1) YANGI / LATER BO‘LIMLARIGA KIRISH
# =====================================================

@router.message(F.text == "🆕 Yangi leadlar")
async def new_leads_section(message: Message, state: FSMContext):
    if not is_authenticated(message.from_user.id):
        await message.answer("Iltimos, login qiling.", reply_markup=get_login_keyboard())
        return

    await state.clear()
    await message.answer("🆕 Yangi leadlar bo‘limi", reply_markup=get_new_leads_keyboard())


@router.message(F.text == "⏳ Keyinroq bog'laniladigan leadlar")
async def later_leads_section(message: Message, state: FSMContext):
    if not is_authenticated(message.from_user.id):
        await message.answer("Iltimos, login qiling.", reply_markup=get_login_keyboard())
        return

    await state.clear()
    await message.answer("⏳ Later leadlar bo‘limi", reply_markup=get_later_leads_keyboard())


# =====================================================
# 2) COUNTS
# =====================================================

@router.message(F.text == "📊 Barcha yangi leadlar soni")
async def new_leads_count(message: Message):
    session = get_user_session(message.from_user.id)
    count = await get_new_leads_count(session["token"])
    await message.answer(f"📊 Yangi leadlar soni: {count} ta")


@router.message(F.text == "📊 Barcha later leadlar soni")
async def later_leads_count(message: Message):
    session = get_user_session(message.from_user.id)
    count = await get_later_leads_count(session["token"])
    await message.answer(f"📊 Later leadlar soni: {count} ta")


# =====================================================
# 3) “BO‘LIMI” (sub-menu) → faqat start tugmasi
# =====================================================

@router.message(F.text == BTN_NEW_SECTION)
async def open_new_leads_subsection(message: Message, state: FSMContext):
    if not is_authenticated(message.from_user.id):
        await message.answer("Iltimos, login qiling.", reply_markup=get_login_keyboard())
        return

    # qaysi tur ekanini sessionga yozib qo‘yamiz
    session = get_user_session(message.from_user.id)
    session["current_lead_type"] = "new"

    await state.clear()
    await message.answer("🆕 Yangi leadlar bo‘limi", reply_markup=get_lead_action_keyboard())


@router.message(F.text == BTN_LATER_SECTION)
async def open_later_leads_subsection(message: Message, state: FSMContext):
    if not is_authenticated(message.from_user.id):
        await message.answer("Iltimos, login qiling.", reply_markup=get_login_keyboard())
        return

    session = get_user_session(message.from_user.id)
    session["current_lead_type"] = "later"

    await state.clear()
    await message.answer("🆕 Later leadlar bo‘limi", reply_markup=get_lead_action_keyboard())


# =====================================================
# 4) ORQAGA — lead jarayonida bo‘lsa bo‘limga qaytaradi
# =====================================================

@router.message(F.text == BTN_BACK)
async def leads_back(message: Message, state: FSMContext):
    user_id = message.from_user.id

    # login bo‘lmasa
    if not is_authenticated(user_id):
        await state.clear()
        await message.answer("Iltimos, login qiling.", reply_markup=get_login_keyboard())
        return

    session = get_user_session(user_id) or {}
    current_state = await state.get_state()

    # lead flow ichida bo‘lsa → bo‘lim keyboardiga qaytadi
    if current_state in (
        LeadStates.viewing_lead.state,
        LeadStates.waiting_for_comment.state,
        LeadStates.waiting_for_status.state,
        LeadStates.confirming.state,
        LeadStates.navigating.state,
    ):
        await state.clear()
        lead_type = session.get("current_lead_type")

        if lead_type == "later":
            await message.answer("⏳ Later leadlar bo‘limi", reply_markup=get_later_leads_keyboard())
        elif lead_type == "new":
            await message.answer("🆕 Yangi leadlar bo‘limi", reply_markup=get_new_leads_keyboard())
        else:
            await message.answer("🏠 Asosiy menyu", reply_markup=get_main_menu_keyboard())
        return

    # state yo‘q bo‘lsa → asosiy menyu
    await state.clear()
    await message.answer("🏠 Asosiy menyu", reply_markup=get_main_menu_keyboard())


# =====================================================
# 5) “▶️ Aloqani boshlash”
#    - agar state YO‘Q bo‘lsa: leadlarni olib, 1-leadni ko‘rsatadi
#    - agar state viewing_lead bo‘lsa: comment so‘raydi
# =====================================================

@router.message(F.text == BTN_START_CALL)
async def start_call(message: Message, state: FSMContext):
    if not is_authenticated(message.from_user.id):
        await message.answer("Iltimos, login qiling.", reply_markup=get_login_keyboard())
        return

    current_state = await state.get_state()

    # 5.1) Agar lead ko‘rsatilgan bo‘lsa — comment bosqichiga o‘tamiz
    if current_state == LeadStates.viewing_lead.state:
        await state.set_state(LeadStates.waiting_for_comment)
        await message.answer("📝 Comment yozing (majburiy):")
        return

    # 5.2) Aks holda — lead listni olib kelamiz va 1-leadni ko‘rsatamiz
    session = get_user_session(message.from_user.id)
    lead_type = session.get("current_lead_type", "new")

    if lead_type == "later":
        leads = await get_later_leads(session["token"])
    else:
        leads = await get_new_leads(session["token"])
        lead_type = "new"

    if not leads:
        if lead_type == "later":
            await message.answer("❌ Later leadlar yo‘q", reply_markup=get_later_leads_keyboard())
        else:
            await message.answer("❌ Yangi leadlar yo‘q", reply_markup=get_new_leads_keyboard())
        return

    session["leads_list"] = leads
    session["current_lead_index"] = 0
    session["current_lead_type"] = lead_type

    await show_lead(message, state, leads[0])


# =====================================================
# 6) LEAD KO‘RSATISH
# =====================================================

async def show_lead(message: Message, state: FSMContext, lead: dict):
    await state.set_state(LeadStates.viewing_lead)
    await state.update_data(current_lead=lead, confirmed=False)

    await message.answer(
        format_lead_info(lead),
        reply_markup=get_lead_action_keyboard()
    )


async def go_next_lead(message: Message, state: FSMContext):
    session = get_user_session(message.from_user.id)
    idx = session.get("current_lead_index", 0)
    leads = session.get("leads_list", [])

    if idx + 1 < len(leads):
        session["current_lead_index"] = idx + 1
        await show_lead(message, state, leads[session["current_lead_index"]])
    else:
        await state.clear()
        session["leads_list"] = []
        session["current_lead_index"] = 0
        await message.answer("✅ Barcha leadlar tugadi", reply_markup=get_main_menu_keyboard())


async def go_prev_lead(message: Message, state: FSMContext):
    session = get_user_session(message.from_user.id)
    idx = session.get("current_lead_index", 0)
    leads = session.get("leads_list", [])

    if idx > 0:
        session["current_lead_index"] = idx - 1
        await show_lead(message, state, leads[session["current_lead_index"]])
    else:
        await message.answer("⛔ Bu birinchi lead")


# =====================================================
# 7) COMMENT (majburiy)
# =====================================================

@router.message(LeadStates.waiting_for_comment)
async def save_comment(message: Message, state: FSMContext):
    data = await state.get_data()
    lead = data["current_lead"]
    session = get_user_session(message.from_user.id)

    text = (message.text or "").strip()
    if not text:
        await message.answer("❌ Comment bo‘sh bo‘lmasin. Qaytadan yozing:")
        return

    ok = await update_lead(session["token"], lead["id"], comment=text)
    if not ok:
        await message.answer("❌ Comment saqlanmadi. Qaytadan yozing:")
        return

    lead["user_comment"] = text
    await state.update_data(current_lead=lead)

    # keyin status majburiy
    await state.set_state(LeadStates.waiting_for_status)
    await message.answer("📌 Statusni tanlang (majburiy):", reply_markup=get_status_keyboard())


# =====================================================
# 8) STATUS (bitasi majburiy)
# =====================================================

async def set_status(message: Message, state: FSMContext, status: str):
    data = await state.get_data()
    lead = data["current_lead"]
    session = get_user_session(message.from_user.id)

    ok = await update_lead(session["token"], lead["id"], status=status)
    if not ok:
        await message.answer("❌ Status saqlanmadi. Qayta tanlang:", reply_markup=get_status_keyboard())
        return

    lead["status_led"] = status
    await state.update_data(current_lead=lead)

    await state.set_state(LeadStates.confirming)
    await message.answer("✅ Tasdiqlaysizmi?", reply_markup=get_confirm_keyboard())
    await message.answer(format_lead_info(lead))


@router.message(LeadStates.waiting_for_status, F.text == BTN_LATER)
async def status_later(message: Message, state: FSMContext):
    await set_status(message, state, "later")


@router.message(LeadStates.waiting_for_status, F.text == BTN_FAILED)
async def status_failed(message: Message, state: FSMContext):
    await set_status(message, state, "failed")


@router.message(LeadStates.waiting_for_status, F.text == BTN_SUCCESS)
async def status_success(message: Message, state: FSMContext):
    await set_status(message, state, "success")


# =====================================================
# 9) CONFIRM / EDIT
# =====================================================

@router.message(LeadStates.confirming, F.text == BTN_CONFIRM)
async def confirm_lead(message: Message, state: FSMContext):
    await state.update_data(confirmed=True)
    await state.set_state(LeadStates.navigating)
    await message.answer("✅ Tasdiqlandi. Navigatsiya:", reply_markup=get_nav_keyboard())


@router.message(LeadStates.confirming, F.text == BTN_EDIT)
async def edit_lead(message: Message, state: FSMContext):
    # qaytadan comment + status kiritiladi
    await state.set_state(LeadStates.waiting_for_comment)
    await message.answer("✏️ Qaytadan comment yozing (majburiy):")


# =====================================================
# 10) NAVIGATION (NEXT / PREV)
# =====================================================

@router.message(LeadStates.navigating, F.text == BTN_NEXT)
async def manual_next(message: Message, state: FSMContext):
    data = await state.get_data()
    if not data.get("confirmed"):
        await message.answer("❗ Avval tasdiqlang.")
        return
    await go_next_lead(message, state)


@router.message(LeadStates.navigating, F.text == BTN_PREV)
async def manual_prev(message: Message, state: FSMContext):
    data = await state.get_data()
    if not data.get("confirmed"):
        await message.answer("❗ Avval tasdiqlang.")
        return
    await go_prev_lead(message, state)
