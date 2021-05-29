from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Cheese

class CheeseListView(ListView):
    model = Cheese
