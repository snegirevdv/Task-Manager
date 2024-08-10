from django import forms

from task_manager.core import consts
from task_manager.statuses import models


class StatusForm(forms.ModelForm):
    """Status creation and editing form."""

    class Meta:
        model = models.TaskStatus
        fields = consts.FieldList.BASE_FORM
