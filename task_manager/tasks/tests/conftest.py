from django.core.management import call_command
from django.db.models import QuerySet
import pytest

from task_manager.core.consts import TEST_FIXTURE_PATH
from task_manager.tasks.models import Task


@pytest.fixture
def tasks(users) -> QuerySet[Task]:
    """Loads the status fixtures for the project."""
    call_command('loaddata', TEST_FIXTURE_PATH / "label.json")
    call_command('loaddata', TEST_FIXTURE_PATH / "status.json")
    call_command('loaddata', TEST_FIXTURE_PATH / "task.json")
    return Task.objects.all()
