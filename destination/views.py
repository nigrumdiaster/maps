from django.shortcuts import render
from geopy.geocoders import Nominatim
from .models import Location, LocationImage
from django.views import View
from taggit.utils import parse_tags
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

template_error = '404error.html'
class Create_location(View):
    template_name = 'destination/create_location.html'
    
    def get(self, request):
        # Display the form for creating a location
        return render(request, self.template_name)
    @csrf_exempt
    def post(self, request):
        # try:
            location_name = request.POST.get('locationName')
            location_description = request.POST.get('locationDescription')
            location_tags = request.POST.get('locationTags')
            location_address = request.POST.get('locationAddress')
            uploaded_images = request.FILES.getlist('file')  

            # Use Geopy to geocode the location address
            geolocator = Nominatim(user_agent="destination")
            location = geolocator.geocode(location_address, timeout=10000)

            if location:
                location_latitude = location.latitude
                location_longitude = location.longitude
            else:
                location_latitude = None
                location_longitude = None

            # Create a new Location object and save it
            new_location = Location(
                name=location_name,
                description=location_description,
                address=location_address,
                latitude=location_latitude,
                longitude=location_longitude
            )
            new_location.save()

            # Add tags to the new location if provided
            if location_tags:
                tags = parse_tags(location_tags)
                new_location.tags.add(*tags)

            # Process and save each uploaded image
            for image in uploaded_images:
                new_image = LocationImage(location=new_location, images=image)
                new_image.save()

            # Prepare context for rendering the template
            context = {
                'message': 'Location created successfully!'
            }
            return render(request, self.template_name, context)
        
        # except Exception as e:
        #     print(f"Error: {e}")
        #     return render(request, template_error)
class List_location(View):
    template_name = 'destination/list_location.html'
    def get(self, request):
        
        locations = Location.objects.all()
        paginator = Paginator(locations, 10)  # Show 10 locations per page

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        data = {'page_obj': page_obj}

        return render(request, self.template_name, data)
    
class Detail_location(View):
    template_name = 'destination/detail_location.html'
    def get(self, request):
        return render(request, self.template_name)




