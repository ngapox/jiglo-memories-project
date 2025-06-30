# crowdcam_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('events/<slug:unique_code>/', views.event_detail_view, name='event_detail'),
]