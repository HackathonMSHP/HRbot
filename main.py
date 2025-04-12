import asyncio
import os
import traceback

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers.start import start_router
from handlers.employer import employer_router
from handlers.worker import worker_router
from utils.bot_dispatcher import create_dispatcher
from utils.db_connector import create_tables #, delete_tables, recreate_tables
from constants.config import TOKEN


async def main() -> None:
    await create_tables()  # создаем таблицы в бд
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = create_dispatcher()
    dp.include_routers(start_router, employer_router, worker_router)
    await dp.start_polling(bot)  # запускаем бота


if __name__ == "__main__":
    print("Стартуем бота ...")
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        # Позволяем корректно завершить программу при Ctrl+C или выходе из системы
        print("Бот остановлен!")
    except Exception:
        print(f"Ошибка!: {traceback.format_exc()}")
