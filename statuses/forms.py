from django import forms

from statuses import models


class StatusForm(forms.ModelForm):
    class Meta:
        model = models.Status
        fields = ('name', )
