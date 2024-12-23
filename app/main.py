# main.py
import uvicorn
from fastapi import FastAPI

from app.middleware import TenantMiddleware
from route import router

app = FastAPI()
app.add_middleware(TenantMiddleware)
# Include routes from the `routes.py` file
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7700, workers=1)
