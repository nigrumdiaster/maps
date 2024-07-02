# destination/urls.py
from django.urls import path
from .views import Create_journey

urlpatterns = [
    path('create/', Create_journey.as_view(), name='create_journey'),
    # Other URL patterns for your app
]
