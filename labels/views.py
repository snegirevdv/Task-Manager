from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic

from core import mixins
from labels import forms, models


class LabelListView(mixins.LoginRequiredMixin, generic.ListView):
    model = models.Label
    template_name = "labels/list.html"


class LabelCreateView(
    mixins.LoginRequiredMixin,
    SuccessMessageMixin,
    generic.CreateView,
):
    model = models.Label
    form_class = forms.LabelForm
    template_name = "labels/detail.html"
    success_url = reverse_lazy("labels:list")
    success_message = "Метка успешно создана."


class LabelUpdateView(
    mixins.LoginRequiredMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    model = models.Label
    form_class = forms.LabelForm
    template_name = "labels/detail.html"
    success_url = reverse_lazy("labels:list")
    success_message = "Метка успешно изменена."


class LabelDeleteView(
    mixins.ProtectedDeletionMixin,
    mixins.LoginRequiredMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    model = models.Label
    template_name = "labels/delete.html"
    success_url = reverse_lazy("labels:list")
    success_message = "Метка успешно удалена."
    deletion_error_message = 'Невозможно удалить метку, потому что она используется.'
