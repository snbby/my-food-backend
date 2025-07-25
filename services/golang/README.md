# Golang service

This service exposes a single paginated search endpoint using the same
`FoodProduct` model as the FastAPI implementation.

```
GET /api/foodproducts/search/?q=<name>&limit=<n>&offset=<n>
```
The application expects environment variables:
```
MYFOOD_DATABASE_HOST: postgres # for docker installation
MYFOOD_DATABASE_PORT: 5432
MYFOOD_DATABASE_NAME: <db_name>
MYFOOD_DATABASE_USER: <user>
MYFOOD_DATABASE_PASS: <pass>
```

With docker deployment application is available under port 8002
