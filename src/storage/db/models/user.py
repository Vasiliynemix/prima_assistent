from sqlalchemy import BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from src.storage.db.models.base import Base


class User(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)

    is_subscribed: Mapped[bool] = mapped_column(nullable=False, default=False)

    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)

    is_end: Mapped[bool] = mapped_column(nullable=False, default=False)
