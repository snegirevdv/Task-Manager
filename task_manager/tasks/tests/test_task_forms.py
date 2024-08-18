from django.urls import reverse
from http import HTTPStatus
from django.db.models import QuerySet
from django.test import Client
from django.http import HttpResponse

from task_manager.core.tests import consts
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task
from task_manager.statuses.models import TaskStatus
from task_manager.labels.models import TaskLabel
from task_manager.users.models import User


def test_task_form_success(author_client: Client, tasks):
    """User can create a new task using Task Form."""
    form_data = consts.FormData.TASK_VALID.copy()
    url: str = reverse("tasks:create")
    form = TaskForm(data=form_data)
    assert form.is_valid(), form.errors

    author_client.post(url, data=form_data)
    labels = form_data.pop("labels")
    assert Task.objects.filter(**form_data).exists()

    task = Task.objects.get(**form_data)
    assert list(task.labels.values_list('pk', flat=True)) == labels


def test_task_form_invalid_data_failure(author_client: Client):
    """User can't create a new task using Task Form with invalid data."""
    url: str = reverse("tasks:create")
    form_data = consts.FormData.TASK_VALID.copy()
    form_data["name"] = ""

    form = TaskForm(data=form_data)
    assert not form.is_valid()

    author_client.post(url, form_data)
    assert "name" in form.errors
    assert not Task.objects.exists()


def test_task_filter_by_status_success(
    author_client: Client,
    tasks: QuerySet[Task],
):
    """Tasks can be filtered by status."""
    url: str = reverse("tasks:list")
    status = TaskStatus.objects.first()
    data = {"status": status.pk}

    response: HttpResponse = author_client.get(url, data={"status": status.pk})
    assert response.status_code == HTTPStatus.OK

    object_list: list[Task] = response.context["object_list"]
    assert all(task.status.pk == status.pk for task in object_list)
    assert len(object_list) == len(tasks.filter(**data))


def test_task_filter_by_label_success(
    author_client: Client,
    tasks: QuerySet[Task],
):
    """Tasks can be filtered by label."""
    url: str = reverse("tasks:list")
    label = TaskLabel.objects.first()
    data = {"labels": label.pk}

    response: HttpResponse = author_client.get(url, data=data)
    assert response.status_code == HTTPStatus.OK

    object_list: list[Task] = response.context["object_list"]
    assert all(
        task.labels.filter(pk=label.pk).exists()
        for task in object_list
    )
    assert len(object_list) == len(tasks.filter(labels=label.pk))


def test_task_filter_by_executor_success(
    author_client: Client, tasks: QuerySet[Task]
):
    """Tasks can be filtered by executor."""
    url: str = reverse("tasks:list")
    executor = User.objects.last()
    data = {"executor": executor.pk}

    response: HttpResponse = author_client.get(url, data=data)
    assert response.status_code == HTTPStatus.OK

    object_list: list[Task] = response.context["object_list"]
    assert all(task.executor.pk == executor.pk for task in object_list)
    assert len(object_list) == len(tasks.filter(**data))


def test_task_filter_only_mine_success(
    author_client: Client,
    tasks: QuerySet[Task],
):
    """Tasks can be filtered by the current user."""
    url: str = reverse("tasks:list")
    author = User.objects.first()
    data = {"only_mine": True}

    response: HttpResponse = author_client.get(url, data=data)
    assert response.status_code == HTTPStatus.OK

    object_list: list[Task] = response.context["object_list"]
    assert all(task.author == author for task in object_list)
    assert len(object_list) == len(tasks.filter(author=author))
