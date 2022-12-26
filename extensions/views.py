from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.db.models import Q
from .models import Extension
from accounts.models import User
from .forms import ExtensionForm
from logs.models import Log

# Create your views here.

class ExtensionListView(LoginRequiredMixin, ListView):
    model = Extension
    context_object_name = "extensions"
    template_name = "extensions/extension_list.html"
    login_url = "/user/login"
    
    # authorization
    def get(self, request, *args, **kwargs):
        if self.request.user.role == "1" or self.request.user.role == "3":
            return super().get(request, *args, **kwargs)
        print("not authorized", self.request.user.role)
        return redirect('my-extensions')


class ExtensionsCreateView(LoginRequiredMixin, CreateView):
    model = Extension
    form_class = ExtensionForm
    success_url = "/extension"
    template_name = "extensions/extension_form.html"
    login_url = "/user/login"
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())\
      # logs
    def post(self, request, *args, **kwargs):
        code = self.get_form()['code'].value()
        username = self.request.user.username
        if self.get_form().is_valid():
            Log(log_code='extension_create', log_message=f'[{username}] created extension [{code}]').save()
        return super().post(request, *args, **kwargs)
    


class ExtensionUpdateView(LoginRequiredMixin, UpdateView):
    model = Extension
    form_class = ExtensionForm
    success_url = "/extension"
    template_name = "extensions/extension_form.html"
    login_url = "/user/login"
    def post(self, request, *args, **kwargs):
        code = self.get_form()['code'].value()
        username = self.request.user.username
        if self.get_form().is_valid():
            Log(log_code='extension_update', log_message=f'[{username}] updated extension [{code}]').save()
        return super().post(request, *args, **kwargs)

class ExtensionDeleteView(LoginRequiredMixin, DeleteView):
    model = Extension
    success_url = "/extension"
    template_name = "extensions/extension_delete.html"
    login_url = "/user/login"
    def post(self, request, *args, **kwargs):
        target = Extension.objects.get(id=self.kwargs["pk"])
        user = self.request.user.username
        Log(log_code='extension_delete', log_message=f'[{user}] deleted the extension [{target.code}]').save()
        return super().post(request, *args, **kwargs)
   

   
