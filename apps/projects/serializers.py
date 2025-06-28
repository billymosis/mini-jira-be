from rest_framework import serializers

from apps.tasks.serializers import TaskSerializer
from apps.users.models import CustomUser
from apps.users.serializers import UserShortSerializer
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    members = UserShortSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "members", "created_at", "updated_at"]
        read_only_fields = ("id", "created_at", "updated_at")


class ProjectRequestSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CustomUser.objects.all(), required=False
    )

    class Meta:
        model = Project
        fields = ["id", "name", "description", "members", "created_at", "updated_at"]


class ProjectTasksSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    members = UserShortSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "members",
            "tasks",
            "created_at",
            "updated_at",
        ]
