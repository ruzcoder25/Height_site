# bot/main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from .config import BOT_TOKEN
from bot.handlers import start, login, menu, leads

# Logging sozlash
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    """Botni ishga tushirish"""
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # ✅ Routerlar tartibi juda muhim:
    # - leads router "⬅️ Orqaga" va lead flow state-larini ushlaydi
    # - menu router umumiy back/logout kabi narsalarni ushlaydi
    dp.include_router(start.router)
    dp.include_router(login.router)
    dp.include_router(leads.router)  # ✅ oldin
    dp.include_router(menu.router)   # ✅ keyin

    logger.info("Bot ishga tushmoqda...")

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
