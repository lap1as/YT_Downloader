from aiogram.fsm.state import State, StatesGroup


class StepsVideoDownloader(StatesGroup):
    GET_VIDEO_URL = State()