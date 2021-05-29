import pytest
from ..models import Cheese
from .factories import CheeseFactory
pytestmark = pytest.mark.django_db

def test__str__():
    cheese = CheeseFactory()
    assert cheese.__str__() == cheese.name
    assert str(cheese) == cheese.name

