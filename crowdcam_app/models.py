# crowdcam_app/models.py

from django.db import models
from django.utils.text import slugify

class Event(models.Model):
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