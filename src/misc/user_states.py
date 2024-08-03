from aiogram.dispatcher.filters.state import State, StatesGroup


class UserDataInputting(StatesGroup):
    wait_for_id = State()
