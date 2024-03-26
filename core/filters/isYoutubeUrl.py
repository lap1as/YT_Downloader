from aiogram.filters import BaseFilter
from aiogram.types import Message
import re


class IsYoutubeUrl(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            url = message.text
            match = re.match(r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)?[\w-]{11}(?=\S*[&\?]si=[^&$]+)|(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]{11}&si=[^&$]+', url, re.IGNORECASE)
            if match:

                return True
        except:
            return False
