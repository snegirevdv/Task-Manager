from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic

from task_manager.core import consts, mixins
from task_manager.labels import forms, models


class LabelListView(mixins.LoginIsRequiredMixin, generic.ListView):
    """List of labels view."""

    queryset = models.TaskLabel.objects.only(*consts.FieldList.BASE_QUERYSET)
    template_name: str = consts.Template.LABEL_LIST.value


class LabelCreateView(
    mixins.LoginIsRequiredMixin,
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
    mixins.LoginIsRequiredMixin,
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
    mixins.ProtectedDeletionMixin,
    mixins.LoginIsRequiredMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    """Label deletion view."""

    model = models.TaskLabel
    success_url: str = reverse_lazy("labels:list")
    template_name: str = consts.Template.LABEL_DELETE.value
    success_message: str = consts.Message.SUCCESS_LABEL_DELETION.value
    deletion_error_message: str = consts.Message.FAILURE_LABEL_DELETION.value
