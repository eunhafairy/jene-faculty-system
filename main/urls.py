
from django.urls import path
from main import views
from posts.views import PostListView

urlpatterns = [
    path('home', PostListView.as_view(), name="home"),
    path('me', views.ProfileView.as_view(), name="profile"),
    path('', views.HomeView.as_view(), name="main"),

]
