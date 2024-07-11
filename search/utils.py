from django.shortcuts import render
from django.db.models import Q
from destination.models import Location
from library.models import Image, Video
from django.db.models import Q

def search_locations(query):
    queries = query.split()
    if queries:
        combined_query = Q()
        for q in queries:
            combined_query |= Q(name__unaccent__icontains=query) | Q(description__unaccent__icontains=query) | Q(tags__name__unaccent__icontains=q)
        locations = Location.objects.filter(combined_query).distinct()
    else:
        locations = Location.objects.none()
    
    return locations
def search_images(query):
    queries = query
    if queries:
        images = Image.objects.filter(title__unaccent__icontains=queries).distinct()
    else:
        images = Image.objects.none()
    
    return images
def search_videos(query):
    queries = query
    if queries:
        videos = Video.objects.filter(title__unaccent__icontains=queries).distinct()
    else:
        videos = Video.objects.none()
    
    return videos
