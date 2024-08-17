import pytest
from django.urls import reverse
from http import HTTPStatus
from django.test import Client
from django.http import HttpResponse
from pytest_django.asserts import assertRedirects

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import TaskLabel


@pytest.mark.django_db
def test_label_form_success(author_client: Client):
    """User can create a new label using Label Form."""
    url: str = reverse("labels:create")
    form_data = {"name": "Test Label"}

    form = LabelForm(data=form_data)
    assert form.is_valid(), form.errors

    response: HttpResponse = author_client.post(url, form.cleaned_data)
    assertRedirects(response, reverse("labels:list"), HTTPStatus.FOUND)

    assert TaskLabel.objects.filter(**form_data).exists()


@pytest.mark.django_db
def test_label_form_invalid_data_failure(author_client: Client):
    """User can't create a new label using Label Form with invalid data."""
    url: str = reverse("labels:create")
    form_data = {"name": ""}

    form = LabelForm(data=form_data)
    assert not form.is_valid()

    response: HttpResponse = author_client.post(url, form_data)
    assert 'name' in response.context['form'].errors
    assert not TaskLabel.objects.filter(**form_data).exists()
