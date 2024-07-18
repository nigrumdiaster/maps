from django.urls import path
from .views import Show_maps, Show_categories, Navigation

urlpatterns = [
    path("maps/", Show_maps.as_view(), name="show_maps"),
    path("categories/", Show_categories, name="show_categories"),
    path("navigation/", Navigation, name="navigation"),
    # Other URL patterns for your app
]
