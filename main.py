import asyncio
import logging
from logging.handlers import RotatingFileHandler


from core.settings import settings
from core.handlers.basic import get_start, chose_what_to_download, download
from core.handlers.video_downloader import download_video
from core.filters.isYoutubeUrl import IsYoutubeUrl
from core.utils.states import ChoseDownloader

from aiogram.filters import Command
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram import F


async def start():
    # Configure logging to rotate log files
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_handler = RotatingFileHandler(
        'bot.log',  # Specify the log file name
        maxBytes=10 * 1024 * 1024,  # Set maximum size for each log file (10 MB in this case)
        backupCount=5  # Set the number of backup files to retain
    )
    log_handler.setFormatter(log_formatter)
    logger = logging.getLogger()
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)  # Set logging level to INFO
    # Initialize the bot with token and default properties
    default = DefaultBotProperties(parse_mode=settings.bots.parse_mode)
    bot = Bot(token=settings.bots.bot_token, default=default)

    # Initialize the dispatcher
    dp = Dispatcher()

    # Register handlers for different types of messages
    dp.message.register(get_start, Command("start"))  # Handle /start command
    dp.message.register(chose_what_to_download, F.text == "Download video")  # Handle "Download video" text
    dp.message.register(chose_what_to_download, F.text == "Download audio")  # Handle "Download audio" text
    dp.message.register(download, IsYoutubeUrl())  # Handle YouTube URLs

    try:
        # Start polling for updates
        await dp.start_polling(bot)
    finally:
        # Ensure bot session is closed properly
        await bot.session.close()


if __name__ == '__main__':
    # Run the start function asynchronously
    asyncio.run(start())
