import aiosqlite
import json
import asyncio
from aiogram import types

DB_NAME = 'work_db.db'

async def create_db():
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
                tags TEXT, 
                likes TEXT, 
                was_likes TEXT,
                skipped TEXT
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
                need_tags TEXT,
                likes TEXT, 
                was_likes TEXT,
                skipped TEXT
            )
        ''')
        await db.commit()

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
    was_likes: list = None,
    skipped: list = None
):
    likes = likes or []
    was_likes = was_likes or []
    skipped = skipped or []
    
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            '''
            INSERT INTO workers (
                id, name, age, sphere, gender, about, status,
                work_experience, tags, likes, was_likes, skipped
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                was_likes = excluded.was_likes,
                skipped = excluded.skipped
            ''',
            (
                worker_id, name, age, sphere, gender, about, status,
                work_experience, json.dumps(tags), json.dumps(likes), 
                json.dumps(was_likes), json.dumps(skipped)
            )
        )
        await db.commit()

async def get_worker(worker_id: int) -> dict:
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
                "was_likes": json.loads(row[10]),
                "skipped": json.loads(row[11])
            }
        return None

async def add_to_worker_skipped(worker_id: int, skipped_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute('SELECT skipped FROM workers WHERE id = ?', (worker_id,))
        row = await cursor.fetchone()
        current_skipped = json.loads(row[0]) if row and row[0] else []
        
        if skipped_id not in current_skipped:
            current_skipped.append(skipped_id)
            await db.execute(
                'UPDATE workers SET skipped = ? WHERE id = ?',
                (json.dumps(current_skipped), worker_id)
            )
            await db.commit()
            return True
        return False

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
    was_likes: list = None,
    skipped: list = None
):
    likes = likes or []
    was_likes = was_likes or []
    skipped = skipped or []
    
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            '''
            INSERT INTO employers (
                id, name_company, age_min, age_max, sphere, gender, status,
                work_experience_min, work_experience_max, need_tags, likes, was_likes, skipped
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                was_likes = excluded.was_likes,
                skipped = excluded.skipped
            ''',
            (
                employer_id, name_company, age_min, age_max, sphere, gender, status,
                work_experience_min, work_experience_max, json.dumps(need_tags),
                json.dumps(likes), json.dumps(was_likes), json.dumps(skipped)
            )
        )
        await db.commit()

async def get_employer(employer_id: int) -> dict:
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
                "was_likes": json.loads(row[11]),
                "skipped": json.loads(row[12])
            }
        return None

async def add_to_employer_skipped(employer_id: int, skipped_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute('SELECT skipped FROM employers WHERE id = ?', (employer_id,))
        row = await cursor.fetchone()
        current_skipped = json.loads(row[0]) if row and row[0] else []
        
        if skipped_id not in current_skipped:
            current_skipped.append(skipped_id)
            await db.execute(
                'UPDATE employers SET skipped = ? WHERE id = ?',
                (json.dumps(current_skipped), employer_id)
            )
            await db.commit()
            return True
        return False

async def get_all_active_workers():
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
                "was_likes": json.loads(row[10]),
                "skipped": json.loads(row[11])
            }
            for row in rows
        ]

async def get_all_active_employers():
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
                "was_likes": json.loads(row[11]),
                "skipped": json.loads(row[12])
            }
            for row in rows
        ]