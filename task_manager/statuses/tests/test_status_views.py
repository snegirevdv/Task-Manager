from http import HTTPStatus

from django.db.models import QuerySet
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from task_manager.core.tests import consts
from task_manager.statuses.models import TaskStatus


def test_status_list_success(
    author_client: Client,
    statuses: QuerySet[TaskStatus],
):
    """
    Label list view returns the correct number of statuses
    and they are in the correct order.
    """
    url = reverse("statuses:list")
    response = author_client.get(url)
    object_list = response.context.get("object_list")

    assert object_list is not None
    assert list(object_list) == list(statuses.order_by("created_at"))


def test_status_creation_success(author_client: Client):
    """
    Label creation page shows the form and allows to create a new
    status for authorized users.
    """
    url = reverse("statuses:create")
    response = author_client.get(url)
    assert "form" in response.context

    data = consts.FormData.STATUS_VALID
    response = author_client.post(url, data=data)
    assertRedirects(response, reverse("statuses:list"), HTTPStatus.FOUND)
    assert TaskStatus.objects.filter(**data).exists()


def test_status_creation_failure(client: Client):
    """Anonymous user can't create a new status."""
    url = reverse("statuses:create")
    data = consts.FormData.STATUS_VALID
    response = client.post(url, data=data)

    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)
    assert not TaskStatus.objects.filter(**data).exists()


def test_status_update_success(
    author_client: Client,
    statuses: QuerySet[TaskStatus],
):
    """
    Label update page shows the form and allows to update an existing
    status for authorized users.
    """
    status = statuses.first()
    url = reverse("statuses:update", kwargs=consts.Kwargs.FIRST)
    response = author_client.get(url)

    assert "form" in response.context
    assert response.context.get("form").instance == status

    data = consts.FormData.STATUS_UPDATE
    response = author_client.post(url, data=data)
    assertRedirects(response, reverse("statuses:list"), HTTPStatus.FOUND)

    status.refresh_from_db()
    assert status.name == data["name"]


def test_status_update_failure(client: Client, statuses: QuerySet[TaskStatus]):
    """Anonymous user can't update an existing status."""
    status = statuses.first()
    data = consts.FormData.STATUS_UPDATE
    url = reverse("statuses:update", kwargs=consts.Kwargs.FIRST)
    response = client.post(url, data=data)
    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)

    status.refresh_from_db()
    assert status.name != data["name"]


def test_status_delete_success(
    author_client: Client,
    statuses: QuerySet[TaskStatus],
):
    """
    Label delete page shows the confirmation and allows to delete an existing
    status for authorized users.
    """
    status = statuses.first()
    url = reverse("statuses:delete", kwargs=consts.Kwargs.FIRST)
    response = author_client.post(url)

    assertRedirects(response, reverse("statuses:list"), HTTPStatus.FOUND)
    assert not TaskStatus.objects.filter(pk=status.pk).exists()


def test_status_delete_failure(client: Client, statuses: QuerySet[TaskStatus]):
    """Anonymous user can't delete an existing status."""
    status = statuses.first()
    url = reverse("statuses:delete", kwargs=consts.Kwargs.FIRST)
    response = client.post(url)

    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)
    assert TaskStatus.objects.filter(pk=status.pk).exists()
