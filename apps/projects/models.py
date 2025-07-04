import uuid
from django.db import models
from typing import TYPE_CHECKING

# Create your models here.

from apps.users.models import CustomUser

if TYPE_CHECKING:
    from apps.tasks.models import Task


class Project(models.Model):
    if TYPE_CHECKING:
        tasks: models.Manager[Task]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="owned_projects"
    )
    members = models.ManyToManyField(
        CustomUser,
        related_name="member_of_projects",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
