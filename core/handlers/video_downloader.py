import logging
import os

from aiogram.types import Message
from aiogram.types import FSInputFile

from pytube import YouTube
from pytube.exceptions import VideoUnavailable




async def check_video_existence(video_url):
    try:
        YouTube(video_url)
        return True
    except VideoUnavailable:
        return False

async def chose_stream(url):
    """Compleate resolution chose"""
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    streams = yt.streams.filter(progressive=True)
    chosen_stream = None


async def download_video(message: Message):
    if await check_video_existence(message.text):
        try:
            await message.answer("Downloading video...")
            yt = YouTube(message.text)
            stream = yt.streams.get_highest_resolution()
            streams = yt.streams.filter(progressive=True)
            chosen_stream = None

            full_path = str(os.path.abspath("videos"))
            name_of_video = str(f"{message.message_id}.mp4")
            stream.download(output_path=full_path, filename=name_of_video)
            await message.answer("Video Downloaded!")

            path_of_downloaded_video = str(f"{full_path}\\{name_of_video}")
            file_size = round((os.stat(path_of_downloaded_video).st_size) / (1024 * 1024))

            if file_size <= 50:
                video = FSInputFile(path_of_downloaded_video)
                await message.answer_video(video)
                os.remove(path_of_downloaded_video)
            else:
                await message.answer("Sorry video is too large")
                os.remove(path_of_downloaded_video)
        except Exception as e:
            logging.error(e)
