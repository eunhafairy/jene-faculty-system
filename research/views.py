from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from .models import Research
from .forms import ResearchForm
from logs.models import Log
# Create your views here.

class ResearchListView(LoginRequiredMixin, ListView):
    model = Research
    context_object_name = "research"
    template_name = "research/research_list.html"
    login_url = "/user/login"

    def get_queryset(self):
        print('myrole', self.request.user.role)
        if self.request.user.role == "1" or self.request.user.role == "2":
            return super().get_queryset()
        else:
            return self.request.user.research.all()
            

class ResearchCreateView(LoginRequiredMixin, CreateView):
    model = Research
    form_class = ResearchForm
    success_url = "/research"
    template_name = "research/research_form.html"
    login_url = "/user/login"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        Log(log_code='research_create', log_message=f'[{self.request.user.username}] created research [{self.object.title}]').save()
        return HttpResponseRedirect(self.get_success_url())



class ResearchUpdateView(LoginRequiredMixin, UpdateView):
    model = Research
    form_class = ResearchForm
    success_url = "/research"
    template_name = "research/research_form.html"
    login_url = "/user/login"
    def post(self, request, *args, **kwargs):
        title = self.get_form()['title'].value()
        username = self.request.user.username
        if self.get_form().is_valid():
            Log(log_code='research_update', log_message=f'[{username}] updated research [{title}]').save()
        return super().post(request, *args, **kwargs)

class ResearchDeleteView(LoginRequiredMixin, DeleteView):
    model = Research
    success_url = "/research"
    template_name = "research/research_delete.html"
    login_url = "/user/login"
    def post(self, request, *args, **kwargs):
        target = Research.objects.get(id=self.kwargs["pk"])
        user = self.request.user.username
        Log(log_code='research_delete', log_message=f'[{user}] deleted the research [{target.title}]').save()
        return super().post(request, *args, **kwargs)
   
   
