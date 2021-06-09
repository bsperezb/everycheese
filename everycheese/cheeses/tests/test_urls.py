import pytest
from django.urls import  reverse, resolve
from .factories import CheeseFactory

pytestmark = pytest.mark.django_db

@pytest.fixture
def cheese():
    return CheeseFactory()

def test_list_reverse():
    """cheese:list shold reverse to /cheeses/."""
    #reverse give us the obsolute url
    assert reverse('cheeses:list') == '/cheeses/'

def test_list_resolve():
    """/cheeses/ should resolve to cheeses:list."""
    # resolving absolute url give us the view name
    assert resolve('/cheeses/').view_name == 'cheeses:list'


def test_add_reverse():
    """cheese:add shold reverse to /cheeses/add/."""
    #reverse give us the obsolute url (path)
    assert reverse('cheeses:add') == '/cheeses/add/'

def test_add_resolve():
    """/cheeses/ should resolve to cheeses:list."""
    # resolving absolute url give us the view name
    assert resolve('/cheeses/add/').view_name == 'cheeses:add'

def test_detail_reverse(cheese):
    """cheeses:detail should reverse to /cheeses/cheeseslug/."""
    url = reverse('cheeses:detail', kwargs={'slug':cheese.slug})
    assert url == f'/cheeses/{cheese.slug}/'

def test_detail_resolve(cheese):
    """/cheeses/cheeseslug/ shold resolve to cheeses:detail."""
    url = f'/cheeses/{cheese.slug}/'
    assert resolve(url).view_name == 'cheeses:detail'
