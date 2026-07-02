import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import settings
from handlers.customer import customer_router
from handlers.admin import admin_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(token=settings.BOT_TOKEN.get_secret_value())
    dp = Dispatcher()

    # Register our clean routers
    dp.include_router(admin_router)
    dp.include_router(customer_router)

    logger.info("SupoBot simplified worker has launched successfully.")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot application gracefully stopped.")
