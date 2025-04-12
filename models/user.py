from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    tg_id: Mapped[int] = mapped_column(unique=True, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

    # Связь 1→1 c Bio
    bio: Mapped["Bio"] = relationship(
        "Bio",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",  # при удалении юзера, удаляется его Bio
    )
