from django.db import models
from taggit.managers import TaggableManager
from destination.models import Location
# Create your models here.
class Journey(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    tags = TaggableManager()
    sound = models.FileField(upload_to='sounds/journey/', blank=True, null=True)
    image = models.ImageField(upload_to='images/journey', blank=True, null=True)
    locations = models.ManyToManyField(Location, related_name='journeys')
    def __str__(self):
        return self.name