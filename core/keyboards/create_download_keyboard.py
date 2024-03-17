from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


repy_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text="Download video"
        )
    ],
    [
        KeyboardButton(
            text="Download audio"
        )
    ]
])
