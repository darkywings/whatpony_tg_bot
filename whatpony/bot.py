import asyncio
import logging.config
import os
import dotenv
import datetime
import logging
import re
from pathlib import Path

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
from utils.log_config import LOGGER_CONFIG
from utils.replies import BotReplies
from utils.keyboard import BotKeyboard

dotenv.load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
Path(BASE_DIR / "logs").mkdir(parents=True, exist_ok=True)



BOT_TOKEN = os.getenv("BOT_TOKEN")

logger = logging.getLogger("whatpony-bot")
logging.config.dictConfig(LOGGER_CONFIG)

logger.info(f"Starting...")

ponyRand = PonyRandomizer(_ponies)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await BotReplies.sendStartMessage(message)

@router.inline_query()
async def inline_handler(inline_query: InlineQuery):

    _user = inline_query.from_user
    _query = inline_query.query
    
    try:
        results = []

        logger.info(f"QueryFrom: uid: {_user.id}; username: {_user.username or "EMPTY"}; query_params: {_query}")

        if match := re.match(r"call (?P<page>\d+)", _query):
            if match:
                _page = int(match.group('page'))
            results = await BotReplies.getPonies(page = _page)

        elif match := re.match(r"shr (?P<share_link>.+)", _query):
            if match:
                _share_link = match.group('share_link')
            results = await BotReplies.getSharedPony(query = _share_link)

        else:
            if match := re.match(r"^(id (?P<pony_id>\d+))?$", _query):
                if match:
                    _pony_id = match.group('pony_id')
                _selected_pony: Pony = await ponyRand.get_pony(index = _pony_id)
            else:
                _selected_pony: Pony = await ponyRand.get_pony()
            results = await BotReplies.getOnePony(selected_pony = _selected_pony)

        await inline_query.answer(results,
                              cache_time=0)
            
        logger.info("OK")

    except Exception as ex:

        logger.error(f"Error on handling query with UID: {_user.id}; query_params: {_query}", exc_info=True)
        result = BotReplies.getError(timestamp = datetime.datetime.now(),
                                     uid = _user.id,
                                     dev = os.getenv('DEV', '::EMPTY_PARAM::'))
        await inline_query.answer(result, cache_time=0)
    

async def main():
    logger.info(f"Started with total {ponyRand.getTotal()} ponies. {ponyRand.getDisabled()} disabled")
    dp.include_router(router)
    await dp.start_polling(bot)

asyncio.run(main())