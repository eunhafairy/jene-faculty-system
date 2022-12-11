from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.core.exceptions import ValidationError

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .models import FacultySubject
from .forms import FacultySubjectForm

from django.core.exceptions import BadRequest


import json
from django.core import serializers

# Create your views here.
class FacultySubjectCreateView(LoginRequiredMixin, CreateView):
    model = FacultySubject
    success_url = "/me"
    template_name = "table/faculty_subject_form.html"
    login_url = "/user/login"
    form_class = FacultySubjectForm
    # authorization
    # def get(self, request, *args, **kwargs):
    #     if self.request.user.role != "1":
    #         return redirect('home')
    #     return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        print("Self object ", self.object.subject)
        existing = FacultySubject.objects.filter(subject = self.object.subject, user = self.request.user)
        if existing:
            raise ValidationError('Invalid request. Subject is existing.')
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
