from django import forms
from django.core.exceptions import ValidationError
from .models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model=Department
        fields = ('code','name', 'description')
        labels = {
            'code': 'Department Code',
            'name': 'Department Name',
            'description': 'Department Description',
        }
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control my-5'}),
            'name': forms.TextInput(attrs={'class': 'form-control my-5'}),
            # 'head': forms.Select(attrs={'class': 'form-select my-5'}),
            'description': forms.Textarea(attrs={'class': 'form-control my-5'}),
        }