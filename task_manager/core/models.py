from django.db import models

from task_manager.core import consts


class BaseModel(models.Model):
    """Basic entity model. Implements fields: name, created_at."""

    name = models.CharField(
        verbose_name=consts.VerboseName.NAME.value,
        max_length=consts.NAME_MAX_LENGTH,
    )
    created_at = models.DateTimeField(
        verbose_name=consts.VerboseName.CREATED_AT.value,
        auto_now_add=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        abstract = True
