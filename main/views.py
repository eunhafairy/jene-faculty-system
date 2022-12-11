from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User
from table.models import FacultySubject
from subjects.models import Subject
from django.core import serializers
import json

# Create your views here.
class HomeView(TemplateView):
    template_name = "main/home.html"

class ProfileView(LoginRequiredMixin,TemplateView):
    template_name = "main/profile.html"
    model = User
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user.username)
        id = json.loads(serializers.serialize('json', FacultySubject.objects.all().filter(user=user)))
        subjects = []
        for i in id:
            subjects.append(Subject.objects.get(id = i.get('fields').get('subject')))
        # subjects = serializers.serialize('json', Subject.objects.all().filter(id=id))
        # context["subjects"] = subjects
        context["user"] = user
        context["subjects"] = subjects
        return context
