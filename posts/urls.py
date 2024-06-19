# blog/urls.py
from django.urls import path
from .views import create_post
from . import views

urlpatterns = [
    path('create/', create_post, name='create_post'),
    path('list/', views.post_list, name='post_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail')
]
