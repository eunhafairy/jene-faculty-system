
from django.urls import path
from . import views
urlpatterns = [
    path("", views.SubjectListView.as_view(), name="subject.list"),
    path("create/", views.SubjectCreateView.as_view(), name="subject.create"),
    path("edit/<int:pk>", views.SubjectUpdateView.as_view(), name="subject.update"),
    path("delete/<int:pk>", views.SubjectDeleteView.as_view(), name="subject.delete"),

]
