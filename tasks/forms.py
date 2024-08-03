from django import forms

from core import consts
from tasks import models


class TaskForm(forms.ModelForm):
    """Task creation and editing form."""

    class Meta:
        model = models.Task
        fields = consts.FieldList.TASK_FORM
