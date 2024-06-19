# destination/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_location, name='create_location'),
]
