from django.db import models
from django.utils import timezone


class BaseQuerySet(models.QuerySet):

    def active(self):
        return self.filter(is_deleted=False)

    def delete(self):
        return self.update(is_deleted=True, deleted_at=timezone.now())


class BaseManager(models.Manager):
    def get_queryset(self):
        return BaseQuerySet(self.model, using=self._db).filter(is_deleted=False)


class BaseModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    objects = BaseManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True
        ordering = ['-created_at']
