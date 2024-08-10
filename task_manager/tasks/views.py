from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django_filters.views import FilterView

from task_manager.core import consts
from task_manager.core.mixins import LoginRequiredMixin
from task_manager.tasks import forms, models, filters
from task_manager.tasks.mixins import OnlyAuthorCanEditMixin


class TaskFilterView(LoginRequiredMixin, FilterView):
    """Task list view with filter."""

    filterset_class = filters.TaskFilter
    queryset = (
        models.Task.objects.select_related("status", "author", "executor")
        .prefetch_related("labels")
        .only(*consts.FieldList.TASK_QUERYSET)
    )
    template_name: str = consts.Template.TASK_LIST.value


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    """Task detail view."""

    queryset = models.Task.objects.prefetch_related("labels")
    template_name: str = consts.Template.TASK_DETAIL.value


class TaskCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    generic.CreateView,
):
    """Task creation view. Author of task is the current user."""

    model = models.Task
    form_class = forms.TaskForm
    template_name: str = consts.Template.TASK_CREATE_UPDATE.value
    success_url: str = reverse_lazy("tasks:list")
    success_message: str = consts.Message.SUCCESS_TASK_CREATION.value

    def form_valid(self, form: forms.TaskForm) -> HttpResponse:
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(
    LoginRequiredMixin,
    OnlyAuthorCanEditMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    """Task editing view. Only author can edit the task."""

    form_class = forms.TaskForm
    queryset = models.Task.objects.prefetch_related("labels")
    template_name: str = consts.Template.TASK_CREATE_UPDATE.value
    success_url: str = reverse_lazy("tasks:list")
    success_message: str = consts.Message.SUCCESS_TASK_UPDATE.value
    author_error_message: str = consts.Message.FAILURE_TASK_UPDATE.value


class TaskDeleteView(
    LoginRequiredMixin,
    OnlyAuthorCanEditMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    """Task deletion view. Only author can delete the task."""

    model = models.Task
    template_name: str = consts.Template.TASK_DELETE.value
    success_url: str = reverse_lazy("tasks:list")
    success_message: str = consts.Message.SUCCESS_TASK_DELETION.value
    author_error_message: str = consts.Message.FAILURE_TASK_DELETE.value
