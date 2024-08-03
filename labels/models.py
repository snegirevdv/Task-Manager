from core import consts
from core.models import BaseModel


class TaskLabel(BaseModel):
    """Task label model."""

    class Meta:
        verbose_name = consts.VerboseName.LABEL.value.lower()
        verbose_name_plural = consts.VerboseName.LABELS.value
