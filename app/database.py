from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi import Request, HTTPException
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the database URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")  # No default value, will raise an error if not set

# Create the async engine
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set in the environment variables.")

engine = create_async_engine(DATABASE_URL, echo=True)

# Create the async sessionmaker
SessionLocal = sessionmaker(
    expire_on_commit=False,
    class_=AsyncSession  # Ensure the session is async
)

# Base for models
Base = declarative_base()

# Middleware to inject tenant schema from subdomain
async def get_tenant_db_subdomain(request: Request):
    host = request.headers.get("host")
    subdomain = host.split(".")[0] if host else None

    if subdomain not in ["tenant1", "tenant2"]:
        raise HTTPException(status_code=400, detail="Invalid tenant")

    schema_engine = engine.execution_options(schema_translate_map={None: subdomain})

    async with SessionLocal(bind=schema_engine) as session:
        yield session



# Dependency to provide the session
async def get_db_session_header(request: Request) -> AsyncSession:
    # Extract tenant ID from the header
    tenant_id = request.headers.get("X-Tenant-ID")
    if not tenant_id or tenant_id not in ["tenant1", "tenant2"]:
        raise HTTPException(status_code=400, detail="Invalid or missing tenant ID")

    # Configure schema mapping for the tenant
    schema_engine = engine.execution_options(schema_translate_map={None: tenant_id})

    async with SessionLocal(bind=schema_engine) as session:
        yield session

