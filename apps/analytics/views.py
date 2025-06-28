from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Q
from django.contrib.auth import get_user_model

from apps.projects.models import Project
from apps.tasks.models import Task, TaskStatus
from .serializers import (
    TaskStatusAnalyticsSerializer,
    ProjectTaskAnalyticsSerializer,
    UserTaskAnalyticsSerializer,
)

CustomUser = get_user_model()


class TaskStatusAnalyticsView(APIView):
    serializer_class = TaskStatusAnalyticsSerializer()

    def get(self, request):
        # Get counts for each task status
        status_counts = (
            Task.objects.filter(is_archived=False)
            .values("status")
            .annotate(count=Count("status"))
        )

        # Convert to a more usable format
        counts = {item["status"]: item["count"] for item in status_counts}

        data = {
            "todo": counts.get(TaskStatus.TODO, 0),
            "in_progress": counts.get(TaskStatus.IN_PROGRESS, 0),
            "done": counts.get(TaskStatus.DONE, 0),
            "total": sum(counts.values()),
        }

        serializer = TaskStatusAnalyticsSerializer(data)
        return Response(serializer.data)


class ProjectTaskAnalyticsView(APIView):
    serializer_class = ProjectTaskAnalyticsSerializer(many=True)

    def get(self, request):
        projects = Project.objects.all()
        analytics_data = []

        for project in projects:
            total_tasks = project.tasks.filter(is_archived=False).count()
            completed_tasks = project.tasks.filter(
                status=TaskStatus.DONE, is_archived=False
            ).count()

            completion_percentage = 0
            if total_tasks > 0:
                completion_percentage = (completed_tasks / total_tasks) * 100

            analytics_data.append(
                {
                    "project_id": project.id,
                    "project_name": project.name,
                    "total_tasks": total_tasks,
                    "completed_tasks": completed_tasks,
                    "completion_percentage": round(completion_percentage, 2),
                }
            )

        serializer = ProjectTaskAnalyticsSerializer(analytics_data, many=True)
        return Response(serializer.data)


class UserTaskAnalyticsView(APIView):
    serializer_class = UserTaskAnalyticsSerializer(many=True)

    def get(self, request):
        users = CustomUser.objects.filter(
            Q(assigned_tasks__isnull=False) | Q(projects__isnull=False)
        ).distinct()

        analytics_data = []

        for user in users:
            total_tasks = Task.objects.filter(
                assigned_to=user, is_archived=False
            ).count()
            completed_tasks = Task.objects.filter(
                assigned_to=user, status=TaskStatus.DONE, is_archived=False
            ).count()
            in_progress_tasks = Task.objects.filter(
                assigned_to=user, status=TaskStatus.IN_PROGRESS, is_archived=False
            ).count()

            completion_rate = 0
            if total_tasks > 0:
                completion_rate = (completed_tasks / total_tasks) * 100

            analytics_data.append(
                {
                    "user_id": user.id,
                    "username": user.username,
                    "total_tasks_assigned": total_tasks,
                    "completed_tasks": completed_tasks,
                    "in_progress_tasks": in_progress_tasks,
                    "completion_rate": round(completion_rate, 2),
                }
            )

        serializer = UserTaskAnalyticsSerializer(analytics_data, many=True)
        return Response(serializer.data)
