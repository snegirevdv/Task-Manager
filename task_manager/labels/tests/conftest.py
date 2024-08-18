from django.core.management import call_command
from django.db.models import QuerySet
import pytest

from task_manager.core.consts import TEST_FIXTURE_PATH
from task_manager.labels.models import TaskLabel


@pytest.fixture
def labels() -> QuerySet[TaskLabel]:
    """Loads and returns the label fixtures for the project."""
    call_command("loaddata", TEST_FIXTURE_PATH / "label.json")
    return TaskLabel.objects.all()
