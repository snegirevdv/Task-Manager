from django import forms

from core import consts
from labels import models


class LabelForm(forms.ModelForm):
    """Label creation and editing form."""

    class Meta:
        model = models.TaskLabel
        fields = consts.FieldList.BASE_FORM
