# crowdcam_app/forms.py

from django import forms
from .models import Photo, Event

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image'] # We only want to show the image upload field to the user

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'event_date'] # These are the only fields the user needs to fill out
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    event_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))