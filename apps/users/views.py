from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import CustomUser
from .serializers import (
    AvatarUploadSerializer,
    LoginResponseSerializer,
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    UserShortSerializer,
)
from drf_spectacular.utils import OpenApiParameter, extend_schema


# Create your views here.
class Register(APIView):
    permission_classes = [permissions.AllowAny]
    request_serializer_class = RegisterSerializer
    response_serializer_class = LoginResponseSerializer

    @extend_schema(
        request=RegisterSerializer,
        responses=LoginResponseSerializer,
    )
    def post(self, request):
        serializer = self.request_serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            response_serializer = self.response_serializer_class(
                instance={
                    "user": user,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }
            )
            return Response(response_serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    permission_classes = [permissions.AllowAny]
    request_serializer_class = LoginSerializer
    response_serializer_class = LoginResponseSerializer

    @extend_schema(
        request=LoginSerializer,
        responses=LoginResponseSerializer,
    )
    def post(self, request):
        serializer = self.request_serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            response_serializer = self.response_serializer_class(
                instance={
                    "user": user,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }
            )
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class UserList(ListAPIView):
    """
    List all projects.
    """

    serializer_class = UserShortSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="search",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter users (case-insensitive contains)",
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        request = self.request
        queryset = CustomUser.objects.all()
        # Filter by search
        search_query = request.query_params.get("search", None)
        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query)
                | Q(email__icontains=search_query)
                | Q(first_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
            )

        # Ordering
        ordering = request.query_params.get("ordering", "-created_at")
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset


class Me(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class AvatarUploadView(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AvatarUploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    @extend_schema(
        request=AvatarUploadSerializer,
        responses={
            200: AvatarUploadSerializer,
            400: OpenApiTypes.OBJECT,
        },
        # This tells Spectacular it's a file upload
        operation={
            "request": {
                "content": {"multipart/form-data": {"schema": AvatarUploadSerializer}}
            }
        },
    )
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if user.avatar:
            user.avatar.delete()

        return super().update(request, *args, **kwargs)
