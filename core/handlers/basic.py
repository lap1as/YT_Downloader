import logging
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.utils.states import ChoseDownloader
from core.keyboards.create_download_keyboard import repy_keyboard
from core.handlers.video_downloader import download_video
from core.handlers.audio_downloader import download_audio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_start(message: Message):
    """
    Start function to greet the user and present options.
    """
    logger.info("Received start command.")
    await message.answer("Hi! I'm YouTube Downloader!")
    await message.answer("Choose what to do:", reply_markup=repy_keyboard)
    logger.info("Sent start message.")

async def chose_what_to_download(message: Message, state: FSMContext):
    """
    Handler to choose what to download based on user input.
    """
    logger.info("Received input for download choice.")
    if message.text == "Download video":
        logger.info("User chose to download video.")
        await state.set_state(ChoseDownloader.download_video)
        await message.answer("Send link to download video")
        logger.info("Prompted for video link.")
    elif message.text == "Download audio":
        logger.info("User chose to download audio.")
        await state.set_state(ChoseDownloader.download_audio)
        await message.answer("Send link to download audio")
        logger.info("Prompted for audio link.")

async def download(message: Message, state: FSMContext):
    """
    Handler to initiate the download based on the user's previous choice.
    """
    logger.info("Initiating download process.")
    current_state = await state.get_state()
    logger.info(f"Current state: {current_state}")
    if current_state == ChoseDownloader.download_video:
        logger.info("Downloading video...")
        await download_video(message, state)
    elif current_state == ChoseDownloader.download_audio:
        logger.info("Downloading audio...")
        await download_audio(message, state)
    else:
        logger.warning(f"Unexpected state: {current_state}")
