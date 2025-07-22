# FastAPI service

This service exposes a single paginated search endpoint

```
GET /api/foodproducts/search/?q=<name>&limit=<n>&offset=<n>
```

Swagger documentation available at:
```
GET /docs
```

The application expects environment variables:
```
MYFOOD_DATABASE_HOST: postgres # for docker installation
MYFOOD_DATABASE_PORT: 5432
MYFOOD_DATABASE_NAME: <db_name>
MYFOOD_DATABASE_USER: <user>
MYFOOD_DATABASE_PASS: <pass>
```
With docker deployment application is available under port 8001