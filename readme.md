# Instructions to run project

1. Crete a .env file at the root dir with the following variables
```
DJANGO_SECRET_KEY
DJANGO_DEBUG

DJANGO_ALLOWED_HOSTS

POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB
POSTGRES_HOST
POSTGRES_PORT
```

2. Use dev containers to spin up db and api
3. Run `make runserver` inside the api container