
from django.urls import path
from accounts import views

urlpatterns = [
    path('login', views.LoginInterfaceView.as_view(), name="login"),
    path('logout', views.LogoutInterfaceView.as_view(), name="logout"),
    path('register/', views.SignUpView.as_view(), name="register"),
    path('my-subjects/', views.MySubjectsListView.as_view(), name="my-subjects"),

]
