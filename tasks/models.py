from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel
from statuses.models import TaskStatus
from labels.models import TaskLabel
from users.models import User


class Task(BaseModel):
    """Task model."""

    description = models.TextField(
        verbose_name=_("Description"),
        null=True,
        blank=True,
    )
    status = models.ForeignKey(
        verbose_name=_("Status"),
        related_name="tasks",
        to=TaskStatus,
        on_delete=models.PROTECT,
    )
    author = models.ForeignKey(
        verbose_name=_("Author"),
        related_name="created_tasks",
        to=User,
        on_delete=models.PROTECT,
    )
    executor = models.ForeignKey(
        verbose_name=_("Executor"),
        related_name="executing_tasks",
        to=User,
        on_delete=models.PROTECT,
    )
    labels = models.ManyToManyField(
        verbose_name=_("Labels"),
        related_name="tasks",
        to=TaskLabel,
        through="TaskLabelRelation",
    )


class TaskLabelRelation(models.Model):
    """Auxiliary model, implements M2M relations for task and label."""

    label = models.ForeignKey(to=TaskLabel, on_delete=models.PROTECT)
    task = models.ForeignKey(to=Task, on_delete=models.CASCADE)
