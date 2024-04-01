import logging

from aiogram.filters import BaseFilter
from aiogram.types import Message
import re


class IsYoutubeUrl(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            url = message.text
            match_mobile_link = re.match(r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)?[\w-]{11}(?=\S*[&\?]si=[^&$]+)|(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]{11}&si=[^&$]+', url, re.IGNORECASE)
            match_desktop_link = re.match(r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]+(&\S*)?$', url)
            if match_mobile_link or match_desktop_link:
                return True
            else:
                return False
        except Exception as e:
            logging.error(e)
