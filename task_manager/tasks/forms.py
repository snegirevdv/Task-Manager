from django import forms

from task_manager.core import consts
from task_manager.tasks import models


class TaskForm(forms.ModelForm):
    """Task creation and editing form."""

    class Meta:
        model = models.Task
        fields = consts.FieldList.TASK_FORM
