# from functools import partial
# import asyncio
# from datetime import datetime
# from aiogram.fsm.context import FSMContext
# from states import LeadLaterStates
# from aiogram import Bot, Dispatcher
# from aiogram.types import Message, CallbackQuery
# from aiogram.filters import Command
# from decouple import config
#
# from buttons import main_menu, generate_update_buttons
# from api import fetch_leads, update_lead_status
#
# TOKEN = config("TELEGRAM_BOT_TOKEN")
# bot = Bot(token=TOKEN)
# dp = Dispatcher()
#
#
# @dp.message(Command("start"))
# async def start(msg: Message):
#     await msg.answer("Kerakli bo‘limni tanlang:", reply_markup=main_menu())
#
#
# async def fetch_leads_async(endpoint: str) -> dict:
#     loop = asyncio.get_running_loop()
#     return await loop.run_in_executor(None, partial(fetch_leads, endpoint))
#
#
# async def send_leads(call: CallbackQuery, api_response: dict):
#     leads = api_response.get("data", [])
#
#     if not leads:
#         await call.message.answer("❗️ Hozircha ma’lumot yo‘q")
#         return
#
#     for item in leads:
#         text = (
#             f"🆔 ID: {item['id']}\n"
#             f"👤 Ism: {item['full_name']}\n"
#             f"📞 Telefon: {item['phone_number']}\n"
#             f"🏢 Biznes nomi: {item.get('business_name', '—')}\n"
#             f"🛠 Xizmat turi: {item.get('service_type', '—')}\n"
#             f"⏰ Qo‘ng‘iroq vaqti: {item.get('call_time', '—')}\n"
#             f"💬 Izoh: {item.get('user_comment', '—')}\n"
#         )
#         await call.message.answer(text, reply_markup=generate_update_buttons(item['id']))
#
#
# # =========================
# # Lead ko‘rsatish
# # =========================
# @dp.callback_query(lambda c: c.data == "new")
# async def show_new(call: CallbackQuery):
#     data = await fetch_leads_async("new_leds/")
#     await send_leads(call, data)
#
#
# @dp.callback_query(lambda c: c.data == "later")
# async def show_later(call: CallbackQuery):
#     data = await fetch_leads_async("later/")
#     await send_leads(call, data)
#
#
# @dp.callback_query(lambda c: c.data == "failed")
# async def show_failed(call: CallbackQuery):
#     data = await fetch_leads_async("failed/")
#     await send_leads(call, data)
#
#
# # =========================
# # Lead status update
# # =========================
# @dp.callback_query(lambda c: c.data.startswith("update_"))
# async def update_lead_status_handler(call: CallbackQuery, state: FSMContext):
#     parts = call.data.split("_")
#     lead_id = int(parts[1])
#     action = parts[2]  # later, failed, done
#
#     if action == "later":
#         # State ga lead_id saqlaymiz va komment so'raymiz
#         await state.update_data(lead_id=lead_id)
#         await call.message.answer("❗ Iltimos, lead uchun komment yozing:")
#         await LeadLaterStates.waiting_for_comment.set()
#         await call.answer()
#         return
#
#     # failed va done uchun avvalgi logika
#     user_comment = ""
#     call_time = None
#     new_status = ""
#
#     if action == "failed":
#         new_status = "FAILED"
#         user_comment = "Bizning xizmat kerak emas"
#     elif action == "done":
#         new_status = "DONE"
#         user_comment = "Klient olindi"
#         call_time = datetime.now().strftime("%Y-%m-%d %H:%M")
#
#     loop = asyncio.get_running_loop()
#     response = await loop.run_in_executor(
#         None,
#         partial(update_lead_status, lead_id, new_status, user_comment, call_time)
#     )
#
#     if response.get("success"):
#         await call.message.answer(f"Lead #{lead_id} statusi '{new_status}' ga o'zgartirildi ✅\nIzoh: {user_comment}")
#     else:
#         await call.message.answer(f"Lead #{lead_id} statusini o'zgartirishda xato ❌")
#
# @dp.message(LeadLaterStates.waiting_for_comment)
# async def process_comment(msg: Message, state: FSMContext):
#     data = await state.get_data()
#     lead_id = data["lead_id"]
#     comment = msg.text
#     new_status = "LATER"
#     call_time = datetime.now().strftime("%Y-%m-%d %H:%M")
#
#     loop = asyncio.get_running_loop()
#     response = await loop.run_in_executor(
#         None,
#         partial(update_lead_status, lead_id, new_status, comment, call_time)
#     )
#
#     if response.get("success"):
#         await msg.answer(f"✅ Lead #{lead_id} muvaffaqiyatli 'Later' ga o‘zgartirildi!\nIzoh: {comment}")
#     else:
#         await msg.answer(f"❌ Lead #{lead_id} statusini o'zgartirishda xato yuz berdi")
#
#     await state.clear()
#
#
# # ====================
# # Main loop
# # ====================
# async def main():
#     print("Bot ishga tushdi...")
#     await dp.start_polling(bot)
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
import asyncio
from handlers.start_stop import router
from handlers.leads import router_lead
from aiogram import Bot, Dispatcher
from decouple import config


TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TELEGRAM_BOT_TOKEN)

dp = Dispatcher()

async def main():

    dp.include_router(router)
    dp.include_router(router_lead)

    await dp.start_polling(bot)

asyncio.run(main())