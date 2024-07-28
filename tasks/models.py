from django.db import models

from statuses.models import Status
from users.models import User
from labels.models import Label


class Task(models.Model):
    name = models.CharField(
        verbose_name="Имя",
        max_length=100,
    )
    description = models.TextField(
        verbose_name="Описание",
        null=True,
        blank=True,
    )
    status = models.ForeignKey(
        verbose_name="Статус",
        related_name="tasks",
        to=Status,
        on_delete=models.PROTECT,
    )
    author = models.ForeignKey(
        verbose_name="Автор",
        related_name="created_tasks",
        to=User,
        on_delete=models.PROTECT,
    )
    executor = models.ForeignKey(
        verbose_name="Исполнитель",
        related_name="executing_tasks",
        to=User,
        on_delete=models.PROTECT,
    )
    labels = models.ManyToManyField(
        verbose_name="Метки",
        related_name="tasks",
        to=Label,
        through="TaskLabel",
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )

    def __str__(self):
        return self.name


class TaskLabel(models.Model):
    label = models.ForeignKey(to=Label, on_delete=models.PROTECT)
    task = models.ForeignKey(to=Task, on_delete=models.CASCADE)
