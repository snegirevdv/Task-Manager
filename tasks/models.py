from django.db import models

from core import consts
from core.models import BaseModel
from statuses.models import TaskStatus
from labels.models import TaskLabel
from users.models import User


class Task(BaseModel):
    """Task model."""

    description = models.TextField(
        verbose_name=consts.VerboseName.DESCRIPTION.value,
        null=True,
        blank=True,
    )
    status = models.ForeignKey(
        verbose_name=consts.VerboseName.STATUS.value,
        related_name="tasks",
        to=TaskStatus,
        on_delete=models.PROTECT,
    )
    author = models.ForeignKey(
        verbose_name=consts.VerboseName.AUTHOR.value,
        related_name="created_tasks",
        to=User,
        on_delete=models.PROTECT,
    )
    executor = models.ForeignKey(
        verbose_name=consts.VerboseName.EXECUTOR.value,
        related_name="executing_tasks",
        to=User,
        on_delete=models.PROTECT,
    )
    labels = models.ManyToManyField(
        verbose_name=consts.VerboseName.LABELS.value,
        related_name="tasks",
        to=TaskLabel,
        through="TaskLabelRelation",
        blank=True,
    )

    class Meta:
        verbose_name: str = consts.VerboseName.TASK.value.lower()
        verbose_name_plural: str = consts.VerboseName.TASKS.value


class TaskLabelRelation(models.Model):
    """Auxiliary model, implements M2M relations for task and label."""

    label = models.ForeignKey(to=TaskLabel, on_delete=models.PROTECT)
    task = models.ForeignKey(to=Task, on_delete=models.CASCADE)
