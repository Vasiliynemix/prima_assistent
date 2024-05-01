from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.keyboards.back import BackToKeyboard
from src.bot.keyboards.boost_setting_one import (
    BoostSettingOneKeyboard,
    BoostSettingOneData,
    BoostSettingOneIsEndKeyboard,
    CompanySettingOneData,
    PersonalSettingOneData,
)
from src.bot.keyboards.boost_settings import (
    BoostSettingsData,
    BoostSettingsKeyboard,
    BoostSettingsActions,
)
from src.bot.keyboards.keyboards import BackToActions, BackToData
from src.bot.routers.utils import get_boost_name
from src.bot.states.states import SettingsState
from src.config import cfg
from src.lexicon.lexicon import Lexicon
from src.storage.db.db import Database
from src.storage.db.models import User

router = Router()


@router.callback_query(BoostSettingsData.filter(F.action == BoostSettingsActions.MENU))
async def boost_settings(callback: CallbackQuery, lexicon: Lexicon, state: FSMContext):
    await state.clear()
    kb = BoostSettingsKeyboard(kb_name=lexicon.kb_name)
    await callback.message.edit_text(
        text=lexicon.send.boost_settings,
        reply_markup=kb.get_kb(),
    )


@router.callback_query(CompanySettingOneData.filter())
async def company_setting_one_is_end(
    callback: CallbackQuery,
    lexicon: Lexicon,
    callback_data: CompanySettingOneData,
):
    boost_type = callback_data.boost_type

    await callback.message.delete()

    # TODO: Add company instruction
    await callback.message.answer(
        text=lexicon.errors.instruction_not_ready.format("настройки компании"),
        reply_markup=BackToKeyboard(kb_name=lexicon.kb_name).get_kb(
            boost_type=boost_type,
        ),
    )


@router.callback_query(PersonalSettingOneData.filter())
async def personal_setting_one_is_end(
    callback: CallbackQuery,
    lexicon: Lexicon,
    callback_data: PersonalSettingOneData,
):
    boost_type = callback_data.boost_type

    await callback.message.delete()

    # TODO: Add personal instruction
    await callback.message.answer(
        text=lexicon.errors.instruction_not_ready.format("настройки персонала"),
        reply_markup=BackToKeyboard(kb_name=lexicon.kb_name).get_kb(
            boost_type=boost_type,
        ),
    )


@router.callback_query(BoostSettingsData.filter())
async def boost_settings_one(
    callback: CallbackQuery,
    lexicon: Lexicon,
    callback_data: BoostSettingsData,
    state: FSMContext,
    user: User,
):
    await state.update_data(boost_type=callback_data.boost_type)

    if not user.is_end:
        await state.set_state(SettingsState.register)
        kb = BoostSettingOneKeyboard(kb_name=lexicon.kb_name)
        await callback.message.edit_text(
            text=lexicon.send.register.format(link=cfg.site_link),
            reply_markup=kb.get_kb(
                btn_name=lexicon.kb_name.register,
                back_to=BackToActions.BOOST_SETTINGS,
            ),
        )
        return

    boost_name = await get_boost_name(callback_data.boost_type)
    await callback.message.edit_text(
        text=lexicon.send.is_end_boost.format(link=cfg.site_link, boost_name=boost_name),
        reply_markup=BoostSettingOneIsEndKeyboard(kb_name=lexicon.kb_name).get_kb(
            boost_type=callback_data.boost_type,
            boost_name=boost_name,
            back_to=BackToActions.BOOST_SETTINGS,
        ),
    )


@router.callback_query(BoostSettingOneData.filter(F.is_end == True))
async def boost_settings_one_is_end(
    callback: CallbackQuery,
    callback_data: BoostSettingOneData,
    lexicon: Lexicon,
):
    boost_type = callback_data.boost_type
    boost_name = await get_boost_name(boost_type)

    await callback.message.delete()

    # TODO: Add boost all
    await callback.message.answer(
        text=lexicon.errors.instruction_not_ready.format(
            f"настройки буста {boost_name}"
        ),
        reply_markup=BackToKeyboard(kb_name=lexicon.kb_name).get_kb(
            boost_type=boost_type,
        ),
    )


@router.callback_query(BoostSettingOneData.filter(), SettingsState.register)
@router.callback_query(
    BackToData.filter(F.back_to == BackToActions.BOOST_SETTINGS_COMPANY)
)
async def register(callback: CallbackQuery, lexicon: Lexicon, state: FSMContext):
    await state.set_state(SettingsState.company)
    await callback.message.delete()

    kb = BoostSettingOneKeyboard(kb_name=lexicon.kb_name)

    await callback.message.answer(text=lexicon.send.company)

    # TODO: Add company instruction
    await callback.message.answer(
        text=lexicon.errors.instruction_not_ready.format("настройки компании"),
        reply_markup=kb.get_kb(
            btn_name=lexicon.kb_name.continue_btn,
            back_to=BackToActions.BOOST_SETTINGS_REGISTER,
        ),
    )


@router.callback_query(BoostSettingOneData.filter(), SettingsState.company)
@router.callback_query(
    BackToData.filter(F.back_to == BackToActions.BOOST_SETTING_PERSONAL)
)
async def company(callback: CallbackQuery, lexicon: Lexicon, state: FSMContext):
    await state.set_state(SettingsState.personal)
    await callback.message.delete()

    kb = BoostSettingOneKeyboard(kb_name=lexicon.kb_name)

    await callback.message.answer(text=lexicon.send.personal)

    # TODO: Add personal instruction
    await callback.message.answer(
        text=lexicon.errors.instruction_not_ready.format("настройки персонала"),
        reply_markup=kb.get_kb(
            btn_name=lexicon.kb_name.continue_btn,
            back_to=BackToActions.BOOST_SETTINGS_COMPANY,
        ),
    )


@router.callback_query(BoostSettingOneData.filter(), SettingsState.personal)
async def personal(callback: CallbackQuery, lexicon: Lexicon, state: FSMContext):
    await state.set_state(SettingsState.boost)
    await callback.message.delete()

    kb = BoostSettingOneKeyboard(kb_name=lexicon.kb_name)

    data = await state.get_data()
    boost_type = data.get("boost_type")
    boost_name = await get_boost_name(boost_type)

    await callback.message.answer(text=lexicon.send.boost.format(boost_name))

    # TODO: Add boost all
    await callback.message.answer(
        text=lexicon.errors.instruction_not_ready.format(
            f"настройки буста {boost_name}"
        ),
        reply_markup=kb.get_kb(
            btn_name=lexicon.kb_name.continue_btn,
            back_to=BackToActions.BOOST_SETTING_PERSONAL,
        ),
    )


@router.callback_query(BoostSettingOneData.filter(), SettingsState.boost)
async def boost(
    callback: CallbackQuery, lexicon: Lexicon, state: FSMContext, db: Database
):
    data = await state.get_data()
    boost_type = data.get("boost_type")
    boost_name = await get_boost_name(boost_type)

    kb = BoostSettingOneKeyboard(kb_name=lexicon.kb_name)

    await callback.message.edit_text(
        text=lexicon.send.end_boost.format(boost_name),
        reply_markup=kb.get_kb(
            btn_name=lexicon.kb_name.settings_menu,
            back_to=BackToActions.BOOST_SETTINGS,
            is_end=True,
        ),
    )

    await db.user.update(tg_id=callback.from_user.id, is_end=True)
    await state.clear()
