from django.urls import path
from .views import Create_journey, List_journey, Detail_journey, add_locations_to_journey

urlpatterns = [
    path('create/', Create_journey.as_view(), name='create_journey'),
    path('list/', List_journey.as_view(), name='list_journey'),
    path('journeys/<int:pk>/', Detail_journey.as_view(), name='detail_journey'),
    path('journeys/<int:pk>/add-locations/', add_locations_to_journey, name='add_locations_to_journey'),
    # Other URL patterns for your app
]
