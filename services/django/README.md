# Django service with DRF

This service exposes a two paginated search endpoints

```
GET /api/foodproducts/search/?q=<name>&limit=<n>&offset=<n>
GET /api/foodproducts/search_detailed/?q=<name>&limit=<n>&offset=<n>
```

Swagger documentation available at:
```
GET /api/schema/swagger-ui/
```

The application expects environment variables:
```
MYFOOD_DATABASE_HOST: postgres # for docker installation
MYFOOD_DATABASE_PORT: 5432
MYFOOD_DATABASE_NAME: <db_name>
MYFOOD_DATABASE_USER: <user>
MYFOOD_DATABASE_PASS: <pass>
MYFOOD_DEBUG: <True|False>
MYFOOD_DJANGO_SECRET_KEY: <secret_key>
```
With docker deployment application is available under port 8000