# crowdcam_app/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login # import login
from django.contrib.auth.forms import UserCreationForm # import the form
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import PhotoForm # Import our new form

@login_required
def dashboard_view(request):
    # Get events created ONLY by the currently logged-in user
    events = Event.objects.filter(host=request.user).order_by('-event_date')
    context = {
        'events': events
    }
    return render(request, 'crowdcam_app/dashboard.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log the user in immediately
            return redirect('homepage')
    else:
        form = UserCreationForm()
    return render(request, 'crowdcam_app/signup.html', {'form': form})

def homepage_view(request):
    # Get all event objects, ordered by the most recent date first
    events = Event.objects.all().order_by('-event_date')
    context = {
        'events': events
    }
    return render(request, 'crowdcam_app/homepage.html', context)

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