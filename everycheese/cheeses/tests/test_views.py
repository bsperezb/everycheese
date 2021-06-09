import pytest
from pytest_django.asserts import assertContains
from django.urls import reverse
from django.contrib.sessions.middleware \
import SessionMiddleware
from django.test import RequestFactory
from everycheese.users.models import User

from ..models import Cheese
from ..views import (
CheeseCreateView,
CheeseListView,
CheeseDetailView
)
from .factories import CheeseFactory
pytestmark = pytest.mark.django_db

def test_good_cheese_list_view_expanded(rf):
# Determine the URL
    url = reverse("cheeses:list")
    # rf is pytest shortcut to django.test.RequestFactory
    # We generate a request as if from a user accessing
    #the cheese list view
    request = rf.get(url)
    # Call as_view() to make a callable object
    # callable_obj is analogous to a function-based view
    callable_obj = CheeseListView.as_view()
    # Pass in the request into the callable_obj to get an
    #HTTP response served up by Django
    response = callable_obj(request)
    # Test that the HTTP response has 'Cheese List' in the
    #HTML and has a 200 response code
    assertContains(response, 'Cheese List')

def test_good_cheese_detail_view(rf):
    #order some cheese from the CheeseFactory
    cheese = CheeseFactory()
    #make a request for our newcheese
    url = reverse("cheeses:detail", kwargs={'slug': cheese.slug})
    request = rf.get(url)
    #test that the response is valid
    #use the request to get the response
    callable_obj = CheeseDetailView.as_view()
    response = callable_obj(request, slug= cheese.slug)
    #test that the response is valid
    assertContains(response, cheese.name)

def test_good_cheese_create_view(rf, admin_user):
    #order some cheese from the Cheese Factory
    cheese = CheeseFactory()
    #make a request for our new cheese
    request = rf.get(reverse("cheeses:add"))
    #add on authenticated user
    request.user = admin_user
    #use yeh requesto to get the response
    response = CheeseCreateView.as_view()(request)
    #test tha the response is vald
    assert response.status_code == 200

def test_good_cheese_list_contains_2_cheeses(rf):
    #el primer liss_test evalua la viesta. este evalua el contenido
    # Let's create a couple cheeses
    cheese1 = CheeseFactory()
    cheese2 = CheeseFactory()
    # Create a request and then a response
    # for a list of cheeses
    request = rf.get(reverse('cheeses:list'))
    response = CheeseListView.as_view()(request)
    # Assert that the response contains both cheese names
    # in the template.
    assertContains(response, cheese1.name)
    assertContains(response, cheese2.name)

def test_detail_contains_cheese_data(rf):
    cheese = CheeseFactory()
    # Make a request for our new cheese
    url = reverse("cheeses:detail", kwargs={'slug': cheese.slug})
    request = rf.get(url)
    # get response with request
    response = CheeseDetailView.as_view()(request, slug= cheese.slug)
    # alternativa
    # callable_obj = CheeseDetailView()
    # response = callable_obj(request, slug = cheese.slug)
    assertContains(response, cheese.name)
    assertContains(response, cheese.get_firmness_display())
    assertContains(response, cheese.country_of_origin.name)

def test_cheese_create_form_valid(rf, admin_user):
#submit the cheese add forma
    form_data = {
        "name":"paski sir",
        "description": "A salty hard cheese",
        "firmness": Cheese.Firmness.HARD,
    }
    request = rf.post(reverse("cheeses:add"), form_data)
    request.user = admin_user
    response  = CheeseCreateView.as_view()(request)

    #get the cheese based on the name
    cheese = Cheese.objects.get(name="paski sir")
    # Test that the cheese matches our form
    assert cheese.description == "A salty hard cheese"
    assert cheese.firmness == Cheese.Firmness.HARD
    assert cheese.creator == admin_user

