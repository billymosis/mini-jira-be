import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
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
