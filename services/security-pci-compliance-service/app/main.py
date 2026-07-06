import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.router import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.SERVICE_NAME}")
    yield
    logger.info(f"Shutting down {settings.SERVICE_NAME}")


app = FastAPI(title=settings.SERVICE_NAME, description=settings.SERVICE_DESCRIPTION,
              version=settings.SERVICE_VERSION, lifespan=lifespan)

app.include_router(router, prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy", "service": settings.SERVICE_NAME, "version": settings.SERVICE_VERSION}


@app.get("/ready", tags=["health"])
async def readiness_check():
    return {"status": "ready", "service": settings.SERVICE_NAME}
