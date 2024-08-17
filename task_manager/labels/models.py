from django.db import models

from task_manager.core import consts
from task_manager.core.models import BaseModel


class TaskLabel(BaseModel):
    """Task label model."""

    name = models.CharField(
        verbose_name=consts.VerboseName.NAME.value,
        max_length=consts.NAME_MAX_LENGTH,
        unique=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = consts.VerboseName.LABEL.value.lower()
        verbose_name_plural = consts.VerboseName.LABELS.value
