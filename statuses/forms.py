from django import forms

from core import consts
from statuses import models


class StatusForm(forms.ModelForm):
    """Status creation and editing form."""

    class Meta:
        model = models.TaskStatus
        fields = consts.FieldList.BASE_FORM
