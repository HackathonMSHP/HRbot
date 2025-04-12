from typing import Sequence

from sqlalchemy import select  # , delete, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import User


class UserRepository:

    @staticmethod
    async def create_user(db: AsyncSession, tg_username: str, tg_id: int) -> User:
        user = User(tg_username=tg_username, tg_id=tg_id)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    @staticmethod
    async def get_user_by_tg_id(
        db: AsyncSession, tg_id: int, with_relations=False
    ) -> User | None:
        if not with_relations:
            result = await db.execute(select(User).where(User.tg_id == tg_id))
        else:
            result = await db.execute(
                select(User)
                .where(User.tg_id == tg_id)
                .options(
                    selectinload(User.bio),

                )
            )
        return result.scalars().first()

    @staticmethod
    async def get_all_users(db: AsyncSession) -> Sequence[User]:
        result = await db.execute(select(User))
        return result.scalars().all()

    @staticmethod
    async def update_user(
        db: AsyncSession, user_id: int, tg_username: str
    ) -> User | None:
        user = await UserRepository.get_user_by_id(db, user_id)
        if user:
            user.tg_username = tg_username
            await db.commit()
            await db.refresh(user)
        return user

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int) -> None:
        user = await UserRepository.get_user_by_id(db, user_id)
        if user:
            await db.delete(user)
            await db.commit()
