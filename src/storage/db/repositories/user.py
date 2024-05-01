from datetime import datetime, timedelta

from loguru import logger
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.storage.db.models import User


class UserRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def set(
        self,
        tg_id: int,
        first_name: str,
        last_name: str,
        username: str,
        is_admin: bool,
    ) -> User | None:
        try:
            stmt = (
                insert(User)
                .values(
                    tg_id=tg_id,
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    is_admin=is_admin,
                )
                .returning(User)
            )
            user = await self.session.scalar(stmt)
            await self.session.commit()
            logger.info(f"User {tg_id} added to DB")
            return user
        except Exception as e:
            logger.error(f"Error while adding user to DB: {e}")
            return None

    async def get(self, tg_id: int) -> User | None:
        try:
            stmt = select(User).where(User.tg_id == tg_id)
            return await self.session.scalar(stmt)
        except Exception as e:
            logger.error(f"Error while getting user from DB: {e}")
            return None

    async def update(self, tg_id: int, **kwargs) -> User | None:
        try:
            new_kwargs = await self.__delete_nulls(kwargs)
            if new_kwargs == {}:
                return None
            stmt = (
                update(User)
                .where(User.tg_id == tg_id)
                .values(**new_kwargs)
                .returning(User)
            )
            user = await self.session.scalar(stmt)
            await self.session.commit()
            logger.info(f"User {tg_id} updated in DB - {new_kwargs}")
            return user
        except Exception as e:
            logger.error(f"Error while updating user in DB: {e}")
            return None

    @staticmethod
    async def __delete_nulls(kwargs: dict) -> dict:
        new_kwargs = {}
        for k, v in kwargs.items():
            if v is not None:
                new_kwargs[k] = v
        return new_kwargs
