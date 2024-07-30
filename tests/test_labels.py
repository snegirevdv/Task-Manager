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
    url: str = reverse("labels:list")
    response: HttpResponse = author_client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert len(response.context["object_list"]) == TaskLabel.objects.count()


def test_label_create_form_success(author_client: Client):
    url = reverse("labels:create")
    form = LabelForm(data={"name": "Test Label"})
    assert form.is_valid(), form.errors

    response = author_client.post(url, data=form.cleaned_data)
    assertRedirects(response, reverse("labels:list"), HTTPStatus.FOUND)

    assert TaskLabel.objects.filter(name="Test Label").exists()


@pytest.mark.parametrize("name", ("labels:list", "labels:create"))
def test_label_anonymous_get_failure(client: Client, task_label: TaskLabel, name: str):
    url: str = reverse(name)
    response: HttpResponse = client.get(url)

    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)


def test_label_anonymous_create_failure(
    client: Client
):
    url = reverse("labels:create")
    response = client.post(url, data={"name": "Test Label"})

    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)
    assert not TaskLabel.objects.exists()


@pytest.mark.django_db
def test_label_update_success(author_client: Client, task_label: TaskLabel):
    url: str = reverse("labels:update", args=[task_label.pk])
    response: HttpResponse = author_client.post(url, data={"name": "abc"})

    assertRedirects(response, reverse("labels:list"), HTTPStatus.FOUND)

    task_label.refresh_from_db()
    assert task_label.name == "abc"


@pytest.mark.django_db
def test_label_delete_success(author_client: Client, task_label: TaskLabel):
    url = reverse("labels:delete", args=[task_label.pk])
    response = author_client.post(url)

    assertRedirects(response, reverse("labels:list"), HTTPStatus.FOUND)
    assert not TaskLabel.objects.filter(pk=task_label.pk).exists()


@pytest.mark.parametrize("url_name", ("labels:update", "labels:delete"))
def test_label_anonymous_edit_failure(
    client: Client,
    task_label: TaskLabel,
    url_name: str,
):
    url = reverse(url_name, args=[task_label.pk])
    response = client.post(url, data={"name": "abc"})
    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)

    task_label.refresh_from_db()
    assert task_label.name == "Test Label"


@pytest.mark.django_db
def test_label_protected_deletion_failure(
    author_client: Client,
    task_label: TaskLabel,
    task: Task,
):
    url = reverse("labels:delete", args=[task_label.pk])
    response = author_client.post(url)

    assertRedirects(response, reverse("labels:list"), HTTPStatus.FOUND)
    assert TaskLabel.objects.filter(pk=task_label.pk).exists()
