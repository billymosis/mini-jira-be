from django.urls import path
from apps.analytics.views import (
    TaskStatusAnalyticsView,
    ProjectTaskAnalyticsView,
    UserTaskAnalyticsView,
)

urlpatterns = [
    path(
        "analytics/task-status/",
        TaskStatusAnalyticsView.as_view(),
        name="task-status-analytics",
    ),
    path(
        "analytics/project-tasks/",
        ProjectTaskAnalyticsView.as_view(),
        name="project-task-analytics",
    ),
    path(
        "analytics/user-tasks/",
        UserTaskAnalyticsView.as_view(),
        name="user-task-analytics",
    ),
]
