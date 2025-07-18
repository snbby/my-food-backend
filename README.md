# MyFood Backend

This repository contains the backend for **MyFood**, a small experiment written in [Django](https://www.djangoproject.com/) and [Django Ninja](https://django-ninja.rest-framework.com/). It exposes a simple API that allows searching for food products sourced from the [OpenFood Facts](https://world.openfoodfacts.org/) database.

The project demonstrates how to build a lightweight REST API, run background tasks with custom Django management commands and orchestrate everything with Docker.

## Features

- **Python 3.13, Django 5** and **Django Ninja** for fast API development.
- PostgreSQL database with models for storing food products and server health statistics.
- Management commands to:
  - download and import the OpenFood Facts product dataset (`food_to_db`).
  - record basic server statistics such as disk and memory usage (`server_health`).
  - generate a sitemap file based on the most common product and brand names (`sitemap`).
- Test suite using `pytest` and `factory-boy` (see `myfood/tests/`).
- Dockerfiles plus a `docker-compose.yaml` that spin up the Django server,
  periodic management tasks and a [Caddy](https://caddyserver.com/) reverse
  proxy.
- GitHub Actions workflow for automatically building images and deploying the
  stack on the production machine.

## Local setup

1. Clone the repository and create a `.env` file with the required settings (see
   the environment variables in `.github/workflows/deploy-prod.yaml`).
2. Build the containers and start the entire stack (server, management workers
   and Caddy):

   ```bash
   docker compose build
   docker compose up
   ```

3. Once running, Caddy proxies `http://localhost` to the Django service. The API
   is available at `http://localhost:8000/api/` and the admin at
   `http://localhost:8000/admin/`.

### Running the tests

Install the Python dependencies and execute the tests:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

If `pytest` fails with `ModuleNotFoundError: No module named 'django'`, make sure
the dependencies above were installed or run the tests inside the Docker
container with `docker compose run server pytest`.

## API overview

The main endpoints are defined in `myfood/api.py` and include:

- `/api/foodproducts/search/` – unauthenticated search with pagination.
- `/api/foodproducts/search_detailed/` – authenticated search returning additional nutritional fields.

Both endpoints support a `q` query parameter to filter by product name.

## Management commands

- `python manage.py food_to_db` – fetches the OpenFood Facts CSV, processes it and stores products in the database.
- `python manage.py server_health` – captures CPU load and memory statistics into the `ModelServerHealth` table.
- `python manage.py sitemap` – creates a simple sitemap file under `artifacts/myfood/`.

These commands run in dedicated Docker images defined in the `deploy/` directory.

## Deployment

`docker-compose.yaml` defines the complete production stack:

- `server` – the Django application served with Gunicorn.
- `caddy` – reverse proxy that terminates TLS and serves the collected static files.
- `cmd_migrations`, `cmd_food_to_db` and `cmd_server_health` – one-off containers for
  management commands.

The GitHub Actions workflow at `.github/workflows/deploy-prod.yaml` builds these
images and, using a self-hosted runner, recreates the containers on the server.
This keeps deployments reproducible and removes manual steps.

## Inspiration

This codebase started as an experiment for learning Django Ninja, handling large CSV imports and automating deployments with Docker and GitHub Actions. Although it is a small project, it shows how I organise code, write tests and containerise a Python service.

