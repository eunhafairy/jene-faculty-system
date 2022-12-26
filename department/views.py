from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.db.models import Q
from .models import Department
from accounts.models import User
from .forms import DepartmentForm
from logs.models import Log
# Create your views here.

class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    context_object_name = "departments"
    template_name = "department/department_list.html"
    login_url = "/user/login"
    
    # authorization
    def get(self, request, *args, **kwargs):
        if self.request.user.role != "1" and self.request.user.role != "4":
            print("not authorized", self.request.user.role)
            return redirect('home')
        return super().get(request, *args, **kwargs)

class MyDepartmentListView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = "users"
    template_name = "department/my_department_list.html"
    login_url = "/user/login"

    def get_queryset(self):
        user = User.objects.filter(dept=self.request.user.dept)
        print("head: ", user)
        if(user):
            return user.filter(~Q(role=1))
        else:
            return super().get_queryset()
    
    # authorization
    def get(self, request, *args, **kwargs):
        head = Department.objects.filter(head=self.request.user)
        if (head):
            return super().get(request, *args, **kwargs)
        print("not authorized", head)
        return redirect('home')


# class PostDetailView(LoginRequiredMixin, DetailView):
#     model = Post
#     context_object_name = "post"
#     template_name = "post/post_detail.html"
#     login_url = "/user/login"

class DepartmentCreateView(LoginRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    success_url = "/department"
    template_name = "department/department_form.html"
    login_url = "/user/login"
    
    # authorization
    def get(self, request, *args, **kwargs):
        if self.request.user.role != "4" and self.request.user.role != "1":
            return redirect('home')
        return super().get(request, *args, **kwargs)
    # logs
    def post(self, request, *args, **kwargs):
        code = self.get_form()['code'].value()
        username = self.request.user.username
        if self.get_form().is_valid():
            Log(log_code='department_create', log_message=f'[{username}] created department [{code}]').save()
        return super().post(request, *args, **kwargs)



class DepartmenthUpdateView(LoginRequiredMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    success_url = "/department"
    template_name = "department/department_form.html"
    login_url = "/user/login"
    def post(self, request, *args, **kwargs):
        code = self.get_form()['code'].value()
        username = self.request.user.username
        if self.get_form().is_valid():
            Log(log_code='department_update', log_message=f'[{username}] updated department [{code}]').save()
        return super().post(request, *args, **kwargs)

class DepartmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Department
    success_url = "/department"
    template_name = "department/department_delete.html"
    login_url = "/user/login"
    def post(self, request, *args, **kwargs):
        target = Department.objects.get(id=self.kwargs["pk"])
        user = self.request.user.username
        Log(log_code='department_delete', log_message=f'[{user}] deleted the department [{target.code}]').save()
        return super().post(request, *args, **kwargs)
   
