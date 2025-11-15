import asyncio
import logging.config
import os
import dotenv
import logging
from logging import Formatter
import random

from aiogram import Router, Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hide_link
from aiogram.types import (
    InlineQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Message
)

from pony_type import _ponies, _easter_eggs, Pony
from pony_type import Message as PonyTypeMessage

dotenv.load_dotenv()

LOGGER_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "()": Formatter,
            "fmt": "%(name)s | %(asctime)s | %(levelname)s | %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "console"
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG"
    }
}

logger = logging.getLogger("whatpony-bot")
logging.config.dictConfig(LOGGER_CONFIG)

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()
router = Router()

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Какая ты пони",
                                 switch_inline_query_current_chat="")
        ]
    ]
)

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.username}. \nЭтот бот позволяет узнать какая ты поняшка\n\n"
        "Напиши \"@whatpony_bot\" чтобы узнать какая ты пони или нажми на кнопку \"Какая ты пони\" ниже",
        reply_markup=keyboard,
    )

@router.inline_query()
async def inline_handler(inline_query: InlineQuery):
    
    _selected_pony: tuple[str, str] = await get_pony(inline_query.query)

    results = [
        InlineQueryResultArticle(
            id="1",
            title="Узнать какая ты пони",
            description="Нажмите сюда, чтобы определить какая вы пони",
            input_message_content=InputTextMessageContent(
                message_text=f"{_selected_pony[0]}{hide_link(_selected_pony[1]) if _selected_pony[1] is not None else ""}",
                parse_mode="HTML"
            ),
            thumbnail_url="https://derpicdn.net/img/view/2012/1/6/38.png",
            reply_markup=keyboard,
        )
    ]
    await inline_query.answer(results,
                              cache_time=1)

async def get_pony(index: str = None):

    _selected_pony = random.choice(_ponies)

    if random.randint(0, 1000) == 1:
        _selected_pony = random.choice(_easter_eggs)

    if index:
        if not index.lstrip("-").isdigit() or abs(int(index)) >= max([len(_ponies), len(_easter_eggs)]):
            return ("⚠️Unable to use index because of the query format", "")
        if int(index) > 0: _selected_pony = _ponies[abs(int(index))-1]
        elif int(index) < 0: _selected_pony = _easter_eggs[abs(int(index))-1]
    
    if isinstance(_selected_pony, Pony):
        return (f"🎉 Твоя пони-личность: \n{_selected_pony.get()}", _selected_pony.getImg())
    
    if isinstance(_selected_pony, PonyTypeMessage):
        return (_selected_pony.getMessage(), _selected_pony.getImg()) 

async def main():
    logger.info(f"Started with {len(_ponies)} ponies")
    dp.include_router(router)
    await dp.start_polling(bot)

asyncio.run(main())