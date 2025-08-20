build:
	./build.sh

lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix

install:
	uv sync

migrate:

collectstatic:

dev:
	uv run python manage.py runserver

start:
	uv run gunicorn -w 5 task_manager.wsgi

render-start:
	gunicorn task_manager.wsgi