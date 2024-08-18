from http import HTTPStatus

from django.db.models import QuerySet
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from task_manager.core.tests import consts
from task_manager.labels.forms import LabelForm
from task_manager.labels.models import TaskLabel


def test_label_list_success(
    author_client: Client,
    labels: QuerySet[TaskLabel],
):
    """
    Label list returns the correct number of labels
    and they are in the correct order.
    """
    url: str = reverse("labels:list")
    response: HttpResponse = author_client.get(url)
    object_list: QuerySet[TaskLabel] = response.context.get("object_list")

    assert object_list is not None
    assert list(object_list) == list(labels.order_by("created_at"))


def test_label_creation_success(author_client: Client):
    """
    Label creation page shows the form and allows to create
    a new label for authorized users.
    """
    url = reverse("labels:create")
    response = author_client.get(url)
    assert "form" in response.context

    data = consts.FormData.LABEL_VALID
    response = author_client.post(url, data=data)
    assertRedirects(response, reverse("labels:list"), HTTPStatus.FOUND)
    assert TaskLabel.objects.filter(**data).exists()


def test_label_creation_failure(client: Client):
    """Anonymous user can't create a new label."""
    url = reverse("labels:create")
    data = consts.FormData.LABEL_VALID
    response = client.post(url, data=data)

    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)
    assert not TaskLabel.objects.filter(**data).exists()


def test_label_update_success(
    author_client: Client,
    labels: QuerySet[TaskLabel],
):
    """
    Label update page shows the form and allows to update
    an existing label for authorized users.
    """
    label = labels.first()
    url = reverse("labels:update", kwargs=consts.Kwargs.FIRST)
    response = author_client.get(url)

    form: LabelForm = response.context.get("form")
    assert form is not None
    assert form.instance == label

    data = consts.FormData.LABEL_UPDATE
    response = author_client.post(url, data=data)
    assertRedirects(response, reverse("labels:list"), HTTPStatus.FOUND)

    label.refresh_from_db()
    assert label.name == data["name"]


def test_label_update_failure(client: Client, labels: QuerySet[TaskLabel]):
    """Anonymous user can't update an existing label."""
    label: TaskLabel = labels.first()
    url: str = reverse("labels:update", kwargs=consts.Kwargs.FIRST)
    data = consts.FormData.LABEL_UPDATE
    response: HttpResponse = client.post(url, data=data)
    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)

    label.refresh_from_db()
    assert label.name != data["name"]


def test_label_delete_success(
    author_client: Client,
    labels: QuerySet[TaskLabel],
):
    """
    Label delete page shows the confirmation and allows to delete an existing
    label for authorized users.
    """
    label: TaskLabel = labels.first()
    url = reverse("labels:delete", kwargs=consts.Kwargs.FIRST)
    response: HttpResponse = author_client.post(url)

    assertRedirects(response, reverse("labels:list"), HTTPStatus.FOUND)
    assert not TaskLabel.objects.filter(pk=label.pk).exists()


def test_label_delete_failure(client: Client, labels: QuerySet[TaskLabel]):
    """Anonymous user can't delete an existing label."""
    label: TaskLabel = labels.first()
    url: str = reverse("labels:delete", kwargs=consts.Kwargs.FIRST)
    response: HttpResponse = client.post(url)

    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)
    assert TaskLabel.objects.filter(pk=label.pk).exists()
