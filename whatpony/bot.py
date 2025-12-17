import asyncio
import logging.config
import os
import dotenv
import logging
import re
from logging import Formatter

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

from pony_type import _ponies, Pony
from utils.randomizer import PonyRandomizer

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

ponyRand = PonyRandomizer(_ponies)

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()
router = Router()

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Какая ты пони",
                                 switch_inline_query_current_chat=""),
            InlineKeyboardButton(text="Поделиться",
                                 switch_inline_query=""),
        ]
    ]
)

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.username}!\nЭтот бот позволяет узнать какая ты поняшка\n\n"
        "Напиши \"@whatpony_bot\" чтобы узнать какая ты пони или нажми на кнопку \"Какая ты пони\" ниже\n\n"
        "Свои предложения можно присылать сюда: https://docs.google.com/forms/d/e/1FAIpQLScKczq2bnnIZSYqb94YdwNfR6phVKzPxgeqBaQwwZWUmLWp5g/viewform?usp=header\n^w^",
        reply_markup=keyboard,
    )

@router.inline_query()
async def inline_handler(inline_query: InlineQuery):

    _query = inline_query.query
    
    if re.match(r"call (\d+)", _query):
        results = []
        _page = int(re.match(r"call (\d+)", _query)[1])
        _max = 50
        for _pony in _ponies[_max * (_page - 1): _max * _page]:
            results.append(
                InlineQueryResultArticle(
                    id = f"{_ponies.index(_pony)}",
                    title = f"{_pony.getName()}",
                    description = f"Вызвать {_pony.getName()}",
                    input_message_content=InputTextMessageContent(
                        message_text=f"{hide_link(_pony.getImg()) if _pony.getImg() is not None else ""}{(await get_pony(f"{_ponies.index(_pony)}"))[0]}",
                        parse_mode="HTML"
                    ),
                    reply_markup=keyboard,
                )
            )

    else:
        _selected_pony: tuple[str, str] = await get_pony(inline_query.query)

        results = [
            InlineQueryResultArticle(
                id="1",
                title="Узнать какая ты пони",
                description="Нажмите сюда, чтобы определить какая вы пони",
                input_message_content=InputTextMessageContent(
                    message_text=f"{hide_link(_selected_pony[1]) if _selected_pony[1] is not None else ""}{_selected_pony[0]}",
                    parse_mode="HTML"
                ),
                thumbnail_url="https://derpicdn.net/img/view/2012/1/6/38.png",
                reply_markup=keyboard,
            )
        ]
    await inline_query.answer(results,
                              cache_time=0)

async def get_pony(index: str = None):

    _selected_pony = ponyRand.get_pony(index)
    
    if isinstance(_selected_pony, Pony):
        if _selected_pony.isMessageOnly():
            return (_selected_pony.getMessage(), _selected_pony.getImg())
        return (f"🎉 Твоя пони-личность: \n{_selected_pony.get()}", _selected_pony.getImg())
    
    if isinstance(_selected_pony, str):
        return (_selected_pony, None)

async def main():
    logger.info(f"Started with {len(_ponies)} ponies")
    dp.include_router(router)
    await dp.start_polling(bot)

asyncio.run(main())