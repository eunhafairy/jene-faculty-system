from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, TemplateView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, UpdateUserForm, CustomePasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from table.models import FacultySubject
from.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
# Create your views here.


class LoginInterfaceView(LoginView):
    template_name = "accounts/login.html"
    success_url="/posts"
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('post.list')
        return super().get(request, *args, **kwargs)

class LogoutInterfaceView(LogoutView):
    template_name = "accounts/logout.html"



class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/register.html"
    success_url = "/posts"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('post.list')
        return super().get(request, *args, **kwargs)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UpdateUserForm
    success_url = "/"
    template_name = "accounts/account_update.html"
    login_url = "/user/login"
    def get(self, request, *args, **kwargs):
        print("LOGGED IN:", self.request.user)
        return super().get(request, *args, **kwargs)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = "/"
    template_name = "accounts/account_delete.html"
    login_url = "/user/login"
   


class MySubjectsListView(LoginRequiredMixin, ListView):
    model = FacultySubject
    template_name="accounts/my_subjects.html"
    context_object_name = "tables"

    # template_name = "post/post_list.html"
    def get_queryset(self):
        qs = super().get_queryset() 
        print('qs',qs)
        return qs.filter(user=self.request.user)
    login_url = "/user/login"

def change_password(request):
    if request.method == 'POST':
        form = CustomePasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })