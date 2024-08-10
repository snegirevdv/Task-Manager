from django import forms
from django.db.models import QuerySet
import django_filters

from task_manager.core import consts
from task_manager.labels.models import TaskLabel
from task_manager.tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    """
    Filter for task list.
    Implements fields: status, executor, labels, author.
    """

    labels = django_filters.ModelChoiceFilter(
        label=consts.FormLabel.LABEL.value,
        queryset=TaskLabel.objects.all(),
        widget=forms.Select,
    )

    only_mine = django_filters.BooleanFilter(
        label=consts.FormLabel.ONLY_MINE.value,
        method="filter_only_mine",
        widget=forms.CheckboxInput,
    )

    class Meta:
        model = Task
        fields = consts.FieldList.TASK_FILTER

    def filter_only_mine(
        self,
        queryset: QuerySet[Task],
        name: str,
        value: bool,
    ) -> QuerySet[Task]:
        """Author boolean filter. True: only user tasks. False: all tasks."""
        if value:
            return queryset.filter(author=self.request.user)

        return queryset
