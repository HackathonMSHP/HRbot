import aiosqlite
from aiogram import Bot, Dispatcher, types

# Инициализация базы данных
async def init_db():
    async with aiosqlite.connect('users.db') as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users
                            (id INTEGER PRIMARY KEY, 
                             username TEXT,
                             full_name TEXT,
                             class TEXT)''')
        await db.commit()

# Сохранение пользователя
async def save_user(user: types.User, user_class: str):
    async with aiosqlite.connect('users.db') as db:
        await db.execute("INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?)",
                        (user.id, user.username, user.full_name, user_class))
        await db.commit()

# Получение пользователя
async def get_user(user_id: int):
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute("SELECT * FROM users WHERE id=?", (user_id,))
        return await cursor.fetchone()

# Пример использования в хэндлере
async def start_handler(message: types.Message):
    await save_user(message.from_user, "premium")
    user = await get_user(message.from_user.id)
    await message.answer(f"Ваши данные сохранены: {user}")