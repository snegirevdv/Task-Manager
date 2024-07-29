from django import forms

from labels import models


class LabelForm(forms.ModelForm):
    """Label creation and editing form."""

    class Meta:
        model = models.TaskLabel
        fields = ("name",)
