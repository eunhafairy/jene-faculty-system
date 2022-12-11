from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from .models import Post
from .forms import PostForm
# Create your views here.

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = "posts"
    template_name = "post/post_list.html"
    
    # def get_queryset(self):
    #     return self.request.user.posts.all()
    login_url = "/user/login"

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    context_object_name = "post"
    template_name = "post/post_detail.html"
    login_url = "/user/login"

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = "/posts"
    template_name = "post/post_form.html"
    login_url = "/user/login"
    def get(self, request, *args, **kwargs):
        if self.request.user.role == "5":
            return redirect('post.list')
        return super().get(request, *args, **kwargs)
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = "/posts"
    template_name = "post/post_form.html"
    login_url = "/user/login"
    def get(self, request, *args, **kwargs):
        if self.request.user.role == "5":
            return redirect('post.list')
        return super().get(request, *args, **kwargs)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = "/posts"
    template_name = "post/post_delete.html"
    login_url = "/user/login"
    def get(self, request, *args, **kwargs):
        if self.request.user.role == "5":
            return redirect('post.list')
        return super().get(request, *args, **kwargs)
   
