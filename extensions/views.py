from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.db.models import Q
from .models import Extension
from accounts.models import User
from .forms import ExtensionForm
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

# class MyDepartmentListView(LoginRequiredMixin, ListView):
#     model = User
#     context_object_name = "users"
#     template_name = "department/my_department_list.html"
#     login_url = "/user/login"

#     def get_queryset(self):
#         user = User.objects.filter(dept=self.request.user.dept)
#         print("head: ", user)
#         if(user):
#             return user.filter(~Q(role=1))
#         else:
#             return super().get_queryset()
    
#     # authorization
#     def get(self, request, *args, **kwargs):
#         head = Department.objects.filter(head=self.request.user)
#         if (head):
#             return super().get(request, *args, **kwargs)
#         print("not authorized", head)
#         return redirect('home')


# class PostDetailView(LoginRequiredMixin, DetailView):
#     model = Post
#     context_object_name = "post"
#     template_name = "post/post_detail.html"
#     login_url = "/user/login"

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
        return HttpResponseRedirect(self.get_success_url())
    
    # authorization
    # def get(self, request, *args, **kwargs):
    #     if self.request.user.role != "4" and self.request.user.role != "1":
    #         return redirect('home')
    #     return super().get(request, *args, **kwargs)



class ExtensionUpdateView(LoginRequiredMixin, UpdateView):
    model = Extension
    form_class = ExtensionForm
    success_url = "/extension"
    template_name = "extensions/extension_form.html"
    login_url = "/user/login"

class ExtensionDeleteView(LoginRequiredMixin, DeleteView):
    model = Extension
    success_url = "/extension"
    template_name = "extensions/extension_delete.html"
    login_url = "/user/login"
   
