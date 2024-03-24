import logging
import os
from pathlib import Path

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import FSInputFile

from core.utils.states import ChoseDownloader
from core.keyboards.create_download_keyboard import repy_keyboard

from pytube import YouTube
from pytube.exceptions import VideoUnavailable


class StreamSelectionException(Exception):
    """Raised when a suitable video stream cannot be selected"""


async def check_video_existence(video_url):
    try:
        YouTube(video_url)
        return True
    except VideoUnavailable:
        return False


async def chose_video_resolution(url, folder_path, name_of_video):
    """Choose video stream with resolution less than or equal to 50 MB"""
    yt = YouTube(url)
    try:
        stream = next((stream for stream in yt.streams.filter(progressive=True) if stream.filesize <= 50 * 1024 * 1024), None)
        if stream:
            stream.download(output_path=folder_path, filename=name_of_video)
            logging.log(msg=f"Video {name_of_video} downloaded", level=logging.INFO)
            return True
        else:
            logging.warning(msg=f"Video {name_of_video} does not have a stream with a size less than or equal to 50 MB")
            return False
    except StreamSelectionException:
        logging.error(msg=f"Failed to choose a stream for video {name_of_video}")
        return False


async def download_video(message: Message, state: FSMContext):
    if await check_video_existence(message.text):
        try:
            folder_path = Path("videos")
            videos_folder = "videos"
            base_dir = Path.cwd()
            full_path_of_downloaded_video = base_dir / videos_folder / f"{message.message_id}.mp4"
            path_of_downloaded_video = full_path_of_downloaded_video.resolve()
            if await chose_video_resolution(url=message.text, folder_path=folder_path, name_of_video=f"{message.message_id}.mp4"):
                try:
                    await message.answer("Downloading video...")
                    yt = YouTube(message.text)
                    video = FSInputFile(path_of_downloaded_video)
                    await message.answer_video(video, caption=yt.title, reply_markup=repy_keyboard)
                    return True
                except Exception as e:
                    logging.error(e)

            else:
                await message.answer("Sorry video is too large")
        except FileNotFoundError:
            logging.error(FileNotFoundError)
            await message.answer("Failed to download video. Please try again later.")
        finally:
            if path_of_downloaded_video.exists():
                os.remove(path_of_downloaded_video)
                await state.clear()
