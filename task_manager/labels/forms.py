from django import forms

from task_manager.core import consts
from task_manager.labels import models


class LabelForm(forms.ModelForm):
    """Label creation and editing form."""

    class Meta:
        model = models.TaskLabel
        fields = consts.FieldList.BASE_FORM
