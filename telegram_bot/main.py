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