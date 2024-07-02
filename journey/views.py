from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Journey
from taggit.utils import parse_tags



class Create_journey(View):
    template_name = 'journey/create_journey.html'
    
    def get(self, request):
        # Display the form for creating a journey
        return render(request, self.template_name)

    @csrf_exempt
    def post(self, request):
        try:
            journey_name = request.POST.get('journeyName')
            journey_description = request.POST.get('journeyDescription')
            journey_tags = request.POST.get('journeyTags')
            journey_song = request.POST.get('journeySong')
            uploaded_image = request.FILES.get('journeyImage')
            

            # Create a new Location object and save it
            new_journey = Journey(
                name=journey_name,
                description=journey_description,
                sound_url=journey_song,
                image=uploaded_image
            )
            new_journey.save()
            # Add tags to the new location if provided
            if journey_tags:
                tags = parse_tags(journey_tags)
                new_journey.tags.add(*tags)
            
            success = {
                'success': 'Tạo điểm đến thành công!'
            }

            # Redirect to a success page or the journey detail page
            return render(request, self.template_name, success)
        
        except Exception as e:
            error = {
                'error': 'Không tạo được điểm đến!'
            }
            print(f"Error: {e}")
            return render(request, self.template_name, error)
