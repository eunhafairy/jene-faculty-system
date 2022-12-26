
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ExtensionListView.as_view(), name="extension.list"),
    path('create', views.ExtensionsCreateView.as_view(), name="extension.create"),
    path('update/<int:pk>', views.ExtensionUpdateView.as_view(), name="extension.update"),
    path('delete/<int:pk>', views.ExtensionDeleteView.as_view(), name="extension.delete"),

    # path('me', views.Myext4ensionListView.as_view(), name="department.me"),
    # path('logout', views.LogoutInterfaceView.as_view(), name="logout"),

    # path('register/', views.SignUpView.as_view(), name="register"),
]
