from django.db import models


class Label(models.Model):
    name = models.CharField(
        verbose_name="Имя",
        max_length=100,
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )

    def __str__(self):
        return self.name
