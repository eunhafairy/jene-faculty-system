
from django.urls import path
from . import views
urlpatterns = [
    path("add-subject", views.FacultySubjectCreateView.as_view(), name="table.add.subject"),
    path("delete-subject/<int:pk>", views.FacultySubjectDeleteView.as_view(), name="table.delete.subject"),
    path("already-exists", views.FacultySubjectAlreadyExists.as_view(), name="table.error.exist"),
    path("add-ext", views.FacultyExtensionCreateView.as_view(), name="table.add.ext"),
    path("delete-ext/<int:pk>", views.FacultyExtensionDeleteView.as_view(), name="table.delete.ext"),
    path("reports/users", views.UserReportsListView.as_view(), name="table.reports.users"),
    path("reports/users/generate", views.generateUserDocument, name="table.generate.users"),
    path("reports/subjects", views.SubjectsReportsListView.as_view(), name="table.reports.subjects"),
    path("reports/subjects/generate", views.generateSubjectDocument, name="table.generate.subjects"),
    path("reports/departments", views.DepartmentReportsListView.as_view(), name="table.reports.departments"),
    path("reports/departments/generate", views.generatDepartmentDocument, name="table.generate.departments"),
    path("reports/research", views.ResearchReportsListView.as_view(), name="table.reports.research"),
    path("reports/research/generate", views.generateResearchDocument, name="table.generate.research"),
   path("reports/extensions", views.ExtensionReportsListView.as_view(), name="table.reports.extensions"),
    path("reports/extensions/generate", views.generateExtensionDocument, name="table.generate.extensions"),
   path("reports/logs", views.LogsReportsListView.as_view(), name="table.reports.logs"),
    path("reports/logs/generate", views.generateLogsDocument, name="table.generate.logs"),
  

]
