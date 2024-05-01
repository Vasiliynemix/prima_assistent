from enum import StrEnum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.keyboards.keyboards import Keyboard, BackToData, BackToActions
from src.config import cfg
from src.lexicon.lexicon import LexiconMsgKbName


class BoostSettingsActions(StrEnum):
    MENU = "menu"


class BoostSettingsData(CallbackData, prefix="boost_settings"):
    action: BoostSettingsActions | None = None
    boost_type: str | None = None


class BoostSettingsKeyboard(Keyboard):
    def __init__(self, kb_name: LexiconMsgKbName) -> None:
        super().__init__(kb_name)

    def get_kb(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        for boost_info in cfg.boost.boosts:
            boost = boost_info.split("|")
            builder.row(
                self._btn_callback(
                    btn_name=self._kb_name.boost_settings_one.format(boost[1]),
                    callback_data=BoostSettingsData(boost_type=boost[0]).pack(),
                )
            )

        builder.row(
            self._btn_callback(
                btn_name=self._kb_name.back,
                callback_data=BackToData(back_to=BackToActions.BOOST_MAIN_MENU).pack(),
            )
        )

        return builder.as_markup()
