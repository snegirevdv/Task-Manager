from django.utils.translation import gettext_lazy as _

from core.models import BaseModel


class TaskLabel(BaseModel):
    """Task label model."""

    class Meta:
        verbose_name: str = _("label")
        verbose_name_plural: str = _("Labels")
