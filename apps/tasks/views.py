from django.http import HttpResponse
from rest_framework.views import APIView, Http404, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import datetime
from django.shortcuts import get_object_or_404

from apps.projects.models import Project
from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer

import logging

logger = logging.getLogger(__name__)


class TaskList(APIView):
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        project: Project = get_object_or_404(Project, pk=request.data.get("project"))

        if not project.members.filter(id=request.user.id).exists():
            return Response(
                {"detail": "You are not a member of this project."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetail(APIView):
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while fetching task with ID '{pk}': {e}",
                exc_info=True,
            )
            raise Http404

    def get(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    pass
