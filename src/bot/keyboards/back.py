from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.keyboards.keyboards import Keyboard, BackToData, BackToActions
from src.lexicon.lexicon import LexiconMsgKbName


class BackToKeyboard(Keyboard):
    def __init__(self, kb_name: LexiconMsgKbName) -> None:
        super().__init__(kb_name)

    def get_kb(self, boost_type: str) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        builder.row(
            self._btn_callback(
                self._kb_name.back,
                BackToData(
                    back_to=BackToActions.BOOST_SETTING_ALL, boost_type=boost_type
                ).pack(),
            )
        )

        builder.row(
            self._btn_callback(
                self._kb_name.settings_menu,
                callback_data=BackToData(back_to=BackToActions.BOOST_SETTINGS).pack(),
            )
        )

        return builder.as_markup()
