from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.database import engine, SessionLocal

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Extract tenant ID from a custom header (e.g., X-Tenant-ID)
        tenant_id = request.headers.get("X-Tenant-ID")

        # Validate tenant
        if not tenant_id or tenant_id not in ["tenant1", "tenant2"]:
            raise HTTPException(status_code=400, detail="Invalid or missing tenant ID")

        # Configure schema mapping for the tenant
        schema_engine = engine.execution_options(schema_translate_map={None: tenant_id})
        tenant_session = sessionmaker(
            bind=schema_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

        # Attach the session to the request
        request.state.db = tenant_session()

        # Proceed with the request
        try:
            response = await call_next(request)
        finally:
            # Ensure the session is closed after the request
            await request.state.db.close()

        return response
