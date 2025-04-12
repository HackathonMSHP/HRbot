from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Bio


class BioRepository:

    @staticmethod
    async def create_bio(db: AsyncSession, user_id: int, about: str = "") -> Bio:
        bio = Bio(user_id=user_id, about=about)
        db.add(bio)
        await db.commit()
        await db.refresh(bio)
        return bio

    @staticmethod
    async def get_bio_by_id(db: AsyncSession, bio_id: int) -> Bio | None:
        result = await db.execute(select(Bio).where(Bio.id == bio_id))
        return result.scalars().first()

    @staticmethod
    async def get_bio_by_user_id(db: AsyncSession, user_id: int) -> Bio | None:
        result = await db.execute(select(Bio).where(Bio.user_id == user_id))
        return result.scalars().first()

    @staticmethod
    async def get_bio_by_tg_id(db: AsyncSession, tg_id: int) -> Sequence[Bio] | None:
        result = await db.execute(select(Bio).where(Bio.user_id == tg_id))
        return result.scalars().all()

    @staticmethod
    async def update_bio(db: AsyncSession, bio_id: int, about: str) -> Bio | None:
        bio = await BioRepository.get_bio_by_id(db, bio_id)
        if bio:
            bio.about = about
            await db.commit()
            await db.refresh(bio)
        return bio

    @staticmethod
    async def delete_bio(db: AsyncSession, bio_id: int) -> None:
        bio = await BioRepository.get_bio_by_id(db, bio_id)
        if bio:
            await db.delete(bio)
            await db.commit()
