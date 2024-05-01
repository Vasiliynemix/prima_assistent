from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from loguru import logger

from src.config import cfg
from src.storage.db.db import Database
from src.storage.storage import Storage


class StorageMiddleware(BaseMiddleware):
    def __init__(self, storage: Storage) -> None:
        self.storage = storage

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: dict[str, Any],
    ) -> Any:
        try:
            async with self.storage.db.async_session() as session:
                db: Database = Database(session)
                data["db"] = db

                is_admin = False
                if event.from_user.id in cfg.admins:
                    is_admin = True

                user = await db.user.get(tg_id=event.from_user.id)
                if user is None:
                    user = await db.user.set(
                        tg_id=event.from_user.id,
                        first_name=event.from_user.first_name,
                        last_name=event.from_user.last_name,
                        username=event.from_user.username,
                        is_admin=is_admin,
                    )

                username = None
                first_name = None
                last_name = None

                if user.username != event.from_user.username:
                    username = event.from_user.username

                if user.first_name != event.from_user.first_name:
                    first_name = event.from_user.first_name

                if user.last_name != event.from_user.last_name:
                    last_name = event.from_user.last_name

                if user.is_admin == is_admin:
                    is_admin = None

                new_user = await db.user.update(
                    tg_id=event.from_user.id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    is_admin=is_admin,
                )
                if new_user is not None:
                    user = new_user

                data["user"] = user
        except Exception as e:
            logger.exception(f"Error ID: {event.from_user.id} | {type(e).__name__} | {e}")

        return await handler(event, data)
