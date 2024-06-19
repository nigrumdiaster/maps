# destination/views.py

from django.shortcuts import render, redirect
from .forms import LocationForm
from geopy.geocoders import Nominatim

def create_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            geolocator = Nominatim(user_agent="destination")
            location = geolocator.geocode(instance.address)
            if location:
                instance.latitude = location.latitude
                instance.longitude = location.longitude
            instance.save()
            return redirect('create_location') 
    else:
        form = LocationForm()
    return render(request, 'destination/create_location.html', {'form': form})
