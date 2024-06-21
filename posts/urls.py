# blog/urls.py
from django.urls import path
from .views import create_post
from . import views

urlpatterns = [
    path('create/', create_post, name='create_post'),
    path('list/', views.list_post, name='list_post'),
    path('post/<int:post_id>/', views.detail_post, name='detail_post')
]
