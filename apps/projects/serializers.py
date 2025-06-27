from rest_framework import serializers

from apps.users.serializers import UserShortSerializer
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    members = UserShortSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "members", "created_at", "updated_at"]
        read_only_fields = ("id", "created_at", "updated_at")
