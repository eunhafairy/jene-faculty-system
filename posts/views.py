from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from logs.models import Log
from .models import Post
from .forms import PostForm
# Create your views here.

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = "posts"
    template_name = "post/post_list.html"
    def get_queryset(self):
        return super().get_queryset().order_by("-created")
    # def get_queryset(self):
    #     return self.request.user.posts.all()
    login_url = "/user/login"

class PostListAllView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = "posts"
    template_name = "post/post_list_all.html"

    def get_queryset(self):
        search = self.request.GET.get("q")
        if search == "all": return super().get_queryset()
        if search == "news": return super().get_queryset().filter(type="1")
            
        if search == "event":
            return super().get_queryset().filter(type="2")
        if search == "rsch":
            return super().get_queryset().filter(type="3")
        if search == "ext":
            return super().get_queryset().filter(type="4")
        return super().get_queryset()
        
        # return self.request.user.posts.all()
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
        Log(log_code='post_create', log_message=f'[{self.request.user.username}] created post [{self.object.title}]').save()

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
    def post(self, request, *args, **kwargs):
        title = self.get_form()['title'].value()
        username = self.request.user.username
        if self.get_form().is_valid():
            Log(log_code='post_update', log_message=f'[{username}] updated post [{title}]').save()
        return super().post(request, *args, **kwargs)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = "/posts"
    template_name = "post/post_delete.html"
    login_url = "/user/login"
    def get(self, request, *args, **kwargs):
        if self.request.user.role == "5":
            return redirect('post.list')
        return super().get(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        target = Post.objects.get(id=self.kwargs["pk"])
        user = self.request.user.username
        Log(log_code='post_delete', log_message=f'[{user}] deleted the post [{target.title}]').save()
        return super().post(request, *args, **kwargs)
   

