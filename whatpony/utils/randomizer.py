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
        self._ponies = []
        self._weights = []
        self._total = 0
        self._enabled = 0
        self._disabled = 0

        _pony: 'Pony'

        for _pony in ponies:

            self._ponies.append(_pony)
            self._total += 1
            self._weights.append(_pony.getWeight())

            if _pony.isDisabled():
                self._disabled += 1
                continue

            self._enabled +=1
        
        _total_weights = sum(self._weights)
        for _pony in self._ponies:
            logger.debug(f"Pony<{self._ponies.index(_pony):3}>: {re.sub(r'[^\w\s\.,!?;:\(\)\"\'-]', '', _pony.getName())[:20]:25} "
                         f"{f"Weight: {f"{_pony.getWeight():5.3f}" if not _pony.isDisabled() else "-.---"}":18} "
                         f"{f"Chance: {f"{round(_pony.getWeight() / _total_weights * 100, 3):5.3f}" if not _pony.isDisabled() else "-.---"}%":15} "
                         f"{"[DISABLED]" if _pony.isDisabled() else ""}")

    def getTotal(self) -> int:
        return self._total
    
    def getEnabled(self) -> int:
        return self._enabled
    
    def getDisabled(self) -> int:
        return self._disabled
    
    async def get_pony(self, index: str | int = None) -> 'Pony':
        '''
        Returns a Pony object

        :param index: Allowing to return a certain pony
        :type index: str | int
        '''
        if index is not None and index != "":
            return self._ponies[int(f"{index}")]
            
        return random.choices(self._ponies, self._weights)[0]