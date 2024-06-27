# library/urls.py

from django.urls import path
from .views import InheritImageView
from . import views

urlpatterns = [
    path('images/', views.ListImageView.as_view(), name='list_image'),
    path('images/add/', views.AddImageView.as_view(), name='add_image'),
    path('images/inherit/', InheritImageView.as_view(), name='inherit_image'),
    # path('videos/', views.ListVideoView.as_view(), name='list_video'),
    # path('videos/add/', views.AddVideoView.as_view(), name='add_video'),
]
