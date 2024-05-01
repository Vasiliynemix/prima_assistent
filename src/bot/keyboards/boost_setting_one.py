from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.keyboards.keyboards import Keyboard, BackToData, BackToActions
from src.lexicon.lexicon import LexiconMsgKbName


class BoostSettingOneData(CallbackData, prefix="boost_setting_one"):
    is_end: bool | None = None
    boost_type: str | None = None


class CompanySettingOneData(CallbackData, prefix="company_setting_one"):
    boost_type: str


class PersonalSettingOneData(CallbackData, prefix="personal_setting_one"):
    boost_type: str


class BoostSettingOneKeyboard(Keyboard):
    def __init__(self, kb_name: LexiconMsgKbName) -> None:
        super().__init__(kb_name)

    def get_kb(
        self, btn_name: str, back_to: BackToActions, is_end: bool = False
    ) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        if not is_end:
            builder.row(
                self._btn_callback(
                    btn_name=btn_name,
                    callback_data=BoostSettingOneData().pack(),
                )
            )

            builder.row(
                self._btn_callback(
                    btn_name=self._kb_name.back,
                    callback_data=BackToData(back_to=back_to).pack(),
                )
            )

        if back_to != BackToActions.BOOST_SETTINGS or is_end:
            builder.row(
                self._btn_callback(
                    btn_name=self._kb_name.settings_menu,
                    callback_data=BackToData(
                        back_to=BackToActions.BOOST_SETTINGS
                    ).pack(),
                )
            )

        return builder.as_markup()


class BoostSettingOneIsEndKeyboard(Keyboard):
    def __init__(self, kb_name: LexiconMsgKbName) -> None:
        super().__init__(kb_name)

    def get_kb(
        self, boost_type: str, boost_name: str, back_to: BackToActions
    ) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        builder.row(
            self._btn_callback(
                btn_name=self._kb_name.company,
                callback_data=CompanySettingOneData(boost_type=boost_type).pack(),
            )
        )

        builder.row(
            self._btn_callback(
                btn_name=self._kb_name.personal,
                callback_data=PersonalSettingOneData(boost_type=boost_type).pack(),
            )
        )

        builder.row(
            self._btn_callback(
                btn_name=self._kb_name.boost.format(boost_name),
                callback_data=BoostSettingOneData(
                    is_end=True,
                    boost_type=boost_type,
                ).pack(),
            )
        )

        builder.row(
            self._btn_callback(
                btn_name=self._kb_name.back,
                callback_data=BackToData(back_to=back_to).pack(),
            )
        )

        return builder.as_markup()
