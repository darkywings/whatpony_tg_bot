import logging
import os
import dotenv

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

dotenv.load_dotenv()

logger = logging.getLogger("whatpony-bot")

DONATE_LINK = os.getenv("DONATE_LINK", "https://www.youtube.com/watch?v=dQw4w9WgXcQ")

if not os.getenv("DONATE_LINK", None):
    logger.warning(f"DONATE_LINK not found in .env")

class BotKeyboard:
    
    def getKeyboard(share_query: str = "") -> InlineKeyboardMarkup:

        '''
        Возвращает подготовленную inline-клавиатуру

        :param share_query: Идентификатор ответа, для возможности им поделиться с другими
        :type share_query: str
        '''
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Какая ты пони",
                                        switch_inline_query_current_chat=""),
                ],
                [
                    InlineKeyboardButton(text="Поделиться",
                                        switch_inline_query=share_query),
                    InlineKeyboardButton(text="Поддержать бота" if os.getenv("DONATE_LINK", None) else "Кнопка не настроена :)",
                                        url=DONATE_LINK),
                ]
            ]
        )