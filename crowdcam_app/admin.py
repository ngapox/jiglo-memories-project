# crowdcam_app/admin.py

from django.contrib import admin
from .models import Event, Photo

# This is a custom "action" for the admin panel
@admin.action(description="Mark selected events as paid")
def mark_as_paid(modeladmin, request, queryset):
    queryset.update(is_paid=True)

class EventAdmin(admin.ModelAdmin):
    # Shows these fields in the event list
    list_display = ('name', 'host', 'event_date', 'is_paid')
    # Adds a filter sidebar to easily find paid/unpaid events
    list_filter = ('is_paid', 'event_date')
    # Adds a search bar
    search_fields = ('name', 'host__username')
    # Adds our new custom action
    actions = [mark_as_paid]

admin.site.register(Event, EventAdmin)
admin.site.register(Photo)