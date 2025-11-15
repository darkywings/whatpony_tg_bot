import random

class Pony:
    '''Базовый класс с информацией о пони'''
    def __init__(self,
                 name: str,
                 description: str | list[str],
                 image_url: str | None = None) -> None:
        '''
        Базовый класс с информацией о пони

        :param name: Имя поняшки
        :type name: str

        :param description: Подпись(подписи) к поняшке
        :type description: str | list[str]

        :param image_url: Изображение поняшки (опционально)
        :type image_url: str | None
        '''
        self._name = name
        self._description = [description] if isinstance(description, str) else description
        self._image_url = image_url

    def getName(self) -> str:
        return self._name
    
    def getDesc(self) -> str:
        return random.choice(self._description)
    
    def getImg(self) -> str:
        return self._image_url
    
    def get(self) -> str:
        '''
        Получить готовую фразу <имя - описание>
        '''
        return f"{self.getName()} - {self.getDesc()}"

class Message:
    '''Базовый класс для отправки обычного сообщения'''
    def __init__(self,
                 message: str,
                 image_url: str | None = None) -> None:
        '''
        Базовый класс для отправки обычного сообщения

        :param message: Текст сообщения
        :type message: str

        :param image_url: URL прикрепляемого изображения(опционально)
        :type image_url: str | None
        '''
        self._message = message
        self._image_url = image_url
    
    def getMessage(self):
        return self._message
    
    def getImg(self):
        return self._image_url