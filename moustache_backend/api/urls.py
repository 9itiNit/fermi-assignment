# api/urls.py
from django.urls import path
from .views import search_properties

urlpatterns = [
    path('search/', search_properties),
]
