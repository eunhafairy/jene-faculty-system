
from django.urls import path
from . import views
urlpatterns = [
    path("add-subject", views.FacultySubjectCreateView.as_view(), name="table.add.subject"),
    path("delete-subject/<int:pk>", views.FacultySubjectDeleteView.as_view(), name="table.delete.subject"),
    path("already-exists", views.FacultySubjectAlreadyExists.as_view(), name="table.error.exist"),
    path("add-ext", views.FacultyExtensionCreateView.as_view(), name="table.add.ext"),
    path("delete-ext/<int:pk>", views.FacultyExtensionDeleteView.as_view(), name="table.delete.ext"),
  

]
