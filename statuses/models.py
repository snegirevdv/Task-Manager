from django.db import models


class Status(models.Model):
    name = models.CharField(
        verbose_name="Имя",
        max_length=100,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    def __str__(self):
        return self.name
