from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db
from app.modules.assistant.schemas import ChatRequest, ChatResponse
from app.modules.assistant.service import chat

router = APIRouter(
    prefix="/assistant",
    tags=["Assistant"],
)


@router.post(
    "/chat",
    response_model=ChatResponse,
)
async def assistant_chat(
    request: ChatRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):

    return await chat(
        db=db,
        session_id=request.session_id,
        message=request.message,
    )
