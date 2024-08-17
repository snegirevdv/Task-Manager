from http import HTTPStatus

import pytest
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from task_manager.statuses.models import TaskStatus
from task_manager.statuses.forms import StatusForm
from task_manager.tasks.models import Task


def test_status_list_success(author_client: Client, task_status: TaskStatus):
    """User can see the list of statuses."""
    url: str = reverse("statuses:list")
    response: HttpResponse = author_client.get(url)
    assert response.status_code == HTTPStatus.OK

    assert len(response.context["object_list"]) == TaskStatus.objects.count()


def test_status_create_form_success(author_client: Client):
    """User can create a new status using Status Form."""
    url: str = reverse("statuses:create")
    form = StatusForm({"name": "Test Status"})
    assert form.is_valid(), form.errors

    response: HttpResponse = author_client.post(url, form.cleaned_data)
    assertRedirects(response, reverse("statuses:list"), HTTPStatus.FOUND)

    assert TaskStatus.objects.all().exists()


@pytest.mark.parametrize("name", ("statuses:list", "statuses:create"))
def test_status_anonymous_get_failure(
    client: Client,
    task_status: TaskStatus,
    name: str,
):
    """Anonymous user can't see the status list and status creation page."""
    url: str = reverse(name)
    response: HttpResponse = client.get(url)
    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)


def test_status_anonymous_create_failure(client: Client):
    """Anonymous user cannot create a new status."""
    url: str = reverse("statuses:create")
    response: HttpResponse = client.post(url, {"name": "Test Status"})

    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)
    assert not TaskStatus.objects.exists()


@pytest.mark.django_db
def test_status_update_success(author_client: Client, task_status: TaskStatus):
    """User can edit any status."""
    url: str = reverse("statuses:update", args=[task_status.pk])
    response: HttpResponse = author_client.post(url, {"name": "abc"})
    assertRedirects(response, reverse("statuses:list"), HTTPStatus.FOUND)

    task_status.refresh_from_db()
    assert task_status.name == "abc"


@pytest.mark.django_db
def test_status_delete_success(author_client: Client, task_status: TaskStatus):
    """User can delete any status."""
    url: str = reverse("statuses:delete", args=[task_status.pk])
    response: HttpResponse = author_client.post(url)
    assertRedirects(response, reverse("statuses:list"), HTTPStatus.FOUND)

    assert not TaskStatus.objects.all().exists()


@pytest.mark.parametrize("url_name", ("statuses:update", "statuses:delete"))
def test_status_anonymous_edit_failure(
    client: Client,
    task_status: TaskStatus,
    url_name: str,
):
    """Anonymous use cannot edit or delete statuses."""
    url: str = reverse(url_name, args=[task_status.pk])
    response: HttpResponse = client.post(url, {"name": "abc"})
    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)

    task_status.refresh_from_db()
    assert task_status.name == "Test Status"


@pytest.mark.django_db
def test_status_protected_deletion_failure(
    author_client: Client,
    task_status: TaskStatus,
    task: Task,
):
    """The using status cannot be deleted."""
    url: str = reverse("statuses:delete", args=[task_status.pk])
    response: HttpResponse = author_client.post(url)

    assertRedirects(response, reverse("statuses:list"), HTTPStatus.FOUND)
    assert TaskStatus.objects.all().exists()
