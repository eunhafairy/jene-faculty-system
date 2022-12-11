
from django.urls import path
from . import views
urlpatterns = [
    path("add-subject", views.FacultySubjectCreateView.as_view(), name="table.add.subject"),
    path("delete-subject/<int:pk>", views.FacultySubjectDeleteView.as_view(), name="table.delete.subject"),
]
