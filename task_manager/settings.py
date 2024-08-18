import os

from django.contrib import messages
import dj_database_url
import dotenv

from pathlib import Path

dotenv.load_dotenv()

PROJECT_DIR = Path(__file__).resolve().parent
BASE_DIR = PROJECT_DIR.parent

DEBUG = True if os.getenv("ENVIRONMENT") == "development" else False

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "webserver",
    "python-django-developer-project-52.onrender.com",
]

SECRET_KEY = os.getenv("SECRET_KEY")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_bootstrap5",
    "django_filters",
    "pytest_django",
    "task_manager.labels",
    "task_manager.statuses",
    "task_manager.tasks",
    "task_manager.users",
    "task_manager.core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "rollbar.contrib.django.middleware.RollbarNotifierMiddleware",
]

ROOT_URLCONF = "task_manager.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJECT_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "task_manager.wsgi.application"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
        "OPTIONS": {
            "min_length": 3,
        },
    },
]

TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGE_CODE = "ru"

LANGUAGES = [
    ("ru", "Russian"),
]

LOCALE_PATHS = [
    os.path.join(PROJECT_DIR, "locale"),
]

STATIC_URL = "/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MESSAGE_TAGS = {
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.ERROR: "alert-danger",
}

AUTH_USER_MODEL = "users.User"


ROLLBAR = {
    "access_token": os.getenv("ROLLBAR_TOKEN"),
    "environment": os.getenv("ENVIRONMENT", "production"),
    "code_version": "1.0",
    "root": BASE_DIR,
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "format": {
            "format": "{levelname}: {name}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "django_log.log",
            "formatter": "format",
        },
    },
    "loggers": {
        "": {
            "handlers": ["file"],
            "level": "WARNING",
            "propagate": True,
        },
    },
}
