import aiosqlite
import json
import asyncio
from aiogram import types

DB_NAME = 'work_db.db'

async def create_db():
    """Создание таблиц при первом запуске"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS workers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                sphere TEXT,
                gender TEXT,
                about TEXT,
                status TEXT DEFAULT 'pause',
                work_experience INTEGER,
                tags TEXT,  # JSON массив
                likes TEXT,  # JSON массив
                was_likes TEXT  # JSON массив
            )
        ''')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS employers (
                id INTEGER PRIMARY KEY,
                name_company TEXT,
                age_min INTEGER,
                age_max INTEGER,
                sphere TEXT,
                gender TEXT,
                status TEXT DEFAULT 'pause',
                work_experience_min INTEGER,
                work_experience_max INTEGER,
                need_tags TEXT,  # JSON массив
                likes TEXT,      # JSON массив
                was_likes TEXT   # JSON массив
            )
        ''')
        await db.commit()

# ========== Worker CRUD Operations ==========

async def add_worker(
    worker_id: int,
    name: str,
    age: int,
    sphere: str,
    gender: str,
    about: str,
    work_experience: int,
    tags: list,
    status: str = "pause",
    likes: list = None,
    was_likes: list = None
):
    likes = likes or []
    was_likes = was_likes or []
    
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            '''
            INSERT INTO workers (
                id, name, age, sphere, gender, about, status,
                work_experience, tags, likes, was_likes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name = excluded.name,
                age = excluded.age,
                sphere = excluded.sphere,
                gender = excluded.gender,
                about = excluded.about,
                status = excluded.status,
                work_experience = excluded.work_experience,
                tags = excluded.tags,
                likes = excluded.likes,
                was_likes = excluded.was_likes
            ''',
            (
                worker_id, name, age, sphere, gender, about, status,
                work_experience, json.dumps(tags), json.dumps(likes), json.dumps(was_likes)
            )
        )
        await db.commit()

async def get_worker(worker_id: int) -> dict:
    """Получение информации о работнике"""
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute('SELECT * FROM workers WHERE id = ?', (worker_id,))
        row = await cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "name": row[1],
                "age": row[2],
                "sphere": row[3],
                "gender": row[4],
                "about": row[5],
                "status": row[6],
                "work_experience": row[7],
                "tags": json.loads(row[8]),
                "likes": json.loads(row[9]),
                "was_likes": json.loads(row[10])
            }
        return None

async def update_worker_status(worker_id: int, new_status: str):
    """Обновление статуса работника"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'UPDATE workers SET status = ? WHERE id = ?',
            (new_status, worker_id)
        )
        await db.commit()

async def add_to_worker_likes(worker_id: int, liked_id: int):
    """Добавляем ID в likes работника"""
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute('SELECT likes FROM workers WHERE id = ?', (worker_id,))
        row = await cursor.fetchone()
        current_likes = json.loads(row[0]) if row and row[0] else []
        
        if liked_id not in current_likes:
            current_likes.append(liked_id)
            await db.execute(
                'UPDATE workers SET likes = ? WHERE id = ?',
                (json.dumps(current_likes), worker_id)
            )
            await db.commit()
            return True
        return False

async def add_to_worker_was_likes(worker_id: int, liked_by_id: int):
    """Добавляем ID в was_likes работника"""
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute('SELECT was_likes FROM workers WHERE id = ?', (worker_id,))
        row = await cursor.fetchone()
        current_was_likes = json.loads(row[0]) if row and row[0] else []
        
        if liked_by_id not in current_was_likes:
            current_was_likes.append(liked_by_id)
            await db.execute(
                'UPDATE workers SET was_likes = ? WHERE id = ?',
                (json.dumps(current_was_likes), worker_id)
            )
            await db.commit()
            return True
        return False

# ========== Employer CRUD Operations ==========

