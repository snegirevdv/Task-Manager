from django.db import connection


def test_db_table_creation_success():
    tables = [
        "labels_tasklabel",
        "statuses_taskstatus",
        "tasks_task",
        "tasks_tasklabelrelation",
        "users_user",
    ]

    with connection.cursor() as cursor:
        for table_name in tables:
            try:
                cursor.execute(f"SELECT * FROM {table_name};")
            except Exception as e:
                assert False, str(e)
