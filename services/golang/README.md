# Golang service

This service exposes a single paginated search endpoint using the same
`FoodProduct` model as the FastAPI implementation.

```
GET /api/foodproducts/search/?q=<name>&limit=<n>&offset=<n>
```

Swagger documentation is served under `/swagger/index.html`.

The application expects the same database environment variables as the
other services and listens on port `8002`.
