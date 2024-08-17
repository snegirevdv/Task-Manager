from django.db import models

from task_manager.core import consts


class BaseModel(models.Model):
    """Basic entity model. Implements fields: created_at."""
    created_at = models.DateTimeField(
        verbose_name=consts.VerboseName.CREATED_AT.value,
        auto_now_add=True,
    )

    class Meta:
        abstract = True
