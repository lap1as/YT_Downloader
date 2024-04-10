import logging
import os
import re
from pathlib import Path

from aiogram.fsm.context import FSMContext
from pytube import YouTube
from aiogram.types import Message, FSInputFile

from core.utils.states import ChoseDownloader
from core.keyboards.create_download_keyboard import repy_keyboard

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def download_audio(message: Message, state: FSMContext):
    try:
        logger.info("Starting audio download process...")

        # Extract YouTube video information
        yt = YouTube(message.text)
        logger.info(f"Video title: {yt.title}")

        # Set up folder paths
        folder_path = Path("audios")
        audios_folder = "audios"

        # Define file name and full path for the downloaded audio
        file_name = f"{yt.title}.mp3"
        clean_filename = re.sub(r'[\\/:*?"<>| ]', '_', file_name)
        base_dir = Path.cwd()
        full_path_of_downloaded_audio = base_dir / audios_folder / clean_filename

        # Download audio from YouTube
        logger.info("Downloading audio...")
        yt.streams.filter(only_audio=True).first().download(output_path=folder_path,
                                                            filename=str(clean_filename))
        logger.info("Audio downloaded successfully.")

        # Create an FSInputFile object for the downloaded audio
        audio = FSInputFile(full_path_of_downloaded_audio)

        # Send the audio as a reply to the message
        logger.info("Sending audio as a reply...")
        await message.answer_audio(audio, caption=yt.title, reply_markup=repy_keyboard)
        logger.info("Audio sent successfully.")
    except Exception as e:
        # Log any errors that occur during the process
        logger.error(f"An error occurred while downloading audio: {e}")
    finally:
        # Remove the downloaded audio file and clear the state
        logger.info("Cleaning up...")
        os.remove(full_path_of_downloaded_audio)
        logger.info("File removed.")
        await state.clear()
        logger.info("State cleared.")
