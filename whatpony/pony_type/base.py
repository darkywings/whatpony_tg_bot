import random

class Pony:
    '''Базовый класс с информацией о пони'''
    def __init__(self,
                 name: str,
                 description: str | list[str] = [],
                 weight: float = 1,
                 image_url: str | list[str] | None = None,
                 message: str | None = None,
                 message_only: bool = False,
                 disable: bool = False) -> None:
        '''
        Базовый класс с информацией о пони

        :param name: Имя поняшки
        :type name: str

        :param description: Подпись(подписи) к поняшке
        :type description: str | list[str]

        :param weight: Шанс выпадения
        :type weight: float

        :param image_url: Изображение(изображения) поняшки (опционально)
        :type image_url: str | list[str] | None

        :param message: Сообщение при message_only = True
        :type message: str | None

        :param message_only: Является ли пони пасхалкой
        :type message_only: bool

        :param disable: Позволяет исключить выбранную пони из выборки
        :type disable: bool
        '''
        self._disabled: bool = disable
        self._name: str = name
        self._description: list[str] = [description] if isinstance(description, str) else description
        self._image_url: list[str] = [image_url] if isinstance(image_url, str) else image_url if isinstance(image_url, list) else None
        self._weight: float = weight
        self._message_only: bool = message_only
        
        self._message: str = message if message and message_only else ValueError("_message should not be empty if _message_only is True")

        if (self._weight < 0.001 and
            self._weight > 100):
            raise ValueError("weight should be in range [0.001, 100]. For disabling use 'disable' parameter")

    def getName(self) -> str:
        return self._name
    
    def getDesc(self) -> str:
        if not self._disabled:
            return random.choice(self._description)
        return None
    
    def getImg(self) -> str:
        if not self._disabled:
            return random.choice(self._image_url)
        return None
    
    def getWeight(self) -> float:
        if self.isDisabled():
            return 0
        return self._weight
    
    def getMessage(self) -> str:
        return self._message
    
    def isMessageOnly(self) -> bool:
        return self._message_only
    
    def isDisabled(self) -> bool:
        return self._disabled