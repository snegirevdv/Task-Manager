from django.http import HttpResponse
import pytest
from pytest_django.asserts import assertRedirects
from django.urls import reverse
from http import HTTPStatus
from django.test import Client
from task_manager.tasks.models import TaskStatus
from django.db.models import QuerySet
from task_manager.core.tests import consts


@pytest.mark.parametrize("route, has_obj", consts.Routes.TASKS)
def test_task_routes_authorized_success(
    author_client: Client,
    tasks: QuerySet[TaskStatus],
    route: str,
    has_obj: bool,
):
    """Routes are accessible for an authorized user."""
    kwargs: dict[str, int] = consts.Kwargs.FIRST if has_obj else {}
    url: str = reverse(route, kwargs=kwargs)
    response: HttpResponse = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize("route, has_obj", consts.Routes.TASKS)
def test_task_routes_unauthorized_redirect(
    client: Client,
    tasks: QuerySet[TaskStatus],
    route: str,
    has_obj: bool,
):
    """Routes redirect an unauthorized user to the login page."""
    kwargs: dict[str, int] = consts.Kwargs.FIRST if has_obj else {}
    url: str = reverse(route, kwargs=kwargs)
    response: HttpResponse = client.get(url)

    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)
