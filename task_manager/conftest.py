from django.core.management import call_command
from django.contrib.auth import get_user_model, models
from django.db.models import QuerySet
from django.test import Client
import pytest

from task_manager.core.consts import TEST_FIXTURE_PATH

User: models.AbstractBaseUser = get_user_model()


@pytest.fixture(autouse=True)
def django_db(db):
    """Auto add django DB."""
    pass


@pytest.fixture
def users() -> QuerySet[models.AbstractBaseUser]:
    """Loads the user fixtures for the project."""
    call_command('loaddata', TEST_FIXTURE_PATH / "user.json")
    return get_user_model().objects.all()


@pytest.fixture
def author_client(users: QuerySet[models.AbstractBaseUser]) -> Client:
    """Creates client and makes author user logging in."""
    author = users.first()
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def another_user_client(users: QuerySet[models.AbstractBaseUser]) -> Client:
    """Creates client and makes non author user logging in."""
    another_user = users.last()
    client = Client()
    client.force_login(another_user)
    return client
