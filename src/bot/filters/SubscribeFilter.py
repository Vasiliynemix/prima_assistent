from aiogram.enums import ChatMemberStatus
from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject
from loguru import logger

from src.bot.utils import get_chat_id
from src.config import Config
from src.storage.db.models import User


class SubscribedFilter(BaseFilter):
    async def __call__(self, update: TelegramObject, cfg: Config) -> bool:
        try:
            chat_member = await update.bot.get_chat_member(
                chat_id=await get_chat_id(bot=update.bot, link=cfg.chat_link.split("/")[-1]),
                user_id=update.from_user.id,
            )
            return chat_member.status != ChatMemberStatus.LEFT and chat_member.status != ChatMemberStatus.KICKED
        except Exception as e:
            logger.exception(f"SubscribedFilter: {e}")
            return False


class SubscribedFilterSuccess(BaseFilter):
    async def __call__(self, update: TelegramObject, user: User) -> bool:
        return user.is_subscribed
