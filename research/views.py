from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from .models import Research
from .forms import ResearchForm
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
            

    # authorization
    # def get(self, request, *args, **kwargs):
    #     if self.request.user.role != "2":
    #         print("not authorized", self.request.user.role)
    #         return redirect('home')
        # return super().get(request, *args, **kwargs)


# class PostDetailView(LoginRequiredMixin, DetailView):
#     model = Post
#     context_object_name = "post"
#     template_name = "post/post_detail.html"
#     login_url = "/user/login"

class ResearchCreateView(LoginRequiredMixin, CreateView):
    model = Research
    form_class = ResearchForm
    success_url = "/research"
    template_name = "research/research_form.html"
    login_url = "/user/login"
    
    # authorization
    # def get(self, request, *args, **kwargs):
    #     if self.request.user.role != "2":
    #         return redirect('home')
    #     return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ResearchUpdateView(LoginRequiredMixin, UpdateView):
    model = Research
    form_class = ResearchForm
    success_url = "/research"
    template_name = "research/research_form.html"
    login_url = "/user/login"

class ResearchDeleteView(LoginRequiredMixin, DeleteView):
    model = Research
    success_url = "/research"
    template_name = "research/research_delete.html"
    login_url = "/user/login"
   
