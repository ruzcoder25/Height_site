from django.contrib.auth.models import AbstractUser
from django.db import models

from common.models import BaseModel


class StatusChoices(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'

class RoleChoices(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    MODERATOR = 'moderator', 'Moderator'


class User(AbstractUser, BaseModel):
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
        blank=True,
    )
    role = models.CharField(
        max_length=50,
        choices=RoleChoices.choices,
        default=RoleChoices.MODERATOR,
        blank=True,
    )

    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'