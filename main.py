import asyncio
import os
import traceback

from aiogram import Bot,Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers.start import start_router
from handlers.employer import employer_router
from handlers.worker import worker_router
#from utils.bot_dispatcher import create_dispatcher
#from utils.db_connector import create_tables #, delete_tables, recreate_tables
from constants.config import TOKEN


async def main() -> None:
    dp = Dispatcher()
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_routers(start_router, employer_router, worker_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Стартуем бота ...")
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен!")     
    except Exception:
        print(f"Ошибка!: {traceback.format_exc()}")
