from django import forms  
from .models import User  
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):
    
    username = forms.CharField(label='Username', min_length=5, max_length=50, widget=forms.TextInput(attrs={"class": "form-control my-5"}))  
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={"class": "form-control my-5", "type":"email"}))  
    password1 = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput(attrs={"class": "form-control my-5"}))  
    password2 = forms.CharField(label='Confirm password', max_length=100, widget=forms.PasswordInput(attrs={"class": "form-control my-5"}))  
    first_name = forms.CharField(label="First name", max_length=100, widget=forms.TextInput(attrs={"class": "form-control my-5"}))
    dept = forms.Select(attrs={'class': 'form-select my-5'}),
    last_name = forms.CharField(label="Last name", max_length=100, widget=forms.TextInput(attrs={"class": "form-control my-5"}))
    profile_image = forms.ImageField(label="Profile Image")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2','first_name','last_name','profile_image', 'dept')
    #---------------validations---------------
    def username_clean(self):  
        # Check if it exists
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")
        return username  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email Already Exist")  
        return email
    
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
    
    def save(self, commit = True):  
        user = User.objects.create_user(  
            username = self.cleaned_data['username'],  
            email = self.cleaned_data['email'],  
            password = self.cleaned_data['password1'],
            dept = self.cleaned_data['dept'],
            first_name = self.cleaned_data['first_name'],
            last_name = self.cleaned_data['last_name'],
            profile_image = self.cleaned_data['profile_image']

        )  
        return user  


class UpdateUserForm(forms.ModelForm):
    
    username = forms.CharField(label='Username', min_length=5, max_length=50, widget=forms.TextInput(attrs={"class": "form-control my-5"}))  
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={"class": "form-control my-5", "type":"email"}))  
    first_name = forms.CharField(label="First name", max_length=100, widget=forms.TextInput(attrs={"class": "form-control my-5"}))
    dept = forms.Select(attrs={'class': 'form-select my-5'}),

    last_name = forms.CharField(label="Last name", max_length=100, widget=forms.TextInput(attrs={"class": "form-control my-5"}))
    profile_image = forms.ImageField(label="Profile Image")

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name','last_name','profile_image', 'dept')
    #---------------validations---------------
    def username_clean(self):  
        # Check if it exists
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")
        return username  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email Already Exist")  
        return email


class CustomePasswordChangeForm(PasswordChangeForm):
    
    old_password = forms.CharField(
        label =_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True, "class": "form-control my-5"}
        ),
    )
    new_password1 = forms.CharField(
        label =_("New password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autofocus": True, "class": "form-control my-5"}
        ),
    )
    new_password2 = forms.CharField(
        label =_("Repeat"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autofocus": True, "class": "form-control my-5"}
        ),
    )


    class Meta:
        model = User
        fields = ('old_password', 'newpassword1', 'newpassword2')

    
    