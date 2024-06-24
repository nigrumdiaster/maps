# destination/urls.py
from django.urls import path
from .views import Create_location, List_location, Detail_location

urlpatterns = [
    path('create/', Create_location.as_view(), name='create_location'),
    path('list/', List_location.as_view(), name='list_location'),
    path('detail/', Detail_location.as_view(), name='detail_location'),

    # Other URL patterns for your app
]
