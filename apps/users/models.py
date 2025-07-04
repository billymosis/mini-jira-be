from typing import TYPE_CHECKING
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


if TYPE_CHECKING:
    from apps.projects.models import Project
    from django.db.models import Manager
    from apps.tasks.models import Task


# Create your models here.
class CustomUser(AbstractUser):
    if TYPE_CHECKING:
        owned_projects: Manager[Project]
        member_of_projects: Manager[Project]
        assigned_tasks: Manager[Task]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    last_seen = models.DateTimeField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_admin(self):
        return self.groups.filter(name="Admins").exists()

    @property
    def is_member(self):
        return self.groups.filter(name="Members").exists()

    @property
    def full_name(self):
        return self.get_full_name()

    class Meta(AbstractUser.Meta):
        verbose_name = "User"
        verbose_name_plural = "Users"
