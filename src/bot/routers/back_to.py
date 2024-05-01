from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.keyboards.boost_main_menu import BoostMainKeyboard
from src.bot.keyboards.boost_setting_one import (
    BoostSettingOneKeyboard,
    BoostSettingOneIsEndKeyboard,
)
from src.bot.keyboards.boost_settings import BoostSettingsKeyboard
from src.bot.keyboards.keyboards import BackToData, BackToActions
from src.bot.routers.utils import get_boost_name
from src.bot.states.states import SettingsState
from src.config import cfg
from src.lexicon.lexicon import Lexicon

router = Router()


@router.callback_query(BackToData.filter(F.back_to == BackToActions.BOOST_MAIN_MENU))
async def back_to_main_menu(
    callback: CallbackQuery, lexicon: Lexicon, state: FSMContext
):
    await state.clear()
    await callback.message.edit_text(
        text=lexicon.send.boost_main_menu,
        reply_markup=BoostMainKeyboard(kb_name=lexicon.kb_name).get_kb(),
    )


@router.callback_query(BackToData.filter(F.back_to == BackToActions.BOOST_SETTINGS))
async def back_to_settings_menu(
    callback: CallbackQuery, lexicon: Lexicon, state: FSMContext
):
    await state.clear()
    await callback.message.edit_text(
        text=lexicon.send.boost_settings,
        reply_markup=BoostSettingsKeyboard(kb_name=lexicon.kb_name).get_kb(),
    )


@router.callback_query(
    BackToData.filter(F.back_to == BackToActions.BOOST_SETTINGS_REGISTER)
)
async def back_to_settings_menu(
    callback: CallbackQuery, lexicon: Lexicon, state: FSMContext
):
    await state.set_state(SettingsState.register)
    kb = BoostSettingOneKeyboard(kb_name=lexicon.kb_name)
    await callback.message.edit_text(
        text=lexicon.send.register.format(link=cfg.site_link),
        reply_markup=kb.get_kb(
            btn_name=lexicon.kb_name.register,
            back_to=BackToActions.BOOST_SETTINGS,
        ),
    )


@router.callback_query(BackToData.filter(F.back_to == BackToActions.BOOST_SETTING_ALL))
async def back_to_settings_menu(
    callback: CallbackQuery,
    lexicon: Lexicon,
    callback_data: BackToData,
):
    boost_name = await get_boost_name(callback_data.boost_type)
    await callback.message.edit_text(
        text=lexicon.send.is_end_boost.format(link=cfg.site_link, boost_name=boost_name),
        reply_markup=BoostSettingOneIsEndKeyboard(kb_name=lexicon.kb_name).get_kb(
            boost_type=callback_data.boost_type,
            boost_name=boost_name,
            back_to=BackToActions.BOOST_SETTINGS,
        ),
    )
