from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Define the reply keyboard markup
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
