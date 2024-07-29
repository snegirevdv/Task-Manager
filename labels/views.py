from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from core.mixins import LoginRequiredMixin, ProtectedDeletionMixin
from labels import forms, models


class LabelListView(LoginRequiredMixin, generic.ListView):
    """List of labels view."""

    model = models.TaskLabel
    template_name = "labels/list.html"


class LabelCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    generic.CreateView,
):
    """Label creation view."""

    model = models.TaskLabel
    form_class = forms.LabelForm
    template_name = "labels/create_update.html"
    success_url: str = reverse_lazy("labels:list")
    success_message: str = _("The label has been successfully created.")


class LabelUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    """Label editing view."""

    model = models.TaskLabel
    form_class = forms.LabelForm
    template_name = "labels/create_update.html"
    success_url: str = reverse_lazy("labels:list")
    success_message: str = _("The label has been successfully updated.")


class LabelDeleteView(
    ProtectedDeletionMixin,
    LoginRequiredMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    """Label deletion view."""

    model = models.TaskLabel
    template_name = "labels/delete.html"
    success_url: str = reverse_lazy("labels:list")
    success_message: str = _("The label has been successfully deleted.")
    deletion_error_message: str = (
        _("The label cannot be deleted because it is in use.")
    )
