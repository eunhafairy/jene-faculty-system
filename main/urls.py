
from django.urls import path
from main import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('me', views.ProfileView.as_view(), name="profile"),

]
