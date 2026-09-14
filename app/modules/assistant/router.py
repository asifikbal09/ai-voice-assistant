from fastapi import APIRouter, HTTPException

from app.modules.assistant.schemas import ChatRequest, ChatResponse
from app.modules.assistant.service import chat_with_assistant


router = APIRouter(
    prefix="/assistant",
    tags=["Assistant"],
)


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = await chat_with_assistant(request.message)

        return ChatResponse(
            success=True,
            message="Assistant response generated successfully.",
            response=response,
        )

    except (ValueError, TypeError) as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )