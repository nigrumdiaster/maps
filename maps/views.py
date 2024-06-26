from django.shortcuts import render
from django.views import View





# Create your views here.
template_error = '404error.html'
class Create_location(View):
    template_name = 'destination/create_location.html'