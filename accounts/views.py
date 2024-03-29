from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, TemplateView, UpdateView, DeleteView, DetailView
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, UpdateUserForm, CustomePasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from table.models import FacultySubject, FacultyExtension
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth import login as auth_login

from django.shortcuts import render, redirect
from django.core import serializers
from subjects.models import Subject
from logs.models import Log

from extensions.models import Extension

import json
# Create your views here.


class LoginInterfaceView(LoginView):
    template_name = "accounts/login.html"
    success_url="/posts"
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('post.list')
        return super().get(request, *args, **kwargs)
    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        Log(log_code='login', log_message=f'[{form.get_user()}] logged in').save()
        return HttpResponseRedirect(self.get_success_url())


class LogoutInterfaceView(LogoutView):
    template_name = "accounts/logout.html"
    def dispatch(self, request, *args, **kwargs):
        print("logout", request)
        Log(log_code='logout', log_message=f'[{request.user.username}] logged out').save()
        return super().dispatch(request, *args, **kwargs)


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/register.html"
    success_url = "/posts"


    def post(self, request, *args, **kwargs):
        print("hello", self.get_form()['username'].value())
        username = self.get_form()['username'].value()
        if self.get_form().is_valid():
            Log(log_code='signup', log_message=f'[{username}] registered').save()
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('post.list')
        return super().get(request, *args, **kwargs)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UpdateUserForm
    success_url = "/home"
    template_name = "accounts/account_update.html"
    login_url = "/user/login"
    def post(self, request, *args, **kwargs):
        target = self.get_form()['username'].value()
        if target == self.request.user.username:
            Log(log_code='account_update', log_message=f'[{self.request.user.username}] updated the their profile').save()
        else:
            Log(log_code='account_update', log_message=f'[{self.request.user.username}] updated the [{target}]\'s profile').save()
            
        return super().post(request, *args, **kwargs)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = "/home"
    template_name = "accounts/account_delete.html"
    login_url = "/user/login"
    def post(self, request, *args, **kwargs):
        target = User.objects.get(id=self.kwargs["pk"])
        user = self.request.user.username
        print("delete",target.username, " | ", self.request.user.username)
        if target.username == self.request.user.username:
            Log(log_code='account_delete', log_message=f'[{user}] deleted the their profile').save()
        else:
            Log(log_code='account_delete', log_message=f'[{user}] deleted the [{target.username}]\'s profile').save()
            
        return super().post(request, *args, **kwargs)

   


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

class MyExtensionsListView(LoginRequiredMixin, ListView):
    model = FacultyExtension
    template_name="accounts/my_extensions.html"
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

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = "user"
    template_name = "accounts/user_detail.html"
    login_url = "/auth"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs["pk"])
        id = json.loads(serializers.serialize('json', FacultySubject.objects.all().filter(user=user)))
        id_ext = json.loads(serializers.serialize('json', FacultyExtension.objects.all().filter(user=user)))

        subjects = []
        ext = []
        for i in id:
            subjects.append(Subject.objects.get(id = i.get('fields').get('subject')))
        for i in id_ext:
            ext.append(Extension.objects.get(id = i.get('fields').get('ext')))
        # subjects = serializers.serialize('json', Subject.objects.all().filter(id=id))
        # context["subjects"] = subjects
        context["user"] = user
        context["subjects"] = subjects
        context["ext"] = ext
        return context
