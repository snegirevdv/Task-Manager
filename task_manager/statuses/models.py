from task_manager.core import consts
from task_manager.core.models import BaseModel


class TaskStatus(BaseModel):
    """Task status model."""

    class Meta:
        verbose_name = consts.VerboseName.STATUS.value.lower()
        verbose_name_plural = consts.VerboseName.STATUSES.value
