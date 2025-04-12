import asyncio
import os
import traceback

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from utils.bot_dispatcher import create_dispatcher
from utils.db_connector import create_tables #, delete_tables, recreate_tables

load_dotenv()
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("Токен не найден. Убедитесь, что вы создали файл .env с токеном.")


async def main() -> None:
    await create_tables()  # создаем таблицы в бд
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = create_dispatcher()
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
