import logging
import os

from aiogram.fsm.context import FSMContext
from pytube import YouTube
from pathlib import Path

from aiogram.types import Message
from aiogram.types import FSInputFile

from core.utils.states import ChoseDownloader
from core.keyboards.create_download_keyboard import repy_keyboard


async def download_audio(message: Message, state: FSMContext):
    try:
        yt = YouTube(message.text)
        folder_path = Path("audios")
        audios_folder = "audios"
        file_name = f"{yt.title}.mp3"
        base_dir = Path.cwd()
        full_path_of_downloaded_audio = base_dir / audios_folder / f"{message.message_id}.mp3"
        yt.streams.filter(only_audio=True).first().download(output_path=folder_path, filename=f"{message.message_id}.mp3")
        audio = FSInputFile(full_path_of_downloaded_audio)
        await message.answer_audio(audio, caption=yt.title, reply_markup=repy_keyboard)
    except Exception as e:
        logging.error(e)
    finally:
        os.remove(full_path_of_downloaded_audio)
        await state.clear()