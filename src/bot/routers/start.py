from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.filters.SubscribeFilter import SubscribedFilterSuccess
from src.bot.keyboards.subscription import SubscriptionKeyboard
from src.bot.routers.utils import start_with_subscribe_success
from src.lexicon.lexicon import Lexicon

router = Router()


@router.message(CommandStart(), SubscribedFilterSuccess())
async def cmd_start_is_subscribed(
    message: Message,
    lexicon: Lexicon,
    state: FSMContext,
):
    await state.clear()
    await start_with_subscribe_success(
        message=message,
        callback=None,
        lexicon=lexicon,
    )


@router.message(CommandStart())
async def cmd_start_is_not_subscribed(
    message: Message,
    lexicon: Lexicon,
    state: FSMContext,
):
    await state.clear()
    kb = SubscriptionKeyboard(kb_name=lexicon.kb_name)
    await message.answer(
        text=lexicon.send.start_subscription,
        reply_markup=kb.get_kb(),
    )
