
from django.urls import path
from . import views
urlpatterns = [
    path("", views.PostListView.as_view(), name="post.list"),
    path("<int:pk>", views.PostDetailView.as_view(), name="post.detail"),
    path("create", views.PostCreateView.as_view(), name="post.create"),
    path("edit/<int:pk>", views.PostUpdateView.as_view(), name="post.update"),
    path("delete/<int:pk>", views.PostDeleteView.as_view(), name="post.delete"),

]
