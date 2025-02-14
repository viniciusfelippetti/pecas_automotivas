from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, Group, PermissionsMixin
import uuid


class Users(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, blank=True
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True, blank=True)
    is_staff = models.BooleanField(default=False, blank=True)
    groups = models.ManyToManyField(Group, related_name="users", blank=True) # Campo Many-to-Many
    objects = UserManager()

    USERNAME_FIELD = "username"


    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"