from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic

from core import consts
from core.mixins import LoginRequiredMixin, ProtectedDeletionMixin
from labels import forms, models


class LabelListView(LoginRequiredMixin, generic.ListView):
    """List of labels view."""

    queryset = models.TaskLabel.objects.only(*consts.FieldList.BASE_QUERYSET)
    template_name: str = consts.Template.LABEL_LIST.value


class LabelCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    generic.CreateView,
):
    """Label creation view."""

    model = models.TaskLabel
    form_class = forms.LabelForm
    success_url: str = reverse_lazy("labels:list")
    template_name: str = consts.Template.LABEL_CREATE_UPDATE.value
    success_message: str = consts.Message.SUCCESS_LABEL_CREATION.value


class LabelUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    """Label editing view."""

    model = models.TaskLabel
    form_class = forms.LabelForm
    success_url: str = reverse_lazy("labels:list")
    template_name: str = consts.Template.LABEL_CREATE_UPDATE.value
    success_message: str = consts.Message.SUCCESS_LABEL_UPDATE.value


class LabelDeleteView(
    ProtectedDeletionMixin,
    LoginRequiredMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    """Label deletion view."""

    model = models.TaskLabel
    success_url: str = reverse_lazy("labels:list")
    template_name: str = consts.Template.LABEL_DELETE.value
    success_message: str = consts.Message.SUCCESS_LABEL_DELETION.value
    deletion_error_message: str = consts.Message.FAILURE_LABEL_DELETION.value
