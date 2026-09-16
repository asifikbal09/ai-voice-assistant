from fastapi import APIRouter, HTTPException

from app.modules.assistant.schemas import ChatRequest, ChatResponse
from app.modules.assistant.service import chat


router = APIRouter(
    prefix="/assistant",
    tags=["Assistant"],
)


@router.post("/chat")
async def chat_service(request: ChatRequest):
    return await chat(
        session_id=request.session_id,
        message=request.message,
    )