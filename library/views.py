# library/views.py

from urllib import request
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, TemplateView
from .models import Image, Video
from django.core.paginator import Paginator
from posts.models import Post
from destination.models import LocationImage

class ListImageView(ListView):
    model = Image
    template_name = 'library/list_image.html'

    def list_image(request):
    image = Image.objects.all().order_by('-created_at')
    paginator = Paginator(image, 10)  # Hiển thị 10 bài viết trên mỗi trang

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'library/list_image.html', {'page_obj': page_obj})

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

    def get(self, request, *args, **kwargs):
        # Fetch image URLs from Post and Destination models
        posts_images = Post.objects.values_list('image', flat=True)
        destinations_images = LocationImage.objects.values_list('images', flat=True)

        # Print the values to check
        print("Post images:", list(posts_images))
        print("Destination images:", list(destinations_images))

        # Create new Image instances for each inherited image URL
        for image_url in posts_images:
            if image_url:
                Image.objects.create(title='Inherited from Post', image=image_url)

        for image_url in destinations_images:
            if image_url:
                Image.objects.create(title='Inherited from Destination', image=image_url)

        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        return Image.objects.all()
