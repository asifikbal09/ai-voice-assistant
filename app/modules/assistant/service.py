from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.assistant.agent import generate_ai_response
from app.modules.conversation.database_service import (
    save_message,
)
from app.modules.conversation.history import (
    get_conversation_history_from_db,
)


async def chat(
    db: AsyncSession,
    session_id: str,
    message: str,
):

    conversation, history = await get_conversation_history_from_db(
        db=db,
        session_id=session_id,
    )

    response = await generate_ai_response(
        user_message=message,
        session_id=session_id,
        history=history,
    )

    await save_message(
        db=db,
        conversation=conversation,
        role="user",
        content=message,
    )

    await save_message(
        db=db,
        conversation=conversation,
        role="assistant",
        content=response,
    )

    return {
        "success": True,
        "message": message,
        "response": response,
    }