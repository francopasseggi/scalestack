# Instructions to run project locally

1. Crete a .env file at the root dir with the following variables

```
# For the api container
DJANGO_SECRET_KEY
DJANGO_DEBUG
DJANGO_ALLOWED_HOSTS
DATABASE_URL=postgres://<POSTGRES_USER>:<POSTGRES_PASSWORD>@db:<POSTGRES_PORT>/<POSTGRES_DB>

# For the db container
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB
POSTGRES_PORT

# AWS Configuration
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_DEFAULT_REGION
```

2. Use dev containers to spin up api, db and lambda
3. Run `make migrate` and `make runserver` inside the api container
4. Interact with the api through the docs (localhost:8000/api/docs)


## Lambda Function

To test the lambda function, run `make lambda` inside the api container 