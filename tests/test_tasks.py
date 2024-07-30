from http import HTTPStatus
from typing import Any

import pytest
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from statuses.models import TaskStatus
from tasks.forms import TaskForm
from tasks.models import Task


def test_task_list_success(author_client: Client, task: Task):
    """User can see the list of tasks."""
    url: str = reverse("tasks:list")
    response: HttpResponse = author_client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert len(response.context["object_list"]) == Task.objects.count()


def test_task_create_form_success(
    author_client: Client,
    task_form_data: dict[str, Any],
):
    """User can create a new task using Task Form."""
    url: str = reverse("tasks:create")
    form = TaskForm(task_form_data)
    assert form.is_valid(), form.errors

    response: HttpResponse = author_client.post(url, task_form_data)
    assertRedirects(response, reverse("tasks:list"), HTTPStatus.FOUND)

    assert Task.objects.all().exists()


@pytest.mark.parametrize("name", ("tasks:list", "tasks:create"))
def test_task_anonymous_get_failure(client: Client, name: str):
    """Anonymous user can't see the task list and task creation page."""
    url: str = reverse(name)
    response: HttpResponse = client.get(url)

    assertRedirects(response, reverse("login"))


def test_task_anonymous_create_failure(
    client: Client,
    task_form_data: dict[str, Any],
):
    """Anonymous user cannot create a new task."""
    url: str = reverse("tasks:create")
    response: HttpResponse = client.post(url, task_form_data)

    assertRedirects(response, reverse("login"))
    assert not Task.objects.all().exists()


@pytest.mark.django_db
def test_task_update_success(
    author_client: Client,
    task: Task,
    task_form_data: dict[str, Any],
):
    """User can edit their own task."""
    url: str = reverse("tasks:update", args=[task.pk])
    task_form_data["name"] = "abc"
    response: HttpResponse = author_client.post(url, task_form_data)

    assertRedirects(
        response, reverse("tasks:list"), status_code=HTTPStatus.FOUND
    )

    task.refresh_from_db()
    assert task.name == "abc"


@pytest.mark.django_db
def test_task_delete_success(author_client: Client, task: TaskStatus):
    """User can delete their own task."""
    url: str = reverse("tasks:delete", args=[task.pk])
    response: HttpResponse = author_client.post(url)

    assertRedirects(response, reverse("tasks:list"))
    assert not Task.objects.all().exists()


@pytest.mark.django_db
def test_task_non_author_update_failure(
    another_user_client: Client,
    task: Task,
    task_form_data: dict[str, Any],
):
    """User can't edit other users' tasks."""
    url: str = reverse("tasks:update", args=[task.pk])
    task_form_data["name"] = "abc"
    response: HttpResponse = another_user_client.post(url, task_form_data)
    assertRedirects(response, reverse("tasks:list"), HTTPStatus.FOUND)

    task.refresh_from_db()
    assert task.name == "Test Task"


@pytest.mark.django_db
def test_task_non_author_delete_failure(
    another_user_client: Client,
    task: TaskStatus,
):
    """User can't delete other users' tasks."""
    url: str = reverse("tasks:delete", args=[task.pk])
    response: HttpResponse = another_user_client.post(url)
    assertRedirects(response, reverse("tasks:list"))

    assert Task.objects.all().exists()


@pytest.mark.parametrize("url_name", ("tasks:update", "tasks:delete"))
def test_task_anonymous_edit_failure(
    client: Client,
    task: Task,
    url_name: str,
    task_form_data: dict[str, Any],
):
    """Anonymous user can't edit or delete tasks."""
    url: str = reverse(url_name, args=[task.pk])
    task_form_data["name"] = "abc"
    response: HttpResponse = client.post(url, task_form_data)
    assertRedirects(response, reverse("login"))

    task.refresh_from_db()
    assert task.name == "Test Task"


@pytest.mark.django_db
def test_task_protected_deletion_failure(
    another_user_client: Client,
    task: Task,
):
    """The using task can't be deleted"""
    url: str = reverse("tasks:delete", args=[task.pk])
    response: HttpResponse = another_user_client.post(url)
    assertRedirects(response, reverse("tasks:list"))

    assert Task.objects.all().exists()
