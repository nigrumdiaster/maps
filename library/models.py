# library/models.py

from django.db import models

class Image(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='library/images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='library/videos/')
    youtube_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

