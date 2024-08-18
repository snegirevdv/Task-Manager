from http import HTTPStatus

from django.forms.utils import ErrorDict
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse

from task_manager.core.tests import consts
from task_manager.users.forms import UserForm
from task_manager.users.models import User


def test_user_form_valid_data(client: Client) -> None:
    """
    The form should successfully create a new user
    when valid data is provided.
    """
    url: str = reverse("users:create")
    data = consts.FormData.USER_VALID
    form = UserForm(data=data)
    assert form.is_valid(), form.errors

    response: HttpResponse = client.post(url, data=data)
    assert response.status_code == HTTPStatus.FOUND
    assert User.objects.filter(username=data["username"]).exists()


def test_user_form_invalid_data(client: Client) -> None:
    """The form should return errors when invalid data is provided."""
    url: str = reverse("users:create")
    data = consts.FormData.USER_INVALID

    form = UserForm(data=data)
    assert not form.is_valid()

    client.post(url, data=data)

    errors: ErrorDict = form.errors
    assert "password2" in errors
    assert "username" in errors
