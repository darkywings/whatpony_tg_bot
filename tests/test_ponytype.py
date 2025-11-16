import pytest
import re
from typing import TYPE_CHECKING

from whatpony.utils.randomizer import PonyRandomizer

from .fixtures import ponies, pony

if TYPE_CHECKING:
    from whatpony.pony_type import Pony

def test_pony(pony: 'Pony'):
    assert pony.getName() == "Дарки Вингс"
    assert pony.getDesc() in ["Пегас", "Стелька", "Минька"]
    assert pony.getImg() == "http://fakeurl/darky.png"
    assert pony.getWeight() == 0.1
    assert pony.isMessageOnly() == False
    assert re.match(r"Дарки Вингс - (Пегас|Стелька|Минька)$", pony.get()) is not None

def test_random(ponies: list['Pony']):
    rand = PonyRandomizer(ponies=ponies)
    _darky_appeared = 0
    _chrystal_appeared = 0
    for i in range(100):
        _pony = rand.get_pony()
        match _pony.getName():
            case "Дарки":   _darky_appeared += 1
            case "Крис":    _chrystal_appeared += 1
    
    assert _darky_appeared > 5
    assert _chrystal_appeared > 5

def test_choice(ponies: list['Pony']):
    rand = PonyRandomizer(ponies=ponies)
    assert rand.get_pony(0).getName() == "Дарки"
    assert rand.get_pony(1).getName() == "Крис"