from aiogram.fsm.state import StatesGroup, State


class SubscribeState(StatesGroup):
    one = State()
    two = State()


class SettingsState(StatesGroup):
    register = State()
    company = State()
    personal = State()
    boost = State()
