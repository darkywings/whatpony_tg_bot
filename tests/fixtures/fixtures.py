import pytest

from whatpony.pony_type import Pony

@pytest.fixture
def pony():
    return Pony(
        name = "Дарки Вингс",
        description = ["Пегас", "Стелька", "Минька"],
        weight=0.1,
        image_url = "http://fakeurl/darky.png"
    )

@pytest.fixture
def ponies():
    return [
        Pony(
            name = "Дарки",
            description = ["Пегас", "Стелька", "Минька"],
            weight=1,
            image_url = "http://fakeurl/darky.png"
        ),
        Pony(
            name = "Крис",
            description = ["Единорог", "Пони"],
            weight=1,
            image_url = "http://fakeurl/chrystal.png"
        ),
    ]