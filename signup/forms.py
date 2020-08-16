from django import forms
from django.forms import ModelForm
from .models import email

class emailForm(forms.ModelForm):
    class Meta:
        model = email
        fields = ['address']

