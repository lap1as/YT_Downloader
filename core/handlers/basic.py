from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import logging

from core.utils.states import StepsVideoDownloader
from core.keyboards.create_download_keyboard import repy_keyboard


async def get_start(message: Message):
    await message.answer("Hi! I'm YouTube Downloader!", reply_markup=repy_keyboard)

async def waiting_for_url(message: Message):
    await message.answer("Send me a URL!")
