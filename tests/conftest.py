from typing import Any

import pytest
from django.test import Client

from users.models import User
from statuses.models import TaskStatus
from labels.models import TaskLabel
from tasks.models import Task


@pytest.fixture(autouse=True)
def django_db(db):
    """Auto add django DB."""
    pass


@pytest.fixture
def author_form_data() -> dict[str, str]:
    """User creating data."""
    return {
        "username": "author_user",
        "first_name": "John",
        "last_name": "Doe",
        "password1": "password",
        "password2": "password",
    }


@pytest.fixture
def task_form_data(
    task_status: TaskStatus,
    task_label: TaskLabel,
    author: User,
    another_user: User,
) -> dict[str, Any]:
    """Task creating data."""
    return {
        "name": "Test Task",
        "status": task_status.pk,
        "labels": [task_label.pk],
        "author": author.pk,
        "executor": another_user.pk,
    }


@pytest.fixture
def author() -> User:
    """Creates and returns author user object."""
    return User.objects.create_user(
        username="author_user",
        first_name="John",
        last_name="Doe",
        password="password",
    )


@pytest.fixture
def another_user() -> User:
    """Creates and returns non author user object."""
    return User.objects.create_user(
        username="another_user",
        first_name="Hello",
        last_name="World",
        password="password",
    )


@pytest.fixture
def author_client(author) -> Client:
    """Creates client and makes author user logging in."""
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def another_user_client(another_user) -> Client:
    """Creates client and makes non author user logging in."""
    client = Client()
    client.force_login(another_user)
    return client


@pytest.fixture
def task_status() -> TaskStatus:
    """Creates and returns status object."""
    return TaskStatus.objects.create(name="Test Status")


@pytest.fixture
def task_label() -> TaskLabel:
    """Creates and returns label object."""
    return TaskLabel.objects.create(name="Test Label")


@pytest.fixture
def task(author, task_status, another_user, task_label) -> Task:
    """Create and returns task object."""
    new_task = Task.objects.create(
        name="Test Task",
        status=task_status,
        author=author,
        executor=author,
    )
    new_task.labels.add(task_label)

    return new_task
