
from django.urls import path
from . import views

urlpatterns = [
    path('', views.DepartmentListView.as_view(), name="department.list"),
    path('create', views.DepartmentCreateView.as_view(), name="department.create"),
    path('update/<int:pk>', views.DepartmenthUpdateView.as_view(), name="department.update"),
    path('delete/<int:pk>', views.DepartmentDeleteView.as_view(), name="department.delete"),
    path('me', views.MyDepartmentListView.as_view(), name="department.me"),
    # path('logout', views.LogoutInterfaceView.as_view(), name="logout"),

    # path('register/', views.SignUpView.as_view(), name="register"),
]
