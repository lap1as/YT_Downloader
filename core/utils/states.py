from aiogram.fsm.state import State, StatesGroup


class ChoseDownloader(StatesGroup):
    download_video = State()
    download_audio = State()
