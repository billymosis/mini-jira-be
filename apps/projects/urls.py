from django.urls import path
from apps.projects import views

urlpatterns = [
    path("projects/", views.ProjectList.as_view(), name="project-list"),
    path("projects/<pk>/", views.ProjectDetail.as_view(), name="project-detail"),
]
