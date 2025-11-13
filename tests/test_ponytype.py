import pytest
import re

from whatpony.pony_type import Pony

@pytest.fixture
def pony():
    return Pony(
        name = "Дарки Вингс",
        description = ["Пегас", "Стелька", "Минька"],
        image_url = "http://fakeurl"
    )

def test_pony(pony: Pony):
    assert pony.getName() == "Дарки Вингс"
    assert pony.getDesc() in ["Пегас", "Стелька", "Минька"]
    assert pony.getImg() == "http://fakeurl"
    assert re.match(r"Дарки Вингс - (Пегас|Стелька|Минька)$", pony.get()) is not None