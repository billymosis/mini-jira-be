from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView, Http404, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Project
from .serializers import (
    ProjectRequestSerializer,
    ProjectSerializer,
    ProjectTasksSerializer,
)
from .permissions import IsAdminOrReadOnly, IsProjectOwnerOrReadOnly
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

import logging

logger = logging.getLogger(__name__)

# Create your views here.


class ProjectList(ListAPIView, CreateAPIView):
    """
    List all projects.
    """

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    pagination_class = PageNumberPagination

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter projects by name (case-insensitive contains)",
            ),
            OpenApiParameter(
                name="member",
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.QUERY,
                description="Filter projects by member ID",
            ),
            OpenApiParameter(
                name="status",
                type={"type": "array", "items": {"type": "string"}},
                location=OpenApiParameter.QUERY,
                description="Filter projects by task status",
            ),
            OpenApiParameter(
                name="task",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter projects by task name (case-insensitive contains)",
            ),
            OpenApiParameter(
                name="assignee",
                type={"type": "array", "items": {"type": "string"}},
                location=OpenApiParameter.QUERY,
                description="Filter projects by task assignee IDs",
            ),
            OpenApiParameter(
                name="ordering",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Which field to use when ordering the results.",
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        request = self.request
        if request.user.is_admin:
            queryset = Project.objects.all()
        else:
            queryset = Project.objects.filter(
                Q(owner=request.user) | Q(members=request.user)
            )

        # Filter by name
        project_name = request.query_params.get("name", None)
        if project_name:
            queryset = queryset.filter(name__icontains=project_name)

        # Filter by member
        member_id = request.query_params.get("member", None)
        if member_id:
            queryset = queryset.filter(members__id=member_id)

        # Filter by task status
        statuses = request.query_params.getlist("status", None)
        if statuses:
            queryset = queryset.filter(tasks__status__in=statuses).distinct()

        # Filter by task name
        task_name = request.query_params.getlist("task", None)
        if task_name:
            queryset = queryset.filter(tasks__name__icontains=task_name).distinct()

        # Filter by task assignee (supports multiple assignees)
        task_assignee_ids = request.query_params.getlist(
            "assignee"
        )  # Use getlist() for multiple values
        if task_assignee_ids:
            queryset = queryset.filter(
                tasks__assigned_to__id__in=task_assignee_ids
            ).distinct()

        # Ordering
        ordering = request.query_params.get("ordering", "-created_at")
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset

    @extend_schema(
        request=ProjectRequestSerializer,
        responses=ProjectSerializer,
    )
    def post(self, request):
        serializer = ProjectRequestSerializer(data=request.data)
        if serializer.is_valid():
            project: Project = serializer.save(owner=request.user)
            project.members.add(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetail(APIView):
    """
    Retrieve, update or delete a project instance.
    """

    serializer_class = ProjectTasksSerializer
    permission_classes = [IsAuthenticated, IsProjectOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while fetching project with ID '{pk}': {e}",
                exc_info=True,
            )
            raise Http404

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectTasksSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectRequestSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(ProjectSerializer(project).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
