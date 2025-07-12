# crowdcam_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage_view, name='homepage'),
    path('signup/', views.signup_view, name='signup'),
    path('my-events/', views.dashboard_view, name='dashboard'),
    path('create-event/', views.create_event_view, name='create_event'),
    path('services/audio-guest-book/', views.audio_guest_book_view, name='audio_guest_book'),
    path('services/photo-booth/', views.photo_booth_view, name='photo_booth'),
    path('services/crowdcam/', views.crowdcam_view, name='crowdcam'),
    path('contact/', views.contact_view, name='contact'),
    path('contact/thank-you/', views.thank_you_view, name='thank_you'),
    path('create-checkout-session/<int:event_id>/', views.create_checkout_session_view, name='create_checkout_session'),
    path('payment-success/', views.payment_success_view, name='payment_success'),
    path('my-events/<int:event_id>/edit/', views.event_update_view, name='event_update'),
    path('my-events/<int:event_id>/delete/', views.event_delete_view, name='event_delete'),
    path('my-events/<int:event_id>/payment-instructions/', views.payment_instructions_view, name='payment_instructions'),
    path('events/<slug:unique_code>/', views.event_detail_view, name='event_detail'),
]
