from aiogram.types import Message, CallbackQuery

from src.bot.keyboards.boost_main_menu import BoostMainKeyboard
from src.config import cfg
from src.lexicon.lexicon import Lexicon


async def start_with_subscribe_success(
    message: Message | None,
    callback: CallbackQuery | None,
    lexicon: Lexicon,
):
    kb = BoostMainKeyboard(kb_name=lexicon.kb_name)
    if message is not None:
        await message.answer(
            text=lexicon.send.boost_main_menu,
            reply_markup=kb.get_kb(),
        )
        return

    if callback is not None:
        await callback.message.edit_text(
            text=lexicon.send.boost_main_menu,
            reply_markup=kb.get_kb(),
        )
        return


async def get_boost_name(boost_type: str) -> str:
    boost_name = ""
    for boost_info in cfg.boost.boosts:
        boost = boost_info.split("|")
        if boost[0] == boost_type:
            boost_name = boost[1]
            return boost_name

    return boost_name
