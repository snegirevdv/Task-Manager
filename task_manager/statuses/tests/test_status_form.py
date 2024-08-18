from http import HTTPStatus

from django.urls import reverse
from django.test import Client
from django.http import HttpResponse
import pytest
from pytest_django.asserts import assertRedirects

from task_manager.core.tests import consts
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import TaskStatus


@pytest.mark.django_db
def test_status_form_success(author_client: Client):
    """User can create a new status using Label Form."""
    url: str = reverse("statuses:create")
    form_data = consts.FormData.STATUS_VALID

    form = StatusForm(data=form_data)
    assert form.is_valid(), form.errors

    response: HttpResponse = author_client.post(url, form.cleaned_data)
    assertRedirects(response, reverse("statuses:list"), HTTPStatus.FOUND)

    assert TaskStatus.objects.filter(**form_data).exists()


@pytest.mark.django_db
def test_status_form_invalid_data_failure(author_client: Client):
    """User can't create a new status using Label Form with invalid data."""
    url: str = reverse("statuses:create")
    form_data = consts.FormData.STATUS_INVALID

    form = StatusForm(data=form_data)
    assert not form.is_valid()

    author_client.post(url, form_data)
    assert "name" in form.errors
    assert not TaskStatus.objects.filter(**form_data).exists()
