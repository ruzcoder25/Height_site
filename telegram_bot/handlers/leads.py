from aiogram import types, Router
from aiogram import F

from telegram_bot.api import get_new_leads, get_later_leads
from telegram_bot.buttons import lead_inline_kb
from aiogram.types.callback_query import CallbackQuery


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
            await message.answer(text, reply_markup=lead_inline_kb(lead['id']))

    else:
        await message.answer("Hozircha yangi buyurtmalar mavjud emas")

@router_lead.message(F.text=="Laret Leads")
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
            await message.answer(text, reply_markup=lead_inline_kb(lead['id']))
    else:
        await message.answer("Keynroq gaplashish uchun buyurtmalar rejalashtirilmagan")




# CallBack handlers

@router_lead.callback_query(lambda c: c.data and c.data.startswith("later:"))
async def update_later_lead(query: CallbackQuery):
    lead_id = query.data.split(":")[1]  # ID ni olish
    await query.answer(f"Later lead {lead_id} tanlandi")

@router_lead.callback_query(lambda c: c.data and c.data.startswith("failed:"))
async def update_failed_lead(query: CallbackQuery):
    lead_id = query.data.split(":")[1]  # ID ni olish
    await query.answer(f"Failed lead {lead_id} tanlandi")








