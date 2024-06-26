from django.urls import path
from .views import Show_maps
urlpatterns = [
    path('show/', Show_maps.as_view(), name='show_maps'),
    # Other URL patterns for your app
]