# crowdcam_app/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Event
from .forms import PhotoForm # Import our new form

def event_detail_view(request, unique_code):
    event = get_object_or_404(Event, unique_code=unique_code)

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.event = event
            photo.save()
            return redirect('event_detail', unique_code=event.unique_code)
    else:
        form = PhotoForm()

    # Get all photos for this event
    photos = event.photos.all().order_by('-uploaded_at')

    context = {
        'event': event,
        'form': form,
        'photos': photos,
    }

    return render(request, 'crowdcam_app/event_detail.html', context)