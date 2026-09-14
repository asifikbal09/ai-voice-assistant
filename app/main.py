from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.modules.assistant.router import router as assistant_router


app = FastAPI(
    title=settings.app_name,
    description="AI Voice Customer Assistant for Premium Design Consultancy",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    assistant_router,
    prefix=settings.api_prefix,
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