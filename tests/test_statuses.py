from http import HTTPStatus

import pytest
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from statuses.models import TaskStatus
from statuses.forms import StatusForm
from tasks.models import Task


def test_status_list_success(author_client: Client, task_status: TaskStatus):
    url: str = reverse("statuses:list")
    response: HttpResponse = author_client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert len(response.context["object_list"]) == TaskStatus.objects.count()


def test_status_create_form_success(author_client: Client):
    url = reverse("statuses:create")
    form = StatusForm(data={"name": "Test Status"})
    assert form.is_valid(), form.errors

    response = author_client.post(url, data=form.cleaned_data)
    assertRedirects(response, reverse("statuses:list"), HTTPStatus.FOUND)

    assert TaskStatus.objects.filter(name="Test Status").exists()


@pytest.mark.parametrize("name", ("statuses:list", "statuses:create"))
def test_status_anonymous_get_failure(client: Client, task_status: TaskStatus, name: str):
    url: str = reverse(name)
    response: HttpResponse = client.get(url)

    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)


def test_status_anonymous_create_failure(
    client: Client
):
    url = reverse("statuses:create")
    response = client.post(url, data={"name": "Test Status"})

    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)
    assert not TaskStatus.objects.exists()


@pytest.mark.django_db
def test_status_update_success(author_client: Client, task_status: TaskStatus):
    url: str = reverse("statuses:update", args=[task_status.pk])
    response: HttpResponse = author_client.post(url, data={"name": "abc"})

    assertRedirects(response, reverse("statuses:list"), HTTPStatus.FOUND)

    task_status.refresh_from_db()
    assert task_status.name == "abc"


@pytest.mark.django_db
def test_status_delete_success(author_client: Client, task_status: TaskStatus):
    url = reverse("statuses:delete", args=[task_status.pk])
    response = author_client.post(url)

    assertRedirects(response, reverse("statuses:list"), HTTPStatus.FOUND)
    assert not TaskStatus.objects.filter(pk=task_status.pk).exists()


@pytest.mark.parametrize("url_name", ("statuses:update", "statuses:delete"))
def test_status_anonymous_edit_failure(
    client: Client,
    task_status: TaskStatus,
    url_name: str,
):
    url = reverse(url_name, args=[task_status.pk])
    response = client.post(url, data={"name": "abc"})
    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)

    task_status.refresh_from_db()
    assert task_status.name == "Test Status"


@pytest.mark.django_db
def test_status_protected_deletion_failure(
    author_client: Client,
    task_status: TaskStatus,
    task: Task,
):
    url = reverse("statuses:delete", args=[task_status.pk])
    response = author_client.post(url)

    assertRedirects(response, reverse("statuses:list"), HTTPStatus.FOUND)
    assert TaskStatus.objects.filter(pk=task_status.pk).exists()
