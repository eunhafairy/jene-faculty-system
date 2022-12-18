
from django.urls import path
from . import views

urlpatterns = [
    path('', views.DepartmentListView.as_view(), name="department.list"),
    path('create', views.DepartmentCreateView.as_view(), name="department.create"),
    path('me', views.MyDepartmentListView.as_view(), name="department.me"),
    # path('logout', views.LogoutInterfaceView.as_view(), name="logout"),

    # path('register/', views.SignUpView.as_view(), name="register"),
]
