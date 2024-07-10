# library/views.py

from urllib import request
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, TemplateView, View
from .models import Image, Video
from django.core.paginator import Paginator
from posts.models import Post
from destination.models import LocationImage, Location

# def image_gallery(request):
#     images = Image.objects.all()
#     image_urls = [image.image.url for image in images]
#     return render(request, 'library/list_image.html', {'image_urls': image_urls})

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

    @csrf_exempt 
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            image_title = request.POST.get('title')
            uploaded_image = request.FILES.get('image')

            new_image = Image(
                title=image_title,
                image=uploaded_image
            )
            new_image.save()
            
            # Redirect user to the create post page with a success message
            success = {
                    'success': 'Thêm hình ảnh thành công!'
                }
            return render(request, "library/add_image.html", success)

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

class ListVideoView(ListView):
    model = Video
    template_name = 'library/list_video.html'
    context_object_name = 'videos'
    paginate_by = 10

    def get_queryset(self):
        return Video.objects.all().order_by('-created_at')

class AddVideoView(View):
    template_name = 'library/add_video.html'
    success_url = reverse_lazy('list_video')

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        title = request.POST.get('title')
        upload = request.FILES.get('upload')
        youtube_url = request.POST.get('youtube_url')

        # Validate the input
        if not title:
            error = "Title is required."
        elif not upload and not youtube_url:
            error = "You must provide either a video file or a YouTube URL."
        elif upload and youtube_url:
            error = "You can only provide one type of video source."
        else:
            error = None

        if error:
            return render(request, self.template_name, {'error': error})

        video = Video(title=title, upload=upload, youtube_url=youtube_url)
        video.save()
        return redirect(self.success_url)


