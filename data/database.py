import aiosqlite
from aiogram import types

DB_NAME = 'users.db'

async def create_db():
    """Создание таблиц при первом запуске"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                user_class TEXT,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()

async def add_user(user: types.User, user_class: str):
    """Добавление нового пользователя"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            '''
            INSERT INTO users (id, username, full_name, user_class)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                username = excluded.username,
                full_name = excluded.full_name,
                user_class = excluded.user_class
            ''',
            (user.id, user.username, user.full_name, user_class)
        )
        await db.commit()

async def get_user(user_id: int):
    """Получение пользователя по ID"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT * FROM users WHERE id = ?', (user_id,)) as cursor:
            return await cursor.fetchone()

async def update_user_class(user_id: int, new_class: str):
    """Обновление класса пользователя"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'UPDATE users SET user_class = ? WHERE id = ?',
            (new_class, user_id)
        )
        await db.commit()

async def get_users_by_class(user_class: str):
    """Получение всех пользователей определенного класса"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT * FROM users WHERE user_class = ?', (user_class,)) as cursor:
            return await cursor.fetchall()