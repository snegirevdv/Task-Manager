from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic

from core import mixins
from statuses import forms, models


class StatusListView(mixins.LoginRequiredMixin, generic.ListView):
    model = models.Status
    template_name = "statuses/list.html"


class StatusCreateView(
    mixins.LoginRequiredMixin,
    SuccessMessageMixin,
    generic.CreateView,
):
    model = models.Status
    form_class = forms.StatusForm
    template_name = "statuses/detail.html"
    success_url = reverse_lazy("statuses:list")
    success_message = "Статус успешно создан."


class StatusUpdateView(
    mixins.LoginRequiredMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    model = models.Status
    form_class = forms.StatusForm
    template_name = "statuses/detail.html"
    success_url = reverse_lazy("statuses:list")
    success_message = "Статус успешно изменён."


class StatusDeleteView(
    mixins.ProtectedDeletionMixin,
    mixins.LoginRequiredMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    model = models.Status
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses:list")
    success_message = "Статус успешно удалён."
    deletion_error_message = "Невозможно удалить статус, потому что он используется."
