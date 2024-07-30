import pytest
from users.models import User
from django.test import Client


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
