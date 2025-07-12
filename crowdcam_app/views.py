# crowdcam_app/views.py
import stripe
from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login # import login
from django.contrib.auth.forms import UserCreationForm # import the form
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import PhotoForm, EventForm, ContactForm # Import our new form

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
        # Only process the form if the event has been paid for
        if event.is_paid:
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

@login_required
def create_event_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            # Create the event object in memory but don't save to the database yet
            event = form.save(commit=False)
            # Assign the currently logged-in user as the host
            event.host = request.user
            # Now, save the event to the database
            event.save()
            # Redirect to the user's dashboard where they'll see their new event
            return redirect('dashboard')
    else:
        form = EventForm()
    
    context = {
        'form': form
    }
    return render(request, 'crowdcam_app/event_form.html', context)

def audio_guest_book_view(request):
    return render(request, 'crowdcam_app/audio_guest_book.html')

def photo_booth_view(request):
    return render(request, 'crowdcam_app/photo_booth.html')

def crowdcam_view(request):
    return render(request, 'crowdcam_app/crowdcam.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Get the cleaned data from the form
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            event_date = form.cleaned_data.get('event_date', 'Not provided')
            message_body = form.cleaned_data['message']

            # Compose the email
            subject = f'New Inquiry from {name} via JiGloMemories.com'
            message = f"""
            You have a new contact form submission:

            From: {name}
            Email: {from_email}
            Event Date: {event_date}

            Message:
            {message_body}
            """
            send_mail(
                subject,
                message,
                from_email, # From
                ['your-business-email@example.com'], # To (replace with your actual email)
                fail_silently=False,
            )
            return redirect('thank_you')
    else:
        form = ContactForm()

    return render(request, 'crowdcam_app/contact.html', {'form': form})

def thank_you_view(request):
    return render(request, 'crowdcam_app/thank_you.html')

# crowdcam_app/views.py

@login_required
def event_update_view(request, event_id):
    # Get the event object that belongs to the current user
    event = get_object_or_404(Event, id=event_id, host=request.user)

    if request.method == 'POST':
        # Populate the form with the submitted data and the existing event instance
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        # Populate the form with the existing data of the event
        form = EventForm(instance=event)

    context = {
        'form': form
    }
    return render(request, 'crowdcam_app/event_form.html', context)

@login_required
def event_delete_view(request, event_id):
    event = get_object_or_404(Event, id=event_id, host=request.user)

    if request.method == 'POST':
        event.delete()
        return redirect('dashboard')

    context = {
        'event': event
    }
    return render(request, 'crowdcam_app/event_confirm_delete.html', context)

@login_required
def payment_instructions_view(request, event_id):
    event = get_object_or_404(Event, id=event_id, host=request.user)
    context = {
        'event': event
    }
    return render(request, 'crowdcam_app/payment_instructions.html', context)