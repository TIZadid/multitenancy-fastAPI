
# Multi-Tenant FastAPI Project

This project demonstrates schema-based multi-tenancy using PostgreSQL with two types of tenant identification: 
1. **Header-Based Tenant Identification**
2. **Subdomain-Based Tenant Identification**

And two methods for implementing these identifications:
- **Middleware**
- **Dependency Injection**

## Key Commands to Run the Project

1. **Install Dependencies**:
    ```bash
    poetry install
    ```

2. **Run PostgreSQL and Apply Migrations**:
    ```bash
    docker compose up -d
    docker compose run flyway migrate
    ```

3. **Start the FastAPI Application**:
    ```bash
    python app/main.py
    ```

4. **Configure /etc/hosts for Subdomain Testing**:
    Add the following lines to your `/etc/hosts` file:
    ```plaintext
    127.0.0.1 tenant1.localhost.com
    127.0.0.1 tenant2.localhost.com
    ```
    This allows testing subdomain routing locally by mapping the custom subdomains to localhost.

## Approaches to Multi-Tenancy

Both the Header-Based and Subdomain-Based tenant identification types can be implemented using either Middleware or Dependency Injection methods. In this project, the following combinations are used as examples:

- **routes_dependancy.py**: Implements Subdomain-Based Tenant Identification using Dependency Injection.
- **routes.py**: Implements Header-Based Tenant Identification using Middleware.

### 1. Header-Based Tenant Identification (Middleware)

The `TenantMiddleware` class dynamically sets the database schema based on the `X-Tenant-ID` header.

#### Code Overview:
```python
class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        tenant_id = request.headers.get("X-Tenant-ID")
        if not tenant_id or tenant_id not in ["tenant1", "tenant2"]:
            raise HTTPException(status_code=400, detail="Invalid or missing tenant ID")

        schema_engine = engine.execution_options(schema_translate_map={None: tenant_id})
        tenant_session = sessionmaker(bind=schema_engine, class_=AsyncSession, expire_on_commit=False)
        request.state.db = tenant_session()

        try:
            response = await call_next(request)
        finally:
            await request.state.db.close()

        return response
```

#### How It Works:
- Extracts the tenant ID from the `X-Tenant-ID` header.
- Validates the tenant ID and configures the database engine to use the corresponding schema.
- Attaches the tenant-specific session to `request.state.db`.
- Ensures the session is closed after the request is processed.

#### Example cURL Request:
```bash
curl -X GET http://localhost:8000/items/ -H "X-Tenant-ID: tenant1"
```

### 2. Subdomain-Based Tenant Identification (Dependency Injection)

The `get_tenant_db_subdomain` function dynamically sets the database schema based on the subdomain in the URL.

#### Code Overview:
```python
async def get_tenant_db_subdomain(request: Request):
    host = request.headers.get("host")
    subdomain = host.split(".")[0] if host else None

    if subdomain not in ["tenant1", "tenant2"]:
        raise HTTPException(status_code=400, detail="Invalid tenant")

    schema_engine = engine.execution_options(schema_translate_map={None: subdomain})

    async with SessionLocal(bind=schema_engine) as session:
        yield session
```

#### How It Works:
- Extracts the subdomain from the `Host` header in the request.
- Validates the subdomain and configures the database engine for the corresponding schema.
- Returns a session specific to the tenant schema.

#### Example cURL Request:
```bash
curl -X GET http://tenant1.localhost.com:8000/items/
```

## Directory Structure

- `app/` - Contains FastAPI application code.
- `db/migrations/` - Flyway migration files.
- `docker-compose.yml` - Docker setup for PostgreSQL and Flyway.

## Additional Notes

- Ensure Docker and Poetry are installed on your system.
- Test subdomain routing locally by correctly configuring `/etc/hosts`.
