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
- Docker Compose orchestrates the server container, scheduled job images and a Caddy reverse proxy.
- Caddy acts as a reverse proxy and serves static files over HTTPS.
- GitHub Actions workflow automatically builds images and redeploys them to the production server.

## Local setup

1. Clone the repository and create a `.env` file with the required settings (see the environment variables in `.github/workflows/deploy-prod.yaml`).
2. Build the containers and start the stack:

   ```bash
   docker compose build
   docker compose up
   ```

3. The API will be available at `http://localhost:8000/api/` and the Django admin at `http://localhost:8000/admin/`.

### Running the tests

Install the dependencies first:

```bash
pip install -r requirements.txt
```

Then execute:

```bash
pytest
```

If `pytest` fails complaining that Django is missing, ensure you installed the packages above or run the tests inside the Docker container with:

```bash
docker compose run --rm server pytest
```

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

The service is deployed using a combination of Docker Compose and GitHub Actions.
`docker-compose.yaml` defines the application container, Caddy and the background command images. Caddy handles HTTPS certificates and proxies requests to the Django server while serving static files.

The workflow `.github/workflows/deploy-prod.yaml` runs on a remote runner. It builds new images, stores environment variables in a `.env` file, runs database migrations and finally restarts the stack with `docker compose up --detach server caddy`.

## Inspiration

This codebase started as an experiment for learning Django Ninja, handling large CSV imports and automating deployments with Docker and GitHub Actions. Although it is a small project, it shows how I organise code, write tests and containerise a Python service.

