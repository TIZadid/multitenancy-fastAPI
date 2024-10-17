from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi import Request, HTTPException

import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://fastapi_user:123456@db:5432/fastapi_db")

# DATABASE_URL = "postgresql+asyncpg://fastapi_user:123456@localhost:5432/fastapi_db"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

# Middleware to inject tenant schema from request headers or other means
async def get_tenant_db(request: Request):
    tenant_id = request.headers.get("X-Tenant-ID")  # Expect tenant ID in header
    if tenant_id not in ["tenant1", "tenant2"]:
        raise HTTPException(status_code=400, detail="Invalid tenant")

    # Set schema based on tenant
    schema_engine = engine.execution_options(
        schema_translate_map={None: tenant_id}
    )
    async with sessionmaker(bind=schema_engine, class_=AsyncSession, expire_on_commit=False)() as session:
        yield session