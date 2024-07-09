from django.urls import path
from .views import Create_journey, List_journey, Detail_journey, change_locations_in_journey

urlpatterns = [
    path('create/', Create_journey.as_view(), name='create_journey'),
    path('list/', List_journey.as_view(), name='list_journey'),
    path('journeys/<int:pk>/', Detail_journey.as_view(), name='detail_journey'),
    path('journeys/<int:pk>/change-locations/', change_locations_in_journey, name='change_locations_in_journey'),
    # Other URL patterns for your app
]
