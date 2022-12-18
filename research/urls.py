from django.urls import path
from . import views
urlpatterns = [
    path("", views.ResearchListView.as_view(), name="research.list"),
    path("create/", views.ResearchCreateView.as_view(), name="research.create"),
    path("edit/<int:pk>", views.ResearchUpdateView.as_view(), name="research.update"),
    path("delete/<int:pk>", views.ResearchDeleteView.as_view(), name="research.delete"),

]
