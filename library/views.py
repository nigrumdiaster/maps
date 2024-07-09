# library/views.py

from urllib import request
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, TemplateView
from .models import Image, Video
from django.core.paginator import Paginator
from posts.models import Post
from destination.models import LocationImage, Location

class ListImageView(ListView):
    model = Image
    template_name = 'library/list_image.html'
    context_object_name = 'images'
    paginate_by = 10  # Hiển thị 10 hình ảnh trên mỗi trang

    def get_queryset(self):
        return Image.objects.all().order_by('-created_at')


class AddImageView(CreateView):
    model = Image
    fields = ['title', 'image']
    template_name = 'library/add_image.html'
    success_url = reverse_lazy('list_image')

# class ListVideoView(ListView):
#     model = Video
#     template_name = 'library/list_video.html'

# class AddVideoView(CreateView):
#     model = Video
#     fields = ['title', 'video']
#     template_name = 'library/add_video.html'
#     success_url = reverse_lazy('list_video')

class InheritImageView(TemplateView):
    template_name = 'library/inherit_image.html'
    context_object_name = 'images'
    paginate_by = 10

    def inherit_images(self):
        posts_images = Post.objects.values_list('image', 'title')
        destinations_images = LocationImage.objects.values_list('images', 'location_id')

        for image_url, title in posts_images:
            if image_url and not Image.objects.filter(image=image_url).exists():
                Image.objects.create(title=title, image=image_url)

        for image_url, location_id in destinations_images:
            location_name=Location.objects.get(pk=location_id)
            if image_url and not Image.objects.filter(image=image_url).exists():
                Image.objects.create(title=location_name, image=image_url)

    def get(self, request, *args, **kwargs):
        # Inherit images if they don't already exist
        self.inherit_images()
