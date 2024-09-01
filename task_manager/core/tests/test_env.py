def test_project_has_app():
    """
    Project has "task_manager" package.
    ALLOWED_HOSTS has "webserver".
    """
    try:
        from task_manager import settings

        assert "webserver" in settings.ALLOWED_HOSTS

    except ImportError:
        assert False, "Failed to import 'settings' from 'task_manager'."
