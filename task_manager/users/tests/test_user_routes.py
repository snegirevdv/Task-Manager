from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from task_manager.core.tests import consts


@pytest.mark.parametrize("route", consts.Routes.USERS_OPEN)
def test_open_routes_success(client: Client, route: str) -> None:
    """The list and creation routes are accessible for any user."""
    url = reverse(route)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize("route", consts.Routes.USERS_PROTECTED)
def test_protected_routes_success(author_client: Client, route: str) -> None:
    """Protected routes redirect unauthenticated users to the login page."""
    url = reverse(route, kwargs=consts.Kwargs.AUTHOR)
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize("route", consts.Routes.USERS_PROTECTED)
def test_protected_routes_failure(
    client: Client, another_user_client: Client, route: str
) -> None:
    """
    Protected routes return forbidden when accessed
    by anonymous or another authenticated user.
    """
    url = reverse(route, kwargs=consts.Kwargs.AUTHOR)
    another_user_response = another_user_client.get(url)
    assertRedirects(another_user_response, reverse("index"), HTTPStatus.FOUND)

    anonymous_response = client.get(url)
    assertRedirects(anonymous_response, reverse("login"), HTTPStatus.FOUND)
