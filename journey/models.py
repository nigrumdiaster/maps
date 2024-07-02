from django.db import models
from taggit.managers import TaggableManager
from destination.models import Location
# Create your models here.
class Journey(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    tags = TaggableManager()
    sound_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='images/journey', blank=True, null=True)

    def __str__(self):
        return self.name