from django import forms

from tasks import models


class TaskForm(forms.ModelForm):
    """Task creation and editing form."""

    class Meta:
        model = models.Task
        fields = ("name", "description", "status", "executor", "labels")
