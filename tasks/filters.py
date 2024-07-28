import django_filters
from django import forms
from tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    only_mine = django_filters.BooleanFilter(
        label="Только свои задачи",
        method="filter_only_mine",
        widget=forms.CheckboxInput,
    )

    class Meta:
        model = Task
        fields = ["status", "executor", "labels"]

    def filter_only_mine(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
