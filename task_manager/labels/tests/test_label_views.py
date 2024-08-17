from django.urls import reverse
from pytest_django.asserts import assertRedirects
from http import HTTPStatus
from django.test import Client
from task_manager.labels.models import TaskLabel
from django.db.models import QuerySet


def test_label_list_success(
    author_client: Client,
    labels: QuerySet[TaskLabel],
) -> None:
    """
    Label list view returns the correct number of labels
    and they are in the correct order.
    """
    url = reverse("labels:list")
    response = author_client.get(url)
    object_list = response.context.get("object_list")

    assert object_list is not None
    assert list(object_list) == list(labels.order_by("created_at"))


def test_label_creation_success(author_client: Client) -> None:
    """
    Label creation page shows the form and allows to create a new
    label for authorized users.
    """
    url = reverse("labels:create")
    response = author_client.get(url)
    assert "form" in response.context

    response = author_client.post(url, data={"name": "New Test Label"})
    assertRedirects(response, reverse("labels:list"), HTTPStatus.FOUND)
    assert TaskLabel.objects.filter(name="New Test Label").exists()


def test_label_creation_failure(client: Client) -> None:
    """Anonymous user can't create a new label."""
    url = reverse("labels:create")
    response = client.post(url, data={"name": "New Test Label"})

    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)
    assert not TaskLabel.objects.filter(name="New Test Label").exists()


def test_label_update_success(
    author_client: Client,
    labels: QuerySet[TaskLabel],
):
    """
    Label update page shows the form and allows to update an existing
    label for authorized users.
    """
    label = labels.first()
    url = reverse("labels:update", kwargs={"pk": label.pk})
    response = author_client.get(url)

    assert "form" in response.context
    assert response.context.get("form").instance == label

    response = author_client.post(url, data={"name": "Updated Label"})
    assertRedirects(response, reverse("labels:list"), HTTPStatus.FOUND)

    label.refresh_from_db()
    assert label.name == "Updated Label"


def test_label_update_failure(client: Client, labels: QuerySet[TaskLabel]):
    """Anonymous user can't update an existing label."""
    label = labels.first()
    url = reverse("labels:update", kwargs={"pk": label.pk})
    response = client.post(url, data={"name": "Updated Label"})
    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)

    label.refresh_from_db()
    assert label.name != "Updated Label"


def test_label_delete_success(
    author_client: Client,
    labels: QuerySet[TaskLabel],
):
    """
    Label delete page shows the confirmation and allows to delete an existing
    label for authorized users.
    """
    label = labels.last()
    url = reverse("labels:delete", kwargs={"pk": label.pk})
    response = author_client.post(url)

    assertRedirects(response, reverse("labels:list"), HTTPStatus.FOUND)
    assert not TaskLabel.objects.filter(pk=label.pk).exists()


def test_label_delete_failure(client: Client, labels: QuerySet[TaskLabel]):
    """Anonymous user can't delete an existing label."""
    label = labels.last()
    url = reverse("labels:delete", kwargs={"pk": label.pk})
    response = client.post(url)

    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)
    assert TaskLabel.objects.filter(pk=label.pk).exists()
