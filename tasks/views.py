from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django_filters.views import FilterView

from core.mixins import LoginRequiredMixin
from tasks import forms, models, filters
from tasks.mixins import OnlyAuthorCanEditMixin


class TaskFilterView(LoginRequiredMixin, FilterView):
    """Task list view with filter."""

    queryset = (
        models.Task.objects.select_related(
            "status",
            "author",
            "executor",
        )
        .prefetch_related("labels")
        .only(
            "id",
            "name",
            "status__name",
            "author__first_name",
            "author__last_name",
            "executor__first_name",
            "executor__last_name",
            "created_at",
            "labels__name",
        )
    )
    filterset_class = filters.TaskFilter
    template_name = "tasks/list.html"


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    """Task detail view."""

    queryset = models.Task.objects.prefetch_related("labels")
    template_name = "tasks/detail.html"


class TaskCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    generic.CreateView,
):
    """Task creation view. Author of task is the current user."""

    model = models.Task
    form_class = forms.TaskForm
    template_name = "tasks/create_update.html"
    success_url: str = reverse_lazy("tasks:list")
    success_message: str = _("The task has been successfully updated.")

    def form_valid(self, form: forms.TaskForm):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(
    LoginRequiredMixin,
    OnlyAuthorCanEditMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    """Task editing view. Only author can edit the task."""

    queryset = models.Task.objects.prefetch_related("labels")
    form_class = forms.TaskForm
    template_name = "tasks/create_update.html"
    success_url: str = reverse_lazy("tasks:list")
    success_message: str = _("The task has been successfully updated.")
    author_error_message: str = _("Only author can edit the task.")


class TaskDeleteView(
    LoginRequiredMixin,
    OnlyAuthorCanEditMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    """Task deletion view. Only author can delete the task."""

    model = models.Task
    template_name = "tasks/delete.html"
    success_url: str = reverse_lazy("tasks:list")
    success_message: str = _("The task has been successfully deleted.")
    author_error_message: str = _("Only author can delete the task.")
