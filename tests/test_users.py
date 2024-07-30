from http import HTTPStatus

from django.http import HttpResponse
from django.test import Client
from django.urls import reverse
import pytest
from pytest_django.asserts import assertRedirects

from users.forms import UserForm
from users.models import User


def test_user_list_success(client: Client, author: User, another_user: User):
    url: str = reverse("users:list")
    response: HttpResponse = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert len(response.context["user_list"]) == User.objects.count()


def test_register_form_success(client: Client, author_form_data):
    url = reverse("users:create")
    form = UserForm(data=author_form_data)
    assert form.is_valid(), form.errors

    response = client.post(path=url, data=form.cleaned_data)
    assertRedirects(
        response=response,
        expected_url=reverse("login"),
        status_code=HTTPStatus.FOUND,
    )


def test_user_update_success(
    author_client: Client,
    author: User,
    author_form_data,
):
    url = reverse("users:update", args=[author.pk])
    author_form_data["first_name"] = "Michael"
    response = author_client.post(path=url, data=author_form_data)
    assertRedirects(
        response=response,
        expected_url=reverse("users:list"),
        status_code=HTTPStatus.FOUND,
    )

    author.refresh_from_db()
    assert author.first_name == "Michael"


def test_user_delete_success(author_client: Client, author: User):
    url = reverse("users:delete", args=[author.pk])
    response = author_client.post(url)
    assertRedirects(
        response=response,
        expected_url=reverse("users:list"),
        status_code=HTTPStatus.FOUND,
    )
    assert not User.objects.filter(pk=author.pk).exists()


@pytest.mark.parametrize("url_name", ("users:update", "users:delete"))
def test_anonymous_edit_failure(
    client: Client,
    author: User,
    url_name: str,
    author_form_data,
):
    url = reverse(url_name, args=[author.pk])
    response = client.post(url, data=author_form_data)
    assertRedirects(
        response=response,
        expected_url=reverse("login"),
        status_code=HTTPStatus.FOUND,
    )
    author.refresh_from_db()
    assert author.first_name == "John"


@pytest.mark.parametrize("url_name", ("users:update", "users:delete"))
def test_another_user_edit_failure(
    another_user_client: Client,
    author: User,
    url_name: str,
    author_form_data,
):
    url = reverse(url_name, args=[author.pk])
    author_form_data["first_name"] = "Michael"
    response = another_user_client.post(url, data=author_form_data)
    assertRedirects(
        response=response,
        expected_url=reverse("users:list"),
        status_code=HTTPStatus.FOUND,
    )
    author.refresh_from_db()
    assert author.first_name == "John"
