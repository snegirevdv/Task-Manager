from http import HTTPStatus

from django.http import HttpResponse
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from task_manager.core.tests import consts
from task_manager.users.forms import UserForm
from task_manager.users.models import User


def test_user_create_view_success(client: Client):
    """
    User creation page shows the form and allows
    to create a new user for any user.
    """
    url: str = reverse("users:create")
    response: HttpResponse = client.get(url)
    assert "form" in response.context

    data = consts.FormData.USER_VALID
    response: HttpResponse = client.post(url, data=data)
    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)
    assert User.objects.filter(username=data["username"]).exists()


def test_user_update_view_success(author_client: Client):
    """
    User update page shows the form and allows the
    user to update their own account.
    """
    user = User.objects.get(**consts.Kwargs.AUTHOR)
    url: str = reverse("users:update", kwargs=consts.Kwargs.AUTHOR)
    response: HttpResponse = author_client.get(url)
    assert "form" in response.context

    form: UserForm = response.context["form"]
    assert form.instance == user

    data = consts.FormData.USER_UPDATE
    response: HttpResponse = author_client.post(url, data=data)
    assertRedirects(response, reverse("index"), HTTPStatus.FOUND)

    user.refresh_from_db()
    assert user.username == data["username"]


def test_user_update_view_failure(client: Client, another_user_client: Client):
    """
    Anonymous user or a user trying to update someone
    else's account is redirected.
    """
    user = User.objects.get(**consts.Kwargs.AUTHOR)
    url: str = reverse("users:update", kwargs=consts.Kwargs.AUTHOR)
    data = consts.FormData.USER_UPDATE

    anonymous_response: HttpResponse = client.post(url, data=data)
    assertRedirects(anonymous_response, reverse("login"), HTTPStatus.FOUND)

    nonauthor_response: HttpResponse = another_user_client.post(url, data=data)
    assertRedirects(
        nonauthor_response,
        reverse("index"),
        HTTPStatus.FOUND,
    )

    user.refresh_from_db()
    assert user.username != data["username"]


def test_user_delete_view_success(author_client: Client):
    """
    User deletion page shows the confirmation and allows
    the user to delete their own account.
    """
    user = User.objects.get(**consts.Kwargs.AUTHOR)
    url: str = reverse("users:delete", kwargs=consts.Kwargs.AUTHOR)
    response: HttpResponse = author_client.post(url)
    assertRedirects(response, reverse("index"), HTTPStatus.FOUND)

    assert not User.objects.filter(pk=user.pk).exists()


def test_user_delete_view_failure(
    client: Client,
    another_user_client: Client,
):
    """
    Anonymous user or a user trying to delete
    someone else's account is redirected.
    """
    user = User.objects.get(**consts.Kwargs.AUTHOR)
    url: str = reverse("users:delete", kwargs=consts.Kwargs.AUTHOR)

    response: HttpResponse = client.post(url)
    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)

    response: HttpResponse = another_user_client.post(url)
    assertRedirects(response, reverse("index"), HTTPStatus.FOUND)

    assert User.objects.filter(pk=user.pk).exists()
