from django import forms
from django.core.exceptions import ValidationError
from .models import FacultySubject
from accounts.models import User
from django.core import serializers

class FacultySubjectForm(forms.ModelForm):

    class Meta:
        model=FacultySubject
        fields = ('subject',)
        labels = {
            'subject': 'Subject'
        }
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-select my-5'}),
        }
    #  ----------------- validation template --------------
