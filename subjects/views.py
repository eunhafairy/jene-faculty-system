from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from .models import Subject
from .forms import SubjectForm
from logs.models import Log
# Create your views here.

class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    context_object_name = "subjects"
    # template_name = "post/post_list.html"
    login_url = "/user/login"
    # authorization
    def get(self, request, *args, **kwargs):
        if self.request.user.role != "1":
            return redirect('home')
        return super().get(request, *args, **kwargs)

class SubjectCreateView(LoginRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    success_url = "/subjects"
    template_name = "subjects/subject_form.html"
    login_url = "/user/login"
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        Log(log_code='subject_create', log_message=f'[{self.request.user.username}] created subject [{self.object.name}]').save()
        return HttpResponseRedirect(self.get_success_url())


class SubjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    success_url = "/subjects"
    template_name = "subjects/subject_form.html"
    login_url = "/user/login"
    def get(self, request, *args, **kwargs):
        if self.request.user.role != "1":
            return redirect('home')
        return super().get(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        name = self.get_form()['name'].value()
        username = self.request.user.username
        if self.get_form().is_valid():
            print("updated subject", name, username, self.get_form().is_valid())
            Log(log_code='subject_update', log_message=f'[{username}] updated subject [{name}]').save()
        return super().post(request, *args, **kwargs)

class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Subject
    success_url = "/subjects"
    template_name = "subjects/subject_delete.html"
    login_url = "/user/login"
    def get(self, request, *args, **kwargs):
        if self.request.user.role != "1":
            return redirect('home')
        return super().get(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        target = Subject.objects.get(id=self.kwargs["pk"])
        user = self.request.user.username
        Log(log_code='subject_delete', log_message=f'[{user}] deleted the post [{target.name}]').save()
        return super().post(request, *args, **kwargs)
