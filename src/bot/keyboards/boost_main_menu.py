from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.keyboards.boost_settings import BoostSettingsData, BoostSettingsActions
from src.bot.keyboards.keyboards import Keyboard
from src.config import cfg
from src.lexicon.lexicon import LexiconMsgKbName


class BoostMainData(CallbackData, prefix="boost_main_menu"):
    boost_type: str


class BoostMainKeyboard(Keyboard):
    def __init__(self, kb_name: LexiconMsgKbName) -> None:
        super().__init__(kb_name)

    def get_kb(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        for boost_info in cfg.boost.boosts:
            boost = boost_info.split("|")
            builder.row(
                self._btn_callback(
                    btn_name=self._kb_name.boost_check.format(boost[1]),
                    callback_data=BoostMainData(boost_type=boost[0]).pack(),
                )
            )

        builder.row(
            self._btn_callback(
                btn_name=self._kb_name.boost_settings,
                callback_data=BoostSettingsData(
                    action=BoostSettingsActions.MENU
                ).pack(),
            ),
        )

        return builder.as_markup()
