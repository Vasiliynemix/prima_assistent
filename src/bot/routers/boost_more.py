from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from src.bot.keyboards.boost_main_menu import BoostMainData, BoostMainKeyboard
from src.bot.routers.utils import get_boost_name
from src.config import cfg
from src.lexicon.lexicon import Lexicon

router = Router()


@router.callback_query(BoostMainData.filter())
async def boost_more(
    callback: CallbackQuery, lexicon: Lexicon, callback_data: BoostMainData
):
    boost_type = callback_data.boost_type
    video_link = ""
    if boost_type == "ak_24":
        video_link = cfg.video_link.about_ak_24
    elif boost_type == "guard":
        video_link = cfg.video_link.about_guard
    elif boost_type == "helper":
        video_link = cfg.video_link.about_helper
    elif boost_type == "site":
        video_link = cfg.video_link.about_site

    boost_name = await get_boost_name(boost_type)

    if video_link == "":
        await callback.answer(
            lexicon.errors.video_not_found.format(boost_name), show_alert=True, cache_time=5
        )
        return

    await callback.message.edit_reply_markup(reply_markup=None)

    boost_name = await get_boost_name(boost_type)
    await callback.message.answer(
        text=lexicon.send.boost_info_one.format(boost_name=boost_name, video_link=video_link),
        parse_mode=ParseMode.HTML,
    )

    await callback.message.answer(
        text=lexicon.send.boost_main_menu,
        reply_markup=BoostMainKeyboard(kb_name=lexicon.kb_name).get_kb(),
    )
