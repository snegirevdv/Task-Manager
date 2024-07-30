from http import HTTPStatus

from django.http import HttpResponse
from django.test import Client
from django.urls import reverse
import pytest
from pytest_django.asserts import assertRedirects

from users.forms import UserForm
from users.models import User


def test_user_list_success(client: Client, author: User, another_user: User):
    """Any user, even anonymous, can see the user list."""
    url: str = reverse("users:list")
    response: HttpResponse = client.get(url)
    assert response.status_code == HTTPStatus.OK

    assert len(response.context["user_list"]) == User.objects.count()


def test_register_form_success(client: Client, author_form_data):
    """Anonymous user can register a new user."""
    url: str = reverse("users:create")
    form = UserForm(author_form_data)
    assert form.is_valid(), form.errors

    response: HttpResponse = client.post(url, form.cleaned_data)
    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)

    assert User.objects.exists()


def test_user_update_success(
    author_client: Client,
    author: User,
    author_form_data,
):
    """User can edit their own account."""
    url: str = reverse("users:update", args=[author.pk])
    author_form_data["first_name"] = "Michael"
    response: HttpResponse = author_client.post(url, author_form_data)
    assertRedirects(response, reverse("users:list"), HTTPStatus.FOUND)

    author.refresh_from_db()
    assert author.first_name == "Michael"


def test_user_delete_success(author_client: Client, author: User):
    """User can delete their own account."""
    url: str = reverse("users:delete", args=[author.pk])
    response: HttpResponse = author_client.post(url)
    assertRedirects(response, reverse("users:list"), HTTPStatus.FOUND)

    assert not User.objects.all().exists()


@pytest.mark.parametrize("url_name", ("users:update", "users:delete"))
def test_user_anonymous_edit_failure(
    client: Client,
    author: User,
    url_name: str,
    author_form_data,
):
    """Anonymous user can't edit or delete user accounts."""
    url: str = reverse(url_name, args=[author.pk])
    response: HttpResponse = client.post(url, author_form_data)
    assertRedirects(response, reverse("login"), HTTPStatus.FOUND)

    author.refresh_from_db()
    assert author.first_name == "John"


@pytest.mark.parametrize("url_name", ("users:update", "users:delete"))
def test_user_another_user_edit_failure(
    another_user_client: Client,
    author: User,
    url_name: str,
    author_form_data,
):
    """User can't edit or delete another user account."""
    url: str = reverse(url_name, args=[author.pk])
    author_form_data["first_name"] = "Michael"
    response: HttpResponse = another_user_client.post(url, author_form_data)
    assertRedirects(
        response=response,
        expected_url=reverse("users:list"),
        status_code=HTTPStatus.FOUND,
    )
    author.refresh_from_db()
    assert author.first_name == "John"


@pytest.mark.django_db
def test_status_protected_deletion_failure(
    author_client: Client,
    another_user: User,
):
    """The using user can't be deleted."""
    url = reverse("users:delete", args=[another_user.pk])
    response = author_client.post(url)

    assertRedirects(response, reverse("users:list"), HTTPStatus.FOUND)
    assert User.objects.all().exists()
