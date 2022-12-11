
from django.urls import path
from . import views
urlpatterns = [
    path("", views.SubjectListView.as_view(), name="subject.list"),
]
