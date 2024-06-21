from django.shortcuts import render
from geopy.geocoders import Nominatim
from .models import Location, LocationImage
from django.views import View
from taggit.utils import parse_tags
from django.views.decorators.csrf import csrf_exempt


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
            uploaded_images = request.FILES.getlist('file')  # Adjusted to 'file[]' for Dropzone.js

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
# class List_location(View):
#     template_name = 'destination/list_location.html'
#     def get(self, request):
#         location = Location.objects.all().filter().order_by('-id')
#         item_count = location.count()
#         items_per_page = 10
#         page_count = item_count // items_per_page + (1 if item_count % items_per_page > 0 else 0)
        
#         if(request.GET.get('trang') is not None):
#             try:
#                 page = int(request.GET.get('trang'))
#                 #vị trí bắt đầu trang
#                 start_index = (page - 1) * items_per_page
#                 #vị trí cuối trang
#                 end_index = start_index + items_per_page
#                 if page > page_count or page <= 0:
#                     return render(request, template_error)
#                 else:
#                     pre_page = 1 if(page == 1) else page - 1
#                     next_page = page_count if(page == page_count) else page + 1
#                     tintuc = tintuc[int(start_index):int(end_index)]
#                     number_page = [i for i in range(1, page_count + 1)]
#                     data = {
#                         "tintuc": tintuc,
#                         "tintucmoi": tintucmoi,
#                         "chuyenmuc": chuyenmuc, 
#                         "banner": banner,
#                         'page_count': number_page, 
#                         "title": "Tin Tức", 
#                         "page": page, 
#                         "pre_page": pre_page, 
#                         "next_page": next_page, 
#                         "len_page_count": len(number_page)
#                     }
#                     return render(request, self.template_name, data)
#             except:
#                 return render(request, template_error)
#         elif (request.GET.get('s') is not None):
#             try:
#                 tieude = request.GET.get('s')
#                 tintuc = TinTuc.objects.all().filter(TieuDe__icontains=tieude).order_by('-id')
#                 data = {
#                     "tintuc": tintuc,
#                     "tintucmoi": tintucmoi, 
#                     "chuyenmuc": chuyenmuc, 
#                     "banner": banner,
#                     "title": "Tin Tức", 
#                 }
#                 return render(request, self.template_name, data)
#             except:
#                 return render(request, template_error)
#         else:
#             try:
#                 tintuc = tintuc[0:8]
#                 number_page = [i for i in range(1, page_count + 1)]
#                 data = {
#                     "tintuc": tintuc,
#                     "tintucmoi": tintucmoi, 
#                     "chuyenmuc": chuyenmuc, 
#                     "banner": banner,
#                     'page_count': number_page, 
#                     "title": "Tin Tức", 
#                     "page": 1,      
#                     "len_page_count": len(number_page)
#                 }
#                 return render(request, self.template_name, data)
#             except:
#                 return render(request, template_error)


#         return render(request, self.template_name)
    