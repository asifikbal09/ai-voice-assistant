from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    description="AI Voice Customer Assistant for Premium Design Consultancy",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "success": True,
        "message": "Premium Voice Assistant API is running.",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "environment": settings.app_env,
    }