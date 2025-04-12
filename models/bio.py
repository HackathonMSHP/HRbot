from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Bio(Base):
    __tablename__ = "bios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    about: Mapped[str] = mapped_column(Text, default="")
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )  # При удалении юзера, его Bio тоже удаляется

    # Обратная связь к пользователю:
    user: Mapped["User"] = relationship(
        "User",
        back_populates="bio",
        uselist=False,  # означает, что у Bio есть ровно один User, а не список
    )
