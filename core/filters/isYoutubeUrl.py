from aiogram.filters import BaseFilter
from aiogram.types import Message
import re
from aiogram.fsm.context import FSMContext


class IsYoutubeUrl(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            url = message.text
            match=re.match(r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]+(&\S*)?$', url)
            if match:
                return True
        except:
            return False


