from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi import Request, HTTPException

import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://fastapi_user:123456@db:5432/fastapi_db")

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create the async sessionmaker
SessionLocal = sessionmaker(
    expire_on_commit=False,
    class_=AsyncSession  # Ensure the session is async
)

# Base for models
Base = declarative_base()

# Middleware to inject tenant schema from subdomain
async def get_tenant_db(request: Request):
    # Extract the tenant from the subdomain (e.g., tenant1.localhost:8000)
    host = request.headers.get("host")
    subdomain = host.split(".")[0] if host else None  # Extracts tenant1 from tenant1.localhost

    if subdomain not in ["tenant1", "tenant2"]:
        raise HTTPException(status_code=400, detail="Invalid tenant")

    # Create an engine with tenant-specific schema
    schema_engine = engine.execution_options(schema_translate_map={None: subdomain})

    # Create a session with the tenant-specific engine
    async with SessionLocal(bind=schema_engine) as session:
        yield session