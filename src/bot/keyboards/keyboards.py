from abc import ABC, abstractmethod
from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton

from src.lexicon.lexicon import LexiconMsgKbName


class BackToActions(Enum):
    BOOST_MAIN_MENU: str = "boost_main_menu"
    BOOST_SETTINGS: str = "boost_settings"
    BOOST_SETTINGS_REGISTER: str = "boost_settings_register"
    BOOST_SETTINGS_COMPANY: str = "boost_settings_company"
    BOOST_SETTING_PERSONAL: str = "boost_settings_personal"
    BOOST_SETTING_ALL: str = "boost_settings_all"


class BackToData(CallbackData, prefix="back_to"):
    back_to: BackToActions
    boost_type: str | None = None


class Keyboard(ABC):
    def __init__(self, kb_name: LexiconMsgKbName) -> None:
        self._kb_name = kb_name

    @abstractmethod
    def get_kb(self, **kwargs) -> InlineKeyboardMarkup:
        pass

    @staticmethod
    def _btn_link(btn_name: str, url: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(text=btn_name, url=url)

    @staticmethod
    def _btn_callback(btn_name: str, callback_data: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(text=btn_name, callback_data=callback_data)

    @staticmethod
    def _btn_message(btn_name: str) -> KeyboardButton:
        return KeyboardButton(text=btn_name)
