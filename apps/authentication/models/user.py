import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.authentication.managers.users import UserRelatedManager


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    secret_key = models.UUIDField(default=uuid.uuid4, editable=True, unique=True, blank=True, null=True)
    email = models.EmailField(blank=True, unique=True)

    objects = UserRelatedManager()

    def is_user(self):
        return self.groups.filter(name="User").exists()

    def is_admin(self):
        return self.groups.filter(name="admin").exists()

    def __repr__(self):
        return f"<User: {self.first_name} {self.last_name} - {self.email}>"
