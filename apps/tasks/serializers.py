from rest_framework import serializers

from apps.users.serializers import UserShortSerializer
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserShortSerializer(read_only=True)

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
