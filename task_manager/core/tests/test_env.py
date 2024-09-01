def test_project_has_app():
    """
    Project has "task_manager" package.
    """
    try:
        from task_manager import settings

        assert "localhost" in settings.ALLOWED_HOSTS

    except ImportError:
        assert False, "Failed to import 'settings' from 'task_manager'."
