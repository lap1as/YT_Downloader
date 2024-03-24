from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.utils.states import ChoseDownloader
from core.keyboards.create_download_keyboard import repy_keyboard
from core.handlers.video_downloader import download_video
from core.handlers.audio_downloader import download_audio


async def get_start(message: Message):
    await message.answer("Hi! I'm YouTube Downloader!")
    await message.answer("Chose what to do:", reply_markup=repy_keyboard)

async def chose_what_to_download(message: Message, state: FSMContext):
    if message.text == "Download video":
        await state.set_state(ChoseDownloader.download_video)
        await message.answer("Send link to download video")
    elif message.text == "Download audio":
        await state.set_state(ChoseDownloader.download_audio)
        await message.answer("Send link to download audio")

async def download(message: Message, state:FSMContext):
    current_state = await state.get_state()
    if current_state == ChoseDownloader.download_video:
        await download_video(message, state)
    elif current_state == ChoseDownloader.download_audio:
        await download_audio(message, state)

    else:
        await message.answer(f"{current_state}")

