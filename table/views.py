from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
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
    success_url = "/user/my-subjects"
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
        print('is it existing: ',existing)
        if existing:
            return redirect('table.error.exist')
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class FacultySubjectAlreadyExists(LoginRequiredMixin, TemplateView):
    template_name = "table/faculty_subject_already_exists.html"

class FacultySubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = FacultySubject
    success_url = "/user/my-subjects"
    template_name = "table/faculty_subject_delete.html"
    login_url = "/user/login"
 
