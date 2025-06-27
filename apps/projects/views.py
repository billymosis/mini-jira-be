from rest_framework.views import APIView, Http404, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Project
from .serializers import ProjectSerializer
from .permissions import IsAdminOrReadOnly, IsProjectOwnerOrReadOnly
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

import logging

logger = logging.getLogger(__name__)

# Create your views here.


class ProjectList(APIView):
    """
    List all projects.
    """

    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    pagination_class = PageNumberPagination

    def get(self, request):
        projects = Project.objects.filter(
            Q(owner=request.user) | Q(members=request.user)
        )

        # Filter by name
        project_name = request.query_params.get("name", None)
        if project_name:
            projects = projects.filter(name__icontains=project_name)

        # Filter by member
        member_id = request.query_params.get("member", None)
        if member_id:
            projects = projects.filter(members__id=member_id)

        # Ordering
        ordering = request.query_params.get("ordering", "-created_at")
        if ordering:
            projects = projects.order_by(ordering)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(projects, request)
        serializer = ProjectSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetail(APIView):
    """
    Retrieve, update or delete a project instance.
    """

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
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
