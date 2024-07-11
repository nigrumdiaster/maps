from django.shortcuts import render
from destination.models import Location
from library.models import Image, Video
from django.views import View
from .utils import search_locations, search_images, search_videos
from django.core.paginator import Paginator
# Create your views here.



from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator

def search(request: HttpRequest) -> HttpResponse:
    template_name = 'search/search_results.html'
    search_query = request.GET.get('searchQuery', '')

    # Pagination for locations (10 per page)
    locations_per_page = 10
    if search_query:
        locations = search_locations(search_query).order_by('-created_at')
            
    else:
        locations = Location.objects.all().order_by('-created_at')
    location_paginator = Paginator(locations, locations_per_page)
    location_page_number = request.GET.get('location_page')
    location_page_obj = location_paginator.get_page(location_page_number)

    # # Pagination for images (12 per page)
    # images_per_page = 12
    # if search_query:
    #     images = search_images(search_query).order_by('-created_at')
            
    # else:
    #     images = Image.objects.all().order_by('-created_at')
    # image_paginator = Paginator(images, images_per_page)
    # image_page_number = request.GET.get('image_page')
    # image_page_obj = image_paginator.get_page(image_page_number)

    # # Pagination for videos (4 per page)
    # videos_per_page = 4
    # if search_query:
    #     videos = search_videos(search_query).order_by('-created_at')
    # else:
    #     videos = Video.objects.all().order_by('-created_at')
    # video_paginator = Paginator(videos, videos_per_page)
    # video_page_number = request.GET.get('video_page')
    # video_page_obj = video_paginator.get_page(video_page_number)

    data = {
        'location_page_obj': location_page_obj,
        # 'image_page_obj': image_page_obj,
        # 'video_page_obj': video_page_obj,
        # 'search_query': search_query,
    }

    return render(request, template_name, data)
