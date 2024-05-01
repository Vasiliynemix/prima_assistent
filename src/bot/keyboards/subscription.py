from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.keyboards.keyboards import Keyboard
from src.config import cfg
from src.lexicon.lexicon import LexiconMsgKbName


class SubscriptionData(CallbackData, prefix="subscription"):
    pass


class SubscriptionKeyboard(Keyboard):
    def __init__(self, kb_name: LexiconMsgKbName) -> None:
        super().__init__(kb_name)

    def get_kb(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        builder.row(self._btn_link(self._kb_name.subscribe, cfg.chat_link))
        builder.row(
            self._btn_callback(
                self._kb_name.check_subscription,
                SubscriptionData().pack(),
            )
        )

        return builder.as_markup()
