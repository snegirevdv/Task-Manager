run:
	poetry run python3 manage.py runserver

locale-create:
	poetry run django-admin makemessages -l ru
	poetry run django-admin makemessages -l en

locale-compile:
	poetry run django-admin compilemessages

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

build:
	poetry install
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

start:
	poetry run gunicorn task_manager.wsgi:application --bind 0.0.0.0:$PORT
