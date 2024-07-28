from django import forms

from labels import models


class LabelForm(forms.ModelForm):
    class Meta:
        model = models.Label
        fields = ("name",)
