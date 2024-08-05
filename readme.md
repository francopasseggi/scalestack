# Project Features

- Project hosted in AWS. Containers are pushed to ECR. 
- The API is run using AppRunner, and can be accessed here: https://miuqehzpzg.us-east-1.awsapprunner.com/.
- Postgres DB provided by AWS.
- Lambda functions are run using containers uploaded to ECR. The function uses asyncio to make requests in parallel.
- Dev container set up for instant local development.
- Pytest based testing.

## Access project

https://miuqehzpzg.us-east-1.awsapprunner.com/

The api docs are interactive, so you can test the endpoints right there.

# Instructions to run project locally with dev containers

We provide a `docker-compose.yml` file for quick setup of the development environment. This includes all necessary services:

- Django application
- PostgreSQL database
- Lambda (for local testing)

To set up and start the development environment:

1. Install Prerequisites:
   - Docker with Docker Compose
   - Visual Studio Code
   - VSCode extensions: "Dev Containers" and "Docker"

2. Create a `.env` file in the root directory of the project with the following content:

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

3. Open the project in Visual Studio Code.

4. Press `Cmd + Shift + P` (on macOS) or `Ctrl + Shift + P` (on Windows/Linux) to open the command palette.

5. Type "Dev Containers: Open Folder in Container" and select it.

6. Wait for the containers to be built and started. This may take a few minutes the first time.

7. Once the Dev Container is ready, open a new terminal in VS Code.

8. Run the following commands to set up the database and run the dev server:

   ```bash
   make migrate
   make runserver
   ```

9. The application should now be running. You can access `http://0.0.0.0:8000/` to interact with the API.

10. To test the lambda function, run `make lambda` inside the api container 