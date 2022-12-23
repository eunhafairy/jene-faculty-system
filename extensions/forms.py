from django import forms
from django.core.exceptions import ValidationError
from .models import Extension

class ExtensionForm(forms.ModelForm):
    class Meta:
        model=Extension
        fields = ('code','name', 'description')
        labels = {
            'code': 'Extension Code',
            'name': 'Extension Name',
            'description': 'Extension Description',
        }
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control my-5'}),
            'name': forms.TextInput(attrs={'class': 'form-control my-5'}),
            'description': forms.Textarea(attrs={'class': 'form-control my-5'}),
        }