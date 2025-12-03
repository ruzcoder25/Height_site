from aiogram import types, Router
from aiogram import F

from telegram_bot.api import get_new_leads, get_later_leads
from telegram_bot.buttons import new_inline_button
# from aiogram.types.callback_query import CallbackQuery


router_lead = Router()


@router_lead.message(F.text=="New Leads")
async def leads(message: types.Message):

    response = await get_new_leads()
    leads = response if isinstance(response, list) else response.get("data", [])
    if leads:
        for lead in leads:
            text = (
                f"🆔 ID: {lead['id']}\n\n\n"
                f"👤 Ism: {lead['full_name']}\n"
                f"📞 Telefon: {lead['phone_number']}\n"
                f"🏢 Biznes nomi: {lead.get('business_name', '—')}\n"
                f"🛠 Xizmat turi: {lead.get('service_type', '—')}\n"
                f"⏰ Qo‘ng‘iroq vaqti: {lead.get('call_time', '—')}\n"
                f"💬 Izoh: {lead.get('user_comment', '—')}\n"
            )
            await message.answer(text, reply_markup=new_inline_button)

    else:
        await message.answer("Hozircha yangi buyurtmalar mavjud emas")

@router_lead.message(F.text=="Later Leads")
async def leads(message: types.Message):
    response = await get_later_leads()
    leads = response if isinstance(response, list) else response.get("data", [])
    if leads:
        for lead in leads:
            text = (
                f"🆔 ID: {lead['id']}\n\n\n"
                f"👤 Ism: {lead['full_name']}\n"
                f"📞 Telefon: {lead['phone_number']}\n"
                f"🏢 Biznes nomi: {lead.get('business_name', '—')}\n"
                f"🛠 Xizmat turi: {lead.get('service_type', '—')}\n"
                f"⏰ Qo‘ng‘iroq vaqti: {lead.get('call_time', '—')}\n"
                f"💬 Izoh: {lead.get('user_comment', '—')}\n"
            )
            await message.answer(text, reply_markup=new_inline_button)
    else:
        await message.answer("Keynroq gaplashish uchun buyurtmalar rejalashtirilmagan")




















