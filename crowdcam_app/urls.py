# crowdcam_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage_view, name='homepage'),
    path('signup/', views.signup_view, name='signup'),
    path('events/<slug:unique_code>/', views.event_detail_view, name='event_detail'),
]