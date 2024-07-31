from django import forms
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
import django_filters

from labels.models import TaskLabel
from tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    """
    Filter for task list.
    Implements fields: status, executor, labels, author.
    """
    label = django_filters.ModelChoiceFilter(
        label=_("Label"),
        queryset=TaskLabel.objects.all(),
        widget=forms.Select,
    )

    only_mine = django_filters.BooleanFilter(
        label=_("Only own tasks"),
        method="filter_only_mine",
        widget=forms.CheckboxInput,
    )

    class Meta:
        model = Task
        fields = ["status", "executor"]

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
