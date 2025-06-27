import uuid
from django.db import models

# Create your models here.


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    members = models.ManyToManyField(
        "users.CustomUser",
        related_name="projects",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
