from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User
# Create your views here.
class HomeView(TemplateView):
    template_name = "main/home.html"

class ProfileView(LoginRequiredMixin,TemplateView):
    template_name = "main/profile.html"
    model = User
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["user"] = User.objects.get(username=self.request.user.username)
        return context
