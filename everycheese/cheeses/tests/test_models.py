import pytest
from ..models import Cheese

pytestmark = pytest.mark.django_db

def test__str__():
    cheese = Cheese.objects.create(
            name="stracchino",
            description="Semi-sweet that goes well with starches",
            firmness=Cheese.Firmness.SOFT,
    )

    assert cheese.__str__() == "stracchino"
    assert str(cheese) == "stracchino"
