build:
	./build.sh

lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix

test:
	uv run pytest --ds=task_manager.settings --reuse-db

install:
	uv sync

migrate:
	uv run python manage.py makemigrations
	uv run python manage.py migrate

collectstatic:
	uv run python manage.py collectstatic --no-input

dev:
	uv run python manage.py runserver

start:
	uv run gunicorn -w 5 task_manager.wsgi

render-start:
	gunicorn task_manager.wsgi