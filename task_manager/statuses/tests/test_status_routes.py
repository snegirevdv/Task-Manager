from http import HTTPStatus

import pytest
from django.db.models import QuerySet
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from task_manager.core.tests import consts
from task_manager.statuses.models import TaskStatus


@pytest.mark.parametrize("route, has_obj", consts.Routes.STATUSES)
def test_status_routes_authorized_success(
    author_client: Client,
    statuses: QuerySet[TaskStatus],
    route: str,
    has_obj: bool,
):
    """Routes are accessible for an authorized user."""
    kwargs: dict[str, int] = consts.Kwargs.FIRST if has_obj else {}
    url: str = reverse(route, kwargs=kwargs)
    response: HttpResponse = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize("route, has_obj", consts.Routes.STATUSES)
def test_status_routes_unauthorized_redirect(
    client: Client,
    statuses: QuerySet[TaskStatus],
    route: str,
    has_obj: bool,
):
    """Routes redirect an unauthorized user to the login page."""
    kwargs: dict[str, int] = consts.Kwargs.FIRST if has_obj else {}
    url: str = reverse(route, kwargs=kwargs)
    response: HttpResponse = client.get(url)

    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)
