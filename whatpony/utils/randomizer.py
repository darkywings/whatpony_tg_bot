from typing import TYPE_CHECKING
import random
import logging
import re

if TYPE_CHECKING:
    from ..pony_type import Pony

logger = logging.getLogger("whatpony-rand")

class PonyRandomizer:

    '''Pony randomizer with weights'''
    def __init__(self,
                 ponies: list['Pony']) -> None:
        '''
        Рандомайзер с весами для выбора пони с неким шансом

        :param ponies: Список состоящий из экземпляров Pony()
        :type ponies: list[Pony]
        '''
        self._ponies = ponies
        self._weights = []

        for _pony in self._ponies:
            self._weights.append(_pony.getWeight())
        
        _total_weights = sum(self._weights)
        for _pony in self._ponies:
            logger.debug(f"Pony<{self._ponies.index(_pony):2}>: {re.sub(r'[^\w\s\.,!?;:\(\)\"\'-]', '', _pony.getName()):25} {f"Weight: {_pony.getWeight():5.3f}":18} {f"Chance: {round(_pony.getWeight() / _total_weights * 100, 3):5.3f}%":15}")

    
    def get_pony(self, index: str | int = None) -> 'Pony':
        '''
        Returns a Pony object

        :param index: Allowing to return a certain pony
        :type index: str | int
        '''
        if index is not None and index != "":
            if not f"{index}".isdigit() or int(f"{index}") >= len(self._ponies):
                return "Unable to use index because of error in the queue"

            return self._ponies[int(f"{index}")]
            
        return random.choices(self._ponies, self._weights)[0]