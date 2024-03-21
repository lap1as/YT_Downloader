from aiogram.fsm.state import State, StatesGroup


class StepsVideoDownloader(StatesGroup):
    wait_for_url = State()
    received_url = State()





