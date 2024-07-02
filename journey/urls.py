# destination/urls.py
from django.urls import path
from .views import Create_journey, List_journey, Detail_journey

urlpatterns = [
    path('create/', Create_journey.as_view(), name='create_journey'),
    path('list/', List_journey.as_view(), name='list_journey'),
    path('journeys/<int:pk>/', Detail_journey.as_view(), name='detail_journey'),
    # Other URL patterns for your app
]
