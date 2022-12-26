from django import forms
from django.core.exceptions import ValidationError
from .models import Research

class ResearchForm(forms.ModelForm):
    class Meta:
        model=Research
        fields = ('title', 'status')
        labels = {
            'title': 'Research Title',
            'status': 'Status',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control my-5'}),
            'status': forms.Select(attrs={'class': 'form-select my-5'}),
        }
    #  ----------------- validation template ----------------------
    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     if 'Django' not in title:
    #         raise ValidationError("Validation error here")
    #     return title
