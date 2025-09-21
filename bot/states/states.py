from aiogram.fsm.state import StatesGroup, State


class GPTState(StatesGroup):
    choosing_style = State()
    waiting_for_input = State()


class IdeaState(StatesGroup):
    waiting_for_input = State()


class ImageState(StatesGroup):
    waiting_for_photo = State()


class IdeaState(StatesGroup):
    waiting_for_input = State()


class AlgoState(StatesGroup):
    waiting_for_name = State()
