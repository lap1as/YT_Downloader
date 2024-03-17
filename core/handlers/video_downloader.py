from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from pytube import YouTube
from pytube.exceptions import VideoUnavailable
import re

from core.utils.states import StepsVideoDownloader


async def youtube_link_check(message: Message, state: FSMContext):
    if state.get_state():
        re.match(r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]+(&\S*)?$', message.text)
    else:
        await message.reply("It's not a valid youtube video link")


async def check_video_existence(video_url):
    try:
        YouTube(video_url)
        return True
    except VideoUnavailable:
        return False


async def download_video(message: Message, state: FSMContext):
    await message.answer("Downloading video...")
    await state.set_state(StepsVideoDownloader.GET_VIDEO_URL)
