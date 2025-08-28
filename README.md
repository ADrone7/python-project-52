# Task Manager
****

## Project Description

A Django-based task management system that allows users to create, track, and manage tasks with statuses and labels.
****

### Hexlet tests and linter status:
[![Actions Status](https://github.com/ADrone7/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/ADrone7/python-project-52/actions)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=ADrone7_python-project-52&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=ADrone7_python-project-52)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=ADrone7_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=ADrone7_python-project-52)
****

### Live on Render.com
https://task-manager-k227.onrender.com
****

### Technologies Used:

| Инструмент                                                                       | Описание                                                                                                                                                                                                                                                                    |
|----------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [uv](https://docs.astral.sh/uv/)                                                 | "is an extremely fast Python package manager written in Rust. It is designed as a replacement for pip and pip-tools. It can also replace venv and pyenv"                                                                                                                   |            |
| [ruff](https://docs.astral.sh/ruff/)                                             | "Your Tool For Linter and Style Guide Enforcement"                                                                                                                                                                                                                          |
| [Django](https://www.djangoproject.com/)                            | "Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design"                                                                                                        |
| [Gunicorn](https://docs.gunicorn.org/en/latest/index.html)                       | "Gunicorn ‘Green Unicorn’ is a Python WSGI HTTP Server for UNIX. It’s a pre-fork worker model ported from Ruby’s Unicorn project. The Gunicorn server is broadly compatible with various web frameworks, simply implemented, light on server resources, and fairly speedy" |
| [python-dotenv](https://pypi.org/project/python-dotenv/)                         | "Python-dotenv reads key-value pairs from a .env file and can set them as environment variables. It helps in the development of applications following the 12-factor principles"                                                                                           |
| [Bootstrap](https://getbootstrap.com/docs/5.3/getting-started/introduction/)     | "Bootstrap is a powerful, feature-packed frontend toolkit. Build anything—from prototype to production—in minutes"                                                                                                                                                         |
| [Psycopg](https://getbootstrap.com/docs/5.3/getting-started/introduction/)       | "Psycopg – PostgreSQL database adapter for Python"                                                                                                                                                                                                                          |
| [pytest](https://docs.pytest.org/en/stable/) | "The pytest framework makes it easy to write small, readable tests, and can scale to support complex functional testing for applications and libraries"                                                                                                                                                                                            |

---

## Installation

### Clone the repository:

```
git clone git@github.com:ADrone7/python-project-52.git
```

```
cd python-project-52
```

### Use the command below to install the required dependencies and generate the database tables.

```
make build
```

### Start the application with the following command:

```
make start
```