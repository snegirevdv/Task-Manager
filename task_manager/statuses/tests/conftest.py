from django.core.management import call_command
from django.db.models import QuerySet
import pytest

from task_manager.core.consts import TEST_FIXTURE_PATH
from task_manager.statuses.models import TaskStatus


@pytest.fixture
def statuses() -> QuerySet[TaskStatus]:
    """Loads and returns the status fixtures for the project."""
    call_command("loaddata", TEST_FIXTURE_PATH / "status.json")
    return TaskStatus.objects.all()
