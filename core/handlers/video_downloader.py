import logging
import os
import re
from pathlib import Path

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from pytube import YouTube
from pytube.exceptions import VideoUnavailable

from core.utils.states import ChoseDownloader
from core.keyboards.create_download_keyboard import repy_keyboard

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StreamSelectionException(Exception):
    """Raised when a suitable video stream cannot be selected"""

async def check_video_existence(video_url):
    """Check if the video is available on YouTube."""
    try:
        YouTube(video_url)
        return True
    except VideoUnavailable:
        return False

async def chose_video_resolution(url, folder_path, name_of_video):
    """Choose a video stream with a resolution less than or equal to 50 MB."""
    yt = YouTube(url)
    try:
        stream = next((stream for stream in yt.streams.filter(progressive=True) if stream.filesize <= 50 * 1024 * 1024), None)
        if stream:
            stream.download(output_path=folder_path, filename=name_of_video)
            logger.info(f"Video {name_of_video} downloaded.")
            return True
        else:
            logger.warning(f"Video {name_of_video} does not have a stream with a size less than or equal to 50 MB.")
            return False
    except StreamSelectionException:
        logger.error(f"Failed to choose a stream for video {name_of_video}.")
        return False

async def download_video(message: Message, state: FSMContext):
    """Download video from the provided URL."""
    if await check_video_existence(message.text):
        try:
            yt = YouTube(message.text)
            folder_path = Path("videos")
            videos_folder = "videos"
            base_dir = Path.cwd()
            filename = f"{yt.title}.mp3"
            clean_filename = re.sub(r'[\\/:*?"<>| ]', '_', yt.title)
            full_path_of_downloaded_video = base_dir / videos_folder / clean_filename
            path_of_downloaded_video = full_path_of_downloaded_video.resolve()
            if await chose_video_resolution(url=message.text, folder_path=folder_path, name_of_video=clean_filename):
                logger.info("Downloading video...")
                yt = YouTube(message.text)
                video = FSInputFile(path_of_downloaded_video)
                await message.answer("Downloading video...")
                await message.answer_video(video, caption=yt.title, reply_markup=repy_keyboard)
                logger.info("Video sent successfully.")
                return True

            else:
                logger.warning("Video is too large.")
                await message.answer("Sorry, the video is too large.")
        except FileNotFoundError:
            logger.error("FileNotFoundError: Failed to download video.")
            await message.answer("Failed to download video. Please try again later.")
        finally:
            if path_of_downloaded_video.exists():
                os.remove(path_of_downloaded_video)
                logger.info("Temporary video file removed.")
                await state.clear()
                logger.info("State cleared.")
