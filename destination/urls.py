# destination/urls.py
from django.urls import path
from .views import Create_location, List_location, Detail_location

urlpatterns = [
    path('create/', Create_location.as_view(), name='create_location'),
    path('location/', List_location.as_view(), name='list_location'),
    path('locations/<int:pk>/', Detail_location.as_view(), name='location_detail'),
    # Other URL patterns for your app
]
