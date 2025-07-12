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

@login_required
def create_checkout_session_view(request, event_id):
    event = get_object_or_404(Event, id=event_id, host=request.user)

    # Configure the Stripe API key
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Build the URLs for success and cancellation
    success_url = request.build_absolute_uri(reverse('payment_success')) + '?session_id={CHECKOUT_SESSION_ID}'
    cancel_url = request.build_absolute_uri(reverse('dashboard'))

    # Define the product and price for Stripe
    line_items = [{
        'price_data': {
            'currency': 'usd', # You can change this to your local currency if supported
            'product_data': {
                'name': f"Activation for event: {event.name}",
            },
            'unit_amount': int(event.price * 100), # Price in cents
        },
        'quantity': 1,
    }]

    try:
        # Create a new Checkout Session with the Stripe API
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            client_reference_id=event.id # Pass the event ID to track the payment
        )

        # Save the checkout session ID to our event model
        event.stripe_checkout_id = checkout_session['id']
        event.save()

        # Redirect the user to the Stripe-hosted checkout page
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        # Handle any errors here (e.g., log them, show a generic error page)
        return render(request, 'crowdcam_app/generic_error.html', {'error': str(e)})
# crowdcam_app/views.py

def payment_success_view(request):
    # Configure the Stripe API key
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session_id = request.GET.get('session_id')
    event = None

    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)

            # Check the payment status from the session
            if session.payment_status == 'paid':
                event_id = session.client_reference_id
                event = get_object_or_404(Event, id=event_id)

                # Proactively mark as paid, even before the webhook arrives
                event.is_paid = True
                event.save()
        except Exception as e:
            print(e) # For debugging

    context = {
        'event': event
    }
    return render(request, 'crowdcam_app/payment_success.html', context)

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