async def add_employer(
    employer_id: int,
    name_company: str,
    age_min: int,
    age_max: int,
    sphere: str,
    gender: str,
    work_experience_min: int,
    work_experience_max: int,
    need_tags: list,
    status: str = "pause",
    likes: list = None,
    was_likes: list = None
):
    """Добавление/обновление работодателя"""
    likes = likes or []
    was_likes = was_likes or []
    
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            '''
            INSERT INTO employers (
                id, name_company, age_min, age_max, sphere, gender, status,
                work_experience_min, work_experience_max, need_tags, likes, was_likes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name_company = excluded.name_company,
                age_min = excluded.age_min,
                age_max = excluded.age_max,
                sphere = excluded.sphere,
                gender = excluded.gender,
                status = excluded.status,
                work_experience_min = excluded.work_experience_min,
                work_experience_max = excluded.work_experience_max,
                need_tags = excluded.need_tags,
                likes = excluded.likes,
                was_likes = excluded.was_likes
            ''',
            (
                employer_id, name_company, age_min, age_max, sphere, gender, status,
                work_experience_min, work_experience_max, json.dumps(need_tags),
                json.dumps(likes), json.dumps(was_likes)
            )
        )
        await db.commit()

async def get_employer(employer_id: int) -> dict:
    """Получение информации о работодателе"""
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute('SELECT * FROM employers WHERE id = ?', (employer_id,))
        row = await cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "name_company": row[1],
                "age_min": row[2],
                "age_max": row[3],
                "sphere": row[4],
                "gender": row[5],
                "status": row[6],
                "work_experience_min": row[7],
                "work_experience_max": row[8],
                "need_tags": json.loads(row[9]),
                "likes": json.loads(row[10]),
                "was_likes": json.loads(row[11])
            }
        return None

async def add_to_employer_likes(employer_id: int, liked_id: int):
    """Добавляем ID в likes работодателя"""
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute('SELECT likes FROM employers WHERE id = ?', (employer_id,))
        row = await cursor.fetchone()
        current_likes = json.loads(row[0]) if row and row[0] else []
        
        if liked_id not in current_likes:
            current_likes.append(liked_id)
            await db.execute(
                'UPDATE employers SET likes = ? WHERE id = ?',
                (json.dumps(current_likes), employer_id)
            )
            await db.commit()
            return True
        return False

async def add_to_employer_was_likes(employer_id: int, liked_by_id: int):
    """Добавляем ID в was_likes работодателя"""
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute('SELECT was_likes FROM employers WHERE id = ?', (employer_id,))
        row = await cursor.fetchone()
        current_was_likes = json.loads(row[0]) if row and row[0] else []
        
        if liked_by_id not in current_was_likes:
            current_was_likes.append(liked_by_id)
            await db.execute(
                'UPDATE employers SET was_likes = ? WHERE id = ?',
                (json.dumps(current_was_likes), employer_id)
            )
            await db.commit()
            return True
        return False

# ========== Common Operations ==========

async def get_all_active_workers():
    """Получение всех активных работников"""
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM workers WHERE status = 'active'")
        rows = await cursor.fetchall()
        return [
            {
                "id": row[0],
                "name": row[1],
                "age": row[2],
                "sphere": row[3],
                "gender": row[4],
                "about": row[5],
                "status": row[6],
                "work_experience": row[7],
                "tags": json.loads(row[8]),
                "likes": json.loads(row[9]),
                "was_likes": json.loads(row[10])
            }
            for row in rows
        ]

async def get_all_active_employers():
    """Получение всех активных работодателей"""
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM employers WHERE status = 'active'")
        rows = await cursor.fetchall()
        return [
            {
                "id": row[0],
                "name_company": row[1],
                "age_min": row[2],
                "age_max": row[3],
                "sphere": row[4],
                "gender": row[5],
                "status": row[6],
                "work_experience_min": row[7],
                "work_experience_max": row[8],
                "need_tags": json.loads(row[9]),
                "likes": json.loads(row[10]),
                "was_likes": json.loads(row[11])
            }
            for row in rows
        ]
