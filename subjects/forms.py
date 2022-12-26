from django import forms
from django.core.exceptions import ValidationError
from .models import Subject

class SubjectForm(forms.ModelForm):
    class Meta:
        model=Subject
        fields = ('code', 'name')
        labels = {
            'name': 'Course Name',
            'code': 'Course Code',
        }
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control my-5'}),
            'name': forms.TextInput(attrs={'class': 'form-control my-5'}),
        }
    #  ----------------- validation template ----------------------
    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     if 'Django' not in title:
    #         raise ValidationError("Validation error here")
    #     return title
