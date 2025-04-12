import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

import models

load_dotenv()
DB_NAME = os.getenv("DB_NAME")


engine = create_async_engine(
    url=f"sqlite+aiosqlite:///{DB_NAME}?foreign_keys=on", echo=False
)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)


async def recreate_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.User.metadata.drop_all)
        await conn.run_sync(models.User.metadata.create_all)
