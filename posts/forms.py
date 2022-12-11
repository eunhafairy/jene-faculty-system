from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields = ('title', 'type', 'content')
        labels = {
            'content': 'Content'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control my-5'}),
            'type': forms.Select(attrs={'class': 'form-select my-5'}),
            'content': forms.Textarea(attrs={'class': 'form-control mb5'})

        }
    #  ----------------- validation template ----------------------
    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     if 'Django' not in title:
    #         raise ValidationError("Validation error here")
    #     return title
