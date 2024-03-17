from aiogram.types import Message
from core.keyboards.create_download_keyboard import repy_keyboard


async def get_start(message: Message):
    await message.answer("Виберіть опцію:", reply_markup=repy_keyboard)
