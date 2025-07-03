# crowdcam_app/admin.py

from django.contrib import admin
from .models import Event, Photo # Make sure Photo is also imported

# Create a custom admin view for the Event model
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'host', 'event_date', 'unique_code')
    search_fields = ('name', 'host__username')

# Register your models here.
admin.site.register(Event, EventAdmin) # Register Event with its custom admin view
admin.site.register(Photo) # Keep the simple registration for Photo