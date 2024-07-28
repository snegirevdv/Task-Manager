from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from django_filters.views import FilterView

from core import mixins
from tasks import forms, models
from tasks.filters import TaskFilter


class TaskFilterView(mixins.LoginRequiredMixin, FilterView):
    model = models.Task
    filterset_class = TaskFilter
    template_name = "tasks/list.html"


class TaskDetailView(mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Task
    template_name = "tasks/detail.html"


class TaskCreateView(
    mixins.LoginRequiredMixin,
    SuccessMessageMixin,
    generic.CreateView,
):
    model = models.Task
    form_class = forms.TaskForm
    template_name = "tasks/update_delete.html"
    success_url = reverse_lazy("tasks:list")
    success_message = "Задача успешно создана."

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(
    mixins.LoginRequiredMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    model = models.Task
    form_class = forms.TaskForm
    template_name = "tasks/update_delete.html"
    success_url = reverse_lazy("tasks:list")
    success_message = "Задача успешно изменена."

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskDeleteView(
    mixins.LoginRequiredMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    model = models.Task
    template_name = "tasks/delete.html"
    success_url = reverse_lazy("tasks:list")
    success_message = "Задача успешно удалена."
