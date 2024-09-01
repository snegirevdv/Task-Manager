run:
	python3 manage.py runserver

migrate:
	python3 manage.py migrate

build:
	pip install -r requirements.txt

start:
	gunicorn -w 5 -b 0.0.0.0:8001 task_manager.wsgi:application

test:
	coverage run -m pytest
	coverage xml
	coverage report
