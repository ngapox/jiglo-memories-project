# crowdcam_app/views.py

from django.shortcuts import render, get_object_or_404
from .models import Event

def event_detail_view(request, unique_code):
    # Get the specific event object from the database using the unique_code from the URL
    event = get_object_or_404(Event, unique_code=unique_code)

    # Create a context dictionary to pass the event object to the template
    context = {
        'event': event
    }

    # Render the HTML template, passing the context to it
    return render(request, 'crowdcam_app/event_detail.html', context)