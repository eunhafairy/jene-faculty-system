from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
# Create your views here.
class LoginInterfaceView(LoginView):
    template_name = "accounts/login.html"
    success_url="/posts"
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('post.list')
        return super().get(request, *args, **kwargs)

class LogoutInterfaceView(LogoutView):
    template_name = "accounts/logout.html"

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/register.html"
    success_url = "/posts"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('post.list')
        return super().get(request, *args, **kwargs)