from django.urls import path
from apps.tasks import views

urlpatterns = [
    path("tasks/", views.TaskList.as_view(), name="task-list"),
    path("tasks/<pk>/", views.TaskDetail.as_view(), name="task-detail"),
]
