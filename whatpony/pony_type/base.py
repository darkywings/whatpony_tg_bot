import random

class Pony:

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