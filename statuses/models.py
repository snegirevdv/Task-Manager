from core.models import BaseModel
from django.utils.translation import gettext_lazy as _


class TaskStatus(BaseModel):
    """Task status model."""

    class Meta:
        verbose_name: str = _("status")
        verbose_name_plural: str = _("Statuses")
