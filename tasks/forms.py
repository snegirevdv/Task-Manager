from django import forms

from tasks import models


class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ("name", "description", "status", "executor", "labels")
