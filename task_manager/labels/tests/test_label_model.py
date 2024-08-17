import datetime
from django.db import IntegrityError
import pytest
from task_manager.labels.models import TaskLabel
from django.db.models import QuerySet


def test_label_creation_success():
    """Label can be successfully created."""
    label = TaskLabel.objects.create(name="Test Label")
    assert TaskLabel.objects.filter(name="Test Label").exists()
    assert label.name == "Test Label"
    assert label.created_at.year == datetime.datetime.now().year


def test_label_update_success(labels: QuerySet[TaskLabel]):
    """Label can be successfully updated."""
    label = labels.first()
    label.name = "Updated Label"
    label.save()

    updated_label = TaskLabel.objects.get(pk=label.pk)
    assert updated_label.name == "Updated Label"


def test_label_deletion_success(labels: QuerySet[TaskLabel]):
    """Label can be successfully updated."""
    label = labels.first()
    label_pk = label.pk
    label.delete()

    assert not TaskLabel.objects.filter(pk=label_pk).exists()


def test_label_creation_failure():
    """Labels with a duplicate name can't be created."""
    with pytest.raises(IntegrityError):
        TaskLabel.objects.create(name="Unique Label")
        TaskLabel.objects.create(name="Unique Label")
