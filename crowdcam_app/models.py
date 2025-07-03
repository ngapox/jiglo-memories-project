# crowdcam_app/models.py

from django.db import models
from django.utils.text import slugify
from django.conf import settings

class Event(models.Model):
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    event_date = models.DateField()
    unique_code = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Photo(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='event_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.event.name} uploaded at {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"