from django.shortcuts import render
from destination.models import Location
from django.views import View
# Create your views here.

def search(request):
    template_name = 'search/search_results.html'
    if request.method == 'GET':
        # Display the form for creating a post
        return render(request, template_name)
    
    elif request.method == 'POST':
        
        data={}
        return render(request, template_name, data)
    