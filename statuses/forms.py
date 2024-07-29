from django import forms

from statuses import models


class StatusForm(forms.ModelForm):
    """Status creation and editing form."""

    class Meta:
        model = models.TaskStatus
        fields = ("name",)
