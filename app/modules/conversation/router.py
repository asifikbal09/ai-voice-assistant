from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db
from app.modules.conversation.service import (
    clear_conversation,
    get_conversation_history,
)
from app.modules.conversation.shemas import ConversationHistoryResponse

router = APIRouter(
    prefix="/conversation",
    tags=["Conversation"],
)


@router.get(
    "/{session_id}",
    response_model=ConversationHistoryResponse,
)
async def conversation_history(session_id: str):
    messages = get_conversation_history(session_id)

    return {
        "success": True,
        "session_id": session_id,
        "messages": messages,
    }


@router.delete("/{session_id}")
async def delete_conversation(session_id: str):
    return clear_conversation(session_id)


@router.get("/database-health")
async def database_health(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(text("SELECT 1"))

    return {
        "success": True,
        "database": result.scalar(),
    }
