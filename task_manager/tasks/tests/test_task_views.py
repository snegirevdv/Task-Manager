from http import HTTPStatus

from django.db.models import QuerySet
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from task_manager.core.tests import consts
from task_manager.labels.models import TaskLabel
from task_manager.statuses.models import TaskStatus
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task
from task_manager.users.models import User


def test_task_list_success(author_client: Client, tasks: QuerySet[Task]):
    """
    Task list view returns the correct number of tasks
    and they are in the correct order.
    """
    url: str = reverse("tasks:list")
    response: HttpResponse = author_client.get(url)
    object_list: list[Task] = response.context.get("object_list")

    assert object_list is not None
    assert list(object_list) == list(tasks.order_by("created_at"))


def test_task_creation_success(author_client: Client, tasks: QuerySet[Task]):
    """
    Task creation page shows the form and allows to create a new
    task for authorized users.
    """
    url: str = reverse("tasks:create")
    response: HttpResponse = author_client.get(url)
    assert "form" in response.context

    data = consts.FormData.TASK_VALID.copy()
    response: HttpResponse = author_client.post(url, data=data)
    assertRedirects(response, reverse("tasks:list"), HTTPStatus.FOUND)
    assert Task.objects.filter(name=data["name"]).exists()


def test_anonymous_task_creation_failure(client: Client):
    """Anonymous user can't create a new task."""
    url: str = reverse("tasks:create")
    data = consts.FormData.TASK_VALID.copy()
    response: HttpResponse = client.post(url, data=data)

    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)
    assert not Task.objects.filter(name=data["name"]).exists()


def test_task_update_success(author_client: Client, tasks: QuerySet[Task]):
    """
    Task update page shows the form and allows to update an existing
    task for authorized users.
    """
    task: Task = tasks.first()
    url: str = reverse("tasks:update", kwargs=consts.Kwargs.FIRST)
    response: HttpResponse = author_client.get(url)

    form: TaskForm = response.context.get("form")
    assert form is not None
    assert form.instance == task

    data = consts.FormData.TASK_UPDATE
    response: HttpResponse = author_client.post(url, data=data)
    assertRedirects(response, reverse("tasks:list"), HTTPStatus.FOUND)

    task.refresh_from_db()
    assert task.name == data["name"]
    assert task.description == data["description"]


def test_anonymous_task_update_failure(client: Client, tasks: QuerySet[Task]):
    """Anonymous user can't update an existing task."""
    task: Task = tasks.first()
    url: str = reverse("tasks:update", kwargs=consts.Kwargs.FIRST)
    data = consts.FormData.LABEL_UPDATE
    response: HttpResponse = client.post(url, data=data)
    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)

    task.refresh_from_db()
    assert task.name != data["name"]


def test_task_delete_success(author_client: Client, tasks: QuerySet[Task]):
    """
    Task delete page shows the confirmation and allows to delete an existing
    task for authorized users.
    """
    task: Task = tasks.last()
    url: str = reverse("tasks:delete", kwargs={"pk": task.pk})
    response: HttpResponse = author_client.post(url)

    assertRedirects(response, reverse("tasks:list"), HTTPStatus.FOUND)
    assert not Task.objects.filter(pk=task.pk).exists()


def test_anonymous_task_delete_failure(client: Client, tasks: QuerySet[Task]):
    """Anonymous user can't delete an existing task."""
    task: Task = tasks.last()
    url: str = reverse("tasks:delete", kwargs={"pk": task.pk})
    response = client.post(url)

    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)
    assert Task.objects.filter(pk=task.pk).exists()


def test_task_detail_success(author_client: Client, tasks: QuerySet[Task]):
    """
    Task detail view shows the correct task
    for authorized users.
    """
    task: Task = tasks.first()
    url: str = reverse("tasks:detail", kwargs={"pk": task.pk})
    response: HttpResponse = author_client.get(url)

    obj: Task = response.context.get("object")
    assert obj == task


def test_non_author_task_update_failure(
    another_user_client: Client,
    tasks: QuerySet[Task],
):
    """Non-author user can't update not own task."""
    task: Task = tasks.first()
    url: str = reverse("tasks:update", kwargs=consts.Kwargs.FIRST)
    data = consts.FormData.LABEL_UPDATE
    response = another_user_client.post(url, data=data)

    assertRedirects(response, reverse("tasks:list"), HTTPStatus.FOUND)

    task.refresh_from_db()
    assert task.name != data["name"]


def test_non_author_task_deletion_failure(
    another_user_client: Client,
    tasks: QuerySet[Task],
):
    """Non-author user can't delete not own task."""
    task: Task = tasks.first()
    url: str = reverse("tasks:delete", kwargs={"pk": task.pk})
    response: HttpResponse = another_user_client.post(url)

    assertRedirects(response, reverse("tasks:list"), HTTPStatus.FOUND)
    assert Task.objects.filter(pk=task.pk).exists()


def test_delete_status_related_to_task_failure(
    author_client: Client, tasks: QuerySet[Task]
) -> None:
    """Cannot delete a status that is related to an existing task."""
    task: Task = tasks.first()
    status: TaskStatus = task.status
    url: str = reverse("statuses:delete", kwargs={"pk": status.pk})

    response: HttpResponse = author_client.post(url)
    assertRedirects(response, reverse("statuses:list"), HTTPStatus.FOUND)
    assert TaskStatus.objects.filter(pk=status.pk).exists()


def test_delete_label_related_to_task_failure(
    author_client: Client,
    tasks: QuerySet[Task],
):
    """Cannot delete a label that is related to an existing task."""
    task: Task = tasks.first()
    label: TaskLabel = task.labels.first()
    url: str = reverse("labels:delete", kwargs={"pk": label.pk})

    response: HttpResponse = author_client.post(url)
    assertRedirects(response, reverse("labels:list"), HTTPStatus.FOUND)
    assert TaskLabel.objects.filter(pk=label.pk).exists()


def test_delete_user_related_to_task_failure(
    author_client: Client,
    tasks: QuerySet[Task],
):
    """Cannot delete a user that is related to an existing task."""
    task: Task = tasks.first()
    user: User = task.executor
    url: str = reverse("users:delete", kwargs={"pk": user.pk})

    response: HttpResponse = author_client.post(url)
    assertRedirects(response, reverse("users:list"), HTTPStatus.FOUND)
    assert User.objects.filter(pk=user.pk).exists()
