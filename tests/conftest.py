import pytest
from django.test import Client

from users.models import User
from statuses.models import TaskStatus
from labels.models import TaskLabel
from tasks.models import Task


@pytest.fixture(autouse=True)
def django_db(db):
    pass


@pytest.fixture
def author_form_data():
    return {
        "username": "author_user",
        "first_name": "John",
        "last_name": "Doe",
        "password1": "password",
        "password2": "password",
    }


@pytest.fixture
def another_user_form_data():
    return {
        "username": "another_user",
        "first_name": "Hello",
        "last_name": "World",
        "password1": "password",
        "password2": "password",
    }


@pytest.fixture
def author():
    return User.objects.create_user(
        username="author_user",
        first_name="John",
        last_name="Doe",
        password="password",
    )


@pytest.fixture
def another_user():
    return User.objects.create_user(
        username="another_user",
        first_name="Hello",
        last_name="World",
        password="password",
    )


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def another_user_client(another_user):
    client = Client()
    client.force_login(another_user)
    return client


@pytest.fixture
def task_status():
    return TaskStatus.objects.create(name="Test Status")


@pytest.fixture
def task_label():
    return TaskLabel.objects.create(name="Test Label")


@pytest.fixture
def task(author, task_status, another_user, task_label):
    new_task = Task.objects.create(
        name="Test Task",
        status=task_status,
        author=author,
        executor=another_user,
    )
    new_task.labels.add(task_label)

    return new_task
