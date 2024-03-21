import asyncio
import logging

from core.settings import settings
from core.handlers.basic import get_start, waiting_for_url
from core.handlers.video_downloader import download_video
from core.filters.isYoutubeUrl import IsYoutubeUrl
from core.utils.states import StepsVideoDownloader

from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram import F


async def start():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    default = DefaultBotProperties(parse_mode=settings.bots.parse_mode)
    bot = Bot(token=settings.bots.bot_token, default=default)

    dp = Dispatcher()

    dp.message.register(get_start, Command("start"))
    dp.message.register(waiting_for_url, F.text == "Download video")
    dp.message.register(download_video, IsYoutubeUrl())

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())
