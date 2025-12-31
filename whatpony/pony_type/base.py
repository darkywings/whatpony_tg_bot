import random

class Pony:
    '''Базовый класс с информацией о пони'''
    def __init__(self,
                 name: str,
                 description: str | list[str],
                 weight: float = 1,
                 image_url: str | list[str] | None = None,
                 message: str | None = None,
                 message_only: bool = False) -> None:
        '''
        Базовый класс с информацией о пони

        :param name: Имя поняшки
        :type name: str

        :param description: Подпись(подписи) к поняшке
        :type description: str | list[str]

        :param weight: Шанс выпадения
        :type weight: float

        :param image_url: Изображение поняшки (опционально)
        :type image_url: str | None

        :param message: Сообщение при message_only = True
        :type message: str | None

        :param message_only: Является ли пони пасхалкой
        :type message_only: bool
        '''
        self._name = name
        self._description = [description] if isinstance(description, str) else description
        self._image_url = [image_url] if isinstance(image_url, str) else image_url
        self._weight = weight
        self._message_only = message_only
        
        self._message = message if message and message_only else ValueError("_message should not be empty if _message_only is True")

        if (self._weight < 0.001 and
            self._weight > 100):
            raise ValueError("_weight should be in range [0.001, 100]")

    def getName(self) -> str:
        return self._name
    
    def getDesc(self) -> str:
        return random.choice(self._description)
    
    def getImg(self) -> str:
        return random.choice(self._image_url)
    
    def getWeight(self):
        return self._weight
    
    def getMessage(self):
        return self._message
    
    def isMessageOnly(self):
        return self._message_only
    
    def get(self) -> str:
        '''
        Получить готовую фразу <имя - описание>
        '''
        return f"{self.getName()}\n{self.getDesc()}"