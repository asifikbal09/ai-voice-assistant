from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db
from app.modules.conversation.database_service import (
    get_messages,
    get_or_create_conversation,
    save_message,
)
from app.modules.conversation.service import (
    clear_conversation,
    get_conversation_history,
)
from app.modules.conversation.shemas import ConversationHistoryResponse

router = APIRouter(
    prefix="/conversation",
    tags=["Conversation"],
)


@router.get("/{session_id}")
async def conversation_history(
    session_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
):

    messages = await get_conversation_history(
        db=db,
        session_id=session_id,
    )

    return {
        "success": True,
        "session_id": session_id,
        "messages": [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in messages
        ],
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
@router.post("/database-test/{session_id}")
async def database_test(
    session_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    conversation = await get_or_create_conversation(
        db=db,
        session_id=session_id,
    )

    await save_message(
        db=db,
        conversation=conversation,
        role="user",
        content="Hello, this is a database test.",
    )

    await save_message(
        db=db,
        conversation=conversation,
        role="assistant",
        content="Hello! Your PostgreSQL conversation storage is working.",
    )

    messages = await get_messages(
        db=db,
        conversation=conversation,
        limit=10,
    )

    return {
        "success": True,
        "session_id": session_id,
        "conversation_id": str(conversation.id),
        "messages": [
            {
                "id": str(message.id),
                "role": message.role,
                "content": message.content,
            }
            for message in messages
        ],
    }