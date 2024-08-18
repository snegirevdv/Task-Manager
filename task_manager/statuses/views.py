from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic

from task_manager.core import consts
from task_manager.core.mixins import (
    LoginIsRequiredMixin,
    ProtectedDeletionMixin,
)
from task_manager.statuses import forms, models


class StatusListView(LoginIsRequiredMixin, generic.ListView):
    """List of statuses view."""

    queryset = models.TaskStatus.objects.only(*consts.FieldList.BASE_QUERYSET)
    template_name: str = consts.Template.STATUS_LIST.value


class StatusCreateView(
    LoginIsRequiredMixin,
    SuccessMessageMixin,
    generic.CreateView,
):
    """Status creation view."""

    model = models.TaskStatus
    form_class = forms.StatusForm
    template_name: str = consts.Template.STATUS_CREATE_UPDATE.value
    success_message: str = consts.Message.SUCCESS_STATUS_CREATION.value
    success_url: str = reverse_lazy("statuses:list")


class StatusUpdateView(
    LoginIsRequiredMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    """Status editing view."""

    model = models.TaskStatus
    form_class = forms.StatusForm
    template_name: str = consts.Template.STATUS_CREATE_UPDATE.value
    success_message: str = consts.Message.SUCCESS_STATUS_UPDATE.value
    success_url: str = reverse_lazy("statuses:list")


class StatusDeleteView(
    ProtectedDeletionMixin,
    LoginIsRequiredMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    """Status deletion view."""

    model = models.TaskStatus
    template_name: str = consts.Template.STATUS_DELETE.value
    success_message: str = consts.Message.SUCCESS_STATUS_DELETION.value
    deletion_error_message: str = consts.Message.FAILURE_STATUS_DELETION.value
    success_url: str = reverse_lazy("statuses:list")
