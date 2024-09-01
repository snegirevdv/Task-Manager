class Routes:
    """Route lists for route tests."""

    USERS_OPEN = [("users:create")]
    USERS_PROTECTED = [("users:update"), ("users:delete")]
    LABELS = [
        ("labels:list", False),
        ("labels:create", False),
        ("labels:update", True),
        ("labels:delete", True),
    ]
    STATUSES = [
        ("statuses:list", False),
        ("statuses:create", False),
        ("statuses:update", True),
        ("statuses:delete", True),
    ]
    TASKS = [
        ("tasks:list", False),
        ("tasks:create", False),
        ("tasks:update", True),
        ("tasks:delete", True),
        ("tasks:detail", True),
    ]


class Kwargs:
    """Kwargs for model managers in tests."""

    FIRST = {"pk": 1}
    SECOND = {"pk": 2}
    AUTHOR = {"pk": 1}
    NON_AUTHOR = {"pk": 2}


class FormData:
    """Form data for the form tests and the POST requests."""

    LABEL_VALID = {"name": "Test label"}
    LABEL_INVALID = {"name": ""}
    LABEL_UPDATE = {"name": "Updated label"}
    STATUS_VALID = {"name": "Test status"}
    STATUS_INVALID = {"name": ""}
    STATUS_UPDATE = {"name": "Updated status"}
    TASK_VALID = {
        "name": "New Test Task",
        "description": "This is a test task",
        "status": 1,
        "executor": 2,
        "labels": [1, 2],
    }
    TASK_INVALID = {
        "name": "",
    }
    TASK_UPDATE = {
        "name": "Updated Task",
        "description": "Updated description",
        "status": 1,
        "executor": 2,
    }
    USER_VALID = {
        "username": "username",
        "password1": "password",
        "password2": "password",
    }
    USER_INVALID = {
        "username": "",
        "password1": "password",
        "password2": "apssword",
    }
    USER_UPDATE = {
        "username": "updated_user",
        "password1": "password",
        "password2": "password",
    }
