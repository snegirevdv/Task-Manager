from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from core import mixins
from statuses import forms, models


class StatusListView(mixins.LoginRequiredMixin, generic.ListView):
    """List of statuses view."""

    queryset = models.TaskStatus.objects.only("pk", "name", "created_at")
    template_name = "statuses/list.html"


class StatusCreateView(
    mixins.LoginRequiredMixin,
    SuccessMessageMixin,
    generic.CreateView,
):
    """Status creation view."""

    model = models.TaskStatus
    form_class = forms.StatusForm
    template_name = "statuses/create_update.html"
    success_url: str = reverse_lazy("statuses:list")
    success_message: str = _("The status has been successfully created.")


class StatusUpdateView(
    mixins.LoginRequiredMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    """Status editing view."""

    model = models.TaskStatus
    form_class = forms.StatusForm
    template_name = "statuses/create_update.html"
    success_url = reverse_lazy("statuses:list")
    success_message = _("The status has been successfully updated.")


class StatusDeleteView(
    mixins.ProtectedDeletionMixin,
    mixins.LoginRequiredMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    """Status deletion view."""

    model = models.TaskStatus
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses:list")
    success_message = _("The status has been successfully deleted.")
    deletion_error_message = _(
        "The status cannot be deleted because it is in use."
    )
