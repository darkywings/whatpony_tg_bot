from typing import TYPE_CHECKING
import logging

from aiogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent
)
from aiogram.utils.markdown import hide_link

from pony_type import _ponies
from utils.keyboard import BotKeyboard

if TYPE_CHECKING:
    from pony_type import Pony
    from aiogram.types import (
        InlineKeyboardMarkup,
        Message
    )

logger = logging.getLogger("whatpony-bot")

bot_keyboard = BotKeyboard()

class BotReplies:

    async def sendStartMessage(message: 'Message') -> None:
        '''
        Отправляет приветственное сообщение при /start

        :param message: Объект сообщения
        :type message: Message
        '''
        await message.reply(
            text = (
                f"Привет, {message.from_user.username}!\n"
                f"Этот бот позволяет узнать какая ты поняшка\n\n"
                f""
                f"Напиши \"@whatpony_bot\" чтобы узнать какая ты пони или нажми на кнопку \"Какая ты пони\" ниже\n\n"
                f""
                f"Свои предложения можно присылать сюда: "
                f"https://docs.google.com/forms/d/e/1FAIpQLScKczq2bnnIZSYqb94YdwNfR6phVKzPxgeqBaQwwZWUmLWp5g/viewform?usp=header\n^w^"
            ),
            reply_markup = bot_keyboard.getKeyboard()
        )
    
    async def getOnePony(selected_pony: 'Pony') -> list[InlineQueryResultArticle]:
        '''
        Формирует результат для вывода выпавшей поняшки

        :param selected_pony: Выпавший объект Pony, который характеризует саму пони-личность
        :type selected_pony: Pony
        '''

        _pony_data: dict = BotReplies._getPonyData(selected_pony)

        return [
                InlineQueryResultArticle(
                    id="1",
                    title="Узнать какая ты пони",
                    description="Нажмите сюда, чтобы определить какая вы пони",
                    input_message_content=InputTextMessageContent(
                        message_text=f"{hide_link(_pony_data.get('img')) if _pony_data.get('img') is not None else ""}{_pony_data.get('output')}",
                        parse_mode="HTML"
                    ),
                    thumbnail_url="https://derpicdn.net/img/view/2012/1/6/38.png",
                    reply_markup=bot_keyboard.getKeyboard(),
                )
            ]
    
    async def getPonies(page: int = 1) -> list[InlineQueryResultArticle]:
        '''
        Возвращает список пони для вызова

        :param page: Страница списка (начинается с 1)
        :type page: int
        '''
        logger.info(f"Returning list of ponies...")

        _results = []
        _max = 50
        for _pony in _ponies[_max * (page - 1): _max * page]:

            _pony_data: dict = BotReplies._getPonyData(_pony)

            _results.append(
                InlineQueryResultArticle(
                    id = f"{_ponies.index(_pony)}",
                    title = f"{_pony.getName()}",
                    description = f"Вызвать {_pony.getName()}",
                    input_message_content=InputTextMessageContent(
                        message_text=f"{hide_link(_pony_data.get('img')) if _pony_data.get('img') is not None else ""}{_pony_data.get('output')}",
                        parse_mode="HTML"
                    ),
                    reply_markup=bot_keyboard.getKeyboard(),
                )
            )

        return _results
    
    def getError(timestamp: str,
                 uid: str,
                 dev: str) -> list[InlineQueryResultArticle]:
        '''
        Возвращает информацию об ошибке

        :param timestamp: Временная метка ошибки
        :type timestamp: str

        :param uid: Идентификатор пользователя, у которого произошла ошибка
        :type uid: str,

        :param dev: Контактные данные разработчика
        :type dev: str
        '''
        return [
            InlineQueryResultArticle(
                id="1",
                title="Произошла ошибка",
                description="Нажмите сюда, чтобы вывести ошибку и контактную информацию разработчика",
                input_message_content=InputTextMessageContent(
                    message_text=f"{hide_link("https://derpicdn.net/img/view/2025/11/20/3715552.gif")}TIMESTAMP: {timestamp}\nUID: {uid}\n\nСвяжитесь с {dev} и передайте ему эту информацию.\nСпасибо ^-^\nИзвините за неудобства",
                    parse_mode="HTML"
                ),
                thumbnail_url="https://derpicdn.net/img/2021/2/13/2549975/large.png",
                reply_markup=bot_keyboard.getKeyboard(),
            )
        ]
    
    def _getPonyData(_pony: 'Pony'):
        _pony_data: dict = {
            "name": _pony.getName(),
            "desc": _pony.getDesc(),
            "img": _pony.getImg(),
            "msg": _pony.getMessage()
        }
        if _pony.isMessageOnly():
            _pony_data.update({"output": (
                f"{_pony_data.get("msg", "::MSG::")}"
            )})
        else:
            _pony_data.update({"output": (
                f"🎉 Твоя пони-личность: \n"
                f"{_pony_data.get("name", "::PONY_NAME::")}\n"
                f"{_pony_data.get("desc", "::PONY_DESC::")}"
            )})
        return _pony_data