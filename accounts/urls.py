
from django.urls import path
from accounts import views

urlpatterns = [
    path('login', views.LoginInterfaceView.as_view(), name="login"),
    path('logout', views.LogoutInterfaceView.as_view(), name="logout"),
    path('register/', views.SignUpView.as_view(), name="register"),
    path('update/<int:pk>', views.UserUpdateView.as_view(), name="user.update"),
    path('delete/<int:pk>', views.UserDeleteView.as_view(), name="user.delete"),
    path('change-password/', views.change_password, name="user.password"),
    path('my-subjects/', views.MySubjectsListView.as_view(), name="my-subjects"),
]
