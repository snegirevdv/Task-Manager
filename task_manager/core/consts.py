from enum import Enum
from pathlib import Path

from django.utils.translation import gettext_lazy as _

NAME_MAX_LENGTH = 100
TEST_FIXTURE_PATH = Path("task_manager/core/tests/fixtures/")


class Template(Enum):
    """Template file paths."""

    INDEX = "index.html"
    LOGIN = "users/login.html"
    LABEL_LIST = "labels/list.html"
    LABEL_CREATE_UPDATE = "labels/create_update.html"
    LABEL_DELETE = "labels/delete.html"
    STATUS_LIST = "statuses/list.html"
    STATUS_CREATE_UPDATE = "statuses/create_update.html"
    STATUS_DELETE = "statuses/delete.html"
    TASK_LIST = "tasks/list.html"
    TASK_CREATE_UPDATE = "tasks/create_update.html"
    TASK_DELETE = "tasks/delete.html"
    TASK_DETAIL = "tasks/detail.html"
    USER_LIST = "users/list.html"
    USER_CREATE_UPDATE = "users/create_update.html"
    USER_DELETE = "users/delete.html"


class FieldList:
    """Model field lists of forms, filter and querysets."""

    BASE_FORM = ("name",)
    BASE_QUERYSET = ("pk", "name", "created_at")
    TASK_FILTER = ("status", "executor", "labels")
    TASK_FORM = BASE_FORM + ("description", "status", "executor", "labels")
    TASK_QUERYSET = BASE_QUERYSET + (
        "status__name",
        "author__first_name",
        "author__last_name",
        "executor__first_name",
        "executor__last_name",
        "labels__name",
    )
    USER_FORM = ("first_name", "last_name", "username")
    USER_QUERYSET = (
        "pk",
        "username",
        "first_name",
        "last_name",
        "date_joined",
    )


class VerboseName(Enum):
    """Model verbose names."""

    NAME = _("Name")
    CREATED_AT = _("Created at")
    LABEL = _("Label")
    LABELS = _("Labels")
    STATUS = _("Status")
    STATUSES = _("Statuses")
    TASK = _("Task")
    TASKS = _("Tasks")
    DESCRIPTION = _("Description")
    AUTHOR = _("Author")
    EXECUTOR = _("Executor")


class FormLabel(Enum):
    """Custom form labels."""

    LABEL = _("Label")
    ONLY_MINE = _("Only own tasks")


class Message(Enum):
    """Flash messages."""

    SUCCESS_LOGIN = _("You are logged in.")
    SUCCESS_LOGOUT = _("You are logged out.")
    SUCCESS_LABEL_CREATION = _("The label has been successfully created.")
    SUCCESS_LABEL_UPDATE = _("The label has been successfully updated.")
    SUCCESS_LABEL_DELETION = _("The label has been successfully deleted.")
    SUCCESS_STATUS_CREATION = _("The status has been successfully created.")
    SUCCESS_STATUS_UPDATE = _("The status has been successfully updated.")
    SUCCESS_STATUS_DELETION = _("The status has been successfully deleted.")
    SUCCESS_TASK_CREATION = _("The task has been successfully created.")
    SUCCESS_TASK_UPDATE = _("The task has been successfully updated.")
    SUCCESS_TASK_DELETION = _("The task has been successfully deleted.")
    SUCCESS_USER_CREATION = _("The user has been successfully registered.")
    SUCCESS_USER_UPDATE = _("The user has been successfully updated.")
    SUCCESS_USER_DELETION = _("The user has been successfully deleted.")

    FAILURE_NOT_AUTHORIZED = _("You are not authorized! Please log in again.")
    FAILURE_LABEL_DELETION = _(
        "The label cannot be deleted because it is in use."
    )
    FAILURE_STATUS_DELETION = _(
        "The status cannot be deleted because it is in use."
    )
    FAILURE_TASK_UPDATE = _("Only author can edit the task.")
    FAILURE_TASK_DELETE = _("Only author can delete the task.")
    FAILURE_USER_EDIT = _("You do not have permission to edit another user.")
    FAILURE_USER_DELETE = _("The user cannot be deleted because it is in use.")
