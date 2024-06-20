# destination/urls.py
from django.urls import path
from .views import Create_location

urlpatterns = [
    path('create/', Create_location.as_view(), name='create_location'),
    # Other URL patterns for your app
]
