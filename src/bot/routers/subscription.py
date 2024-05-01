from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.filters.SubscribeFilter import SubscribedFilter
from src.bot.keyboards.subscription import SubscriptionData
from src.bot.routers.utils import start_with_subscribe_success
from src.bot.states.states import SubscribeState
from src.lexicon.lexicon import Lexicon
from src.storage.db.db import Database
from src.storage.db.models import User

router = Router()


@router.callback_query(SubscriptionData.filter(), SubscribedFilter())
@router.callback_query(SubscriptionData.filter(), SubscribeState.one)
async def subscription_success(
    callback: CallbackQuery,
    db: Database,
    user: User,
    lexicon: Lexicon,
):
    if not user.is_subscribed:
        await db.user.update(tg_id=callback.from_user.id, is_subscribed=True)

    await start_with_subscribe_success(
        message=None,
        callback=callback,
        lexicon=lexicon,
    )


@router.callback_query(SubscriptionData.filter())
async def subscription_fail(
    callback: CallbackQuery,
    lexicon: Lexicon,
    state: FSMContext,
):
    await state.set_state(SubscribeState.one)
    await callback.answer(lexicon.send.subscription_fail, show_alert=True)
