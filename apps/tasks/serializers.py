from rest_framework import serializers

from apps.users.models import CustomUser
from apps.users.serializers import UserShortSerializer
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserShortSerializer(allow_null=True)
    is_archived = serializers.BooleanField(allow_null=False)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "assigned_to",
            "project",
            "is_archived",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id", "created_at", "updated_at")


class TaskRequestSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        allow_null=True,
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "assigned_to",
            "project",
            "is_archived",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id", "created_at", "updated_at")
