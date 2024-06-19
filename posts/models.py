from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField

class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('News', 'Tin tức'),
        ('Travel', 'Du lịch'),
        ('History', 'Lịch sử'),
    ]

    title = models.CharField(max_length=100, default=' ')
    post_type = models.CharField(max_length=50, choices=POST_TYPE_CHOICES)
    content = RichTextField()
    source_url = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title[:50]