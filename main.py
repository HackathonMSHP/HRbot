import asyncio
import os
import traceback

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers.start import start_router
from handlers.employer import employer_router
from handlers.worker import worker_router
#from utils.bot_dispatcher import create_dispatcher
#from utils.db_connector import create_tables #, delete_tables, recreate_tables
from constants.config import TOKEN
from data.database import *


async def main() -> None:
    await create_db()
    #bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    #dp.include_routers(start_router, employer_router, worker_router)


if __name__ == "__main__":
    print("Стартуем бота ...")
    asyncio.run(main())
