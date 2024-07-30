from http import HTTPStatus

import pytest
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from labels.models import TaskLabel
from labels.forms import LabelForm
from tasks.models import Task


def test_label_list_success(author_client: Client, task_label: TaskLabel):
    """User can see the list of labels."""
    url: str = reverse("labels:list")
    response: HttpResponse = author_client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert len(response.context["object_list"]) == TaskLabel.objects.count()


def test_label_create_form_success(author_client: Client):
    """User can create a new label using Label Form."""
    url: str = reverse("labels:create")
    form = LabelForm({"name": "Test Label"})
    assert form.is_valid(), form.errors

    response: HttpResponse = author_client.post(url, form.cleaned_data)
    assertRedirects(response, reverse("labels:list"), HTTPStatus.FOUND)

    assert TaskLabel.objects.all().exists()


@pytest.mark.parametrize("name", ("labels:list", "labels:create"))
def test_label_anonymous_get_failure(
    client: Client,
    task_label: TaskLabel,
    name: str,
):
    """Anonymous user cannot see the list of labels and label creation page."""
    url: str = reverse(name)
    response: HttpResponse = client.get(url)

    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)


def test_label_anonymous_create_failure(client: Client):
    """Anonymous user cannot create a new label."""
    url: str = reverse("labels:create")
    response: HttpResponse = client.post(url, {"name": "Test Label"})

    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)
    assert not TaskLabel.objects.exists()


@pytest.mark.django_db
def test_label_update_success(author_client: Client, task_label: TaskLabel):
    """User can edit any label."""
    url: str = reverse("labels:update", args=[task_label.pk])
    response: HttpResponse = author_client.post(url, {"name": "abc"})

    assertRedirects(response, reverse("labels:list"), HTTPStatus.FOUND)

    task_label.refresh_from_db()
    assert task_label.name == "abc"


@pytest.mark.django_db
def test_label_delete_success(author_client: Client, task_label: TaskLabel):
    """User can delete any label."""
    url: str = reverse("labels:delete", args=[task_label.pk])
    response: HttpResponse = author_client.post(url)

    assertRedirects(response, reverse("labels:list"), HTTPStatus.FOUND)
    assert not TaskLabel.objects.all().exists()


@pytest.mark.parametrize("url_name", ("labels:update", "labels:delete"))
def test_label_anonymous_edit_failure(
    client: Client,
    task_label: TaskLabel,
    url_name: str,
):
    """Anonymous use cannot edit or delete labels."""
    url: str = reverse(url_name, args=[task_label.pk])
    response: HttpResponse = client.post(url, {"name": "abc"})
    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)

    task_label.refresh_from_db()
    assert task_label.name == "Test Label"


@pytest.mark.django_db
def test_label_protected_deletion_failure(
    author_client: Client,
    task_label: TaskLabel,
    task: Task,
):
    """The using label cannot be deleted."""
    url: str = reverse("labels:delete", args=[task_label.pk])
    response: HttpResponse = author_client.post(url)

    assertRedirects(response, reverse("labels:list"), HTTPStatus.FOUND)
    assert TaskLabel.objects.all().exists()
