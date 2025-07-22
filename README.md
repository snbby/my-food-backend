# MyFood Backend

This repository contains the backend for **MyFood**, a collection of small services built with different technologies. It includes:

- a **Django** project under `services/django`;
- a **FastAPI** project under `services/fastapi`;
- a **Golang** service using the Gin framework under `services/golang`.

All of them expose a search endpoint for food products, populated with fake data sourced from the [OpenFood Facts](https://world.openfoodfacts.org/) dataset.

The project demonstrates how to build lightweight REST APIs, run background tasks with custom Django management commands and orchestrate everything with Docker

## Features

- **Python 3.13, Django 5 + DRF, FastAPI and Golang Gin** for fast API development.
- PostgreSQL database with models for storing food products.
- Test suite using `pytest` and `factory-boy` (see `services/django/myfood/tests/`).
- Docker Compose orchestrates the server container, scheduled job images and a Caddy reverse proxy.
- Caddy acts as a reverse proxy and serves static files over HTTPS.
- GitHub Actions workflow automatically builds images and redeploys them to the production server.
- FastAPI and Golang Gin services replicate the main search endpoint.
- Database migrations are performed through the Django ORM.
- Focus on CI/CD best practices with all services deployed in Docker containers.

## API overview
The main endpoints for the Django service are defined in `services/django/myfood/api.py` and include:

- `/api/foodproducts/search/` – unauthenticated search with pagination.
- `/api/foodproducts/search_detailed/` – authenticated search returning additional nutritional fields.

Both endpoints support a `q` query parameter to filter by product name. When deployed the public URLs are:

- `https://django.my-food.com/api/foodproducts/search/`
- `https://django.my-food.com/api/foodproducts/search_detailed/`

The FastAPI (`services/fastapi`) and Golang (`services/golang`) apps expose the same search functionality at:

- `https://fastapi.my-food.com/api/foodproducts/search/`
- `https://golang.my-food.com/api/foodproducts/search/`

## Deployment

The service is deployed using a combination of Docker Compose and GitHub Actions.
`docker-compose.yaml` defines the application container, Caddy and the background command images. Caddy handles HTTPS certificates and proxies requests to the Django server while serving static files.

The workflow `.github/workflows/deploy-prod.yaml` runs on a remote runner. It builds new images, stores environment variables in a `.env` file, runs database migrations and finally restarts the stack with `docker compose up --detach django fastapi golang caddy`.

## Local setup

1. Clone the repository and create a `.env` file with environment variables:
```bash
MYFOOD_DATABASE_HOST: postgres # For docker installation
MYFOOD_DATABASE_PORT: 5432
MYFOOD_DATABASE_NAME: <db_name>
MYFOOD_DATABASE_USER: <user>
MYFOOD_DATABASE_PASS: <pass>
MYFOOD_DEBUG: <True|False> # For Django service
MYFOOD_DJANGO_SECRET_KEY: <secret_key> # For Django service
```
2. Build the containers and start the stack:

```bash
docker compose up --build django fastapi golang postgres
```

3. The API will be available at:

http://localhost:8000/api/foodproducts/search/ (Django DRF)
http://localhost:8001/api/foodproducts/search/ (FastAPI)
http://localhost:8002/api/foodproducts/search/ (Golang GIN)  
http://localhost:8000/admin/ (Django admin)
