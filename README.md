
# Multi-Tenant FastAPI Project

This repository contains a FastAPI project that implements schema-based multi-tenancy using PostgreSQL. Each tenant's data is isolated within its own schema, identified by subdomains (e.g., `tenant1.localhost.com/items`). Flyway is used for managing database migrations, and Docker is used to set up PostgreSQL and Flyway. The FastAPI application itself runs outside of Docker.

## Features

- **Multi-Tenancy**: Tenant data is isolated in separate schemas within PostgreSQL.
- **Subdomain-Based Tenant Identification**: Routes are configured based on subdomains, allowing tenants to be dynamically identified.
- **Data Migration**: Managed with Flyway to ensure schemas are up-to-date.

## Prerequisites

- [Docker](https://www.docker.com/)
- [Python 3.10+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/) for dependency management

## Setup and Running the Application

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo
```

### Step 2: Set Up Docker for PostgreSQL and Flyway

1. **Run PostgreSQL and Flyway with Docker Compose**:
    ```bash
    docker compose up -d
    ```
   This command initializes PostgreSQL and Flyway containers.

2. **Database Migration with Flyway**:
    ```bash
    docker compose run flyway migrate
    ```
   This command applies all pending migrations to your PostgreSQL database.

### Step 3: Configure `/etc/hosts` for Local Testing

To enable subdomain-based routing for tenant identification on localhost, add the following to your `/etc/hosts` file:

```plaintext
127.0.0.1 tenant1.localhost.com
127.0.0.1 tenant2.localhost.com
# Add more tenants as needed
```

### Step 4: Install Dependencies

Use Poetry to install the project dependencies:


```bash
poetry install
```

### Step 5: Run the FastAPI Application

With Docker running PostgreSQL and migrations applied, start the FastAPI application by running the main function in main.py,

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The application is now accessible. For example:
- `http://tenant1.localhost.com:8000/items` to access items for `tenant1`.
- `http://tenant2.localhost.com:8000/items` to access items for `tenant2`.

## Directory Structure

- `app/` - Contains FastAPI application code.
- `db/migrations/` - Flyway migration files.
- `docker-compose.yml` - Docker setup for PostgreSQL and Flyway.

## Additional Notes

- **Database Migrations**: Create new Flyway migration scripts in the `db/migrations` folder following Flyway’s naming conventions.
- **Testing**: Ensure `/etc/hosts` is correctly configured for each tenant subdomain.


