from aiogram.fsm.state import StatesGroup, State


class GPTState(StatesGroup):
    choosing_style = State()
    waiting_for_input = State()

class IdeaState(StatesGroup):
    waiting_for_input = State()