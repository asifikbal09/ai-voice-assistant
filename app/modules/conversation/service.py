from app.modules.conversation.memory import conversation_memory


def get_conversation_history(session_id: str):
    return conversation_memory.get_history(session_id)


def clear_conversation(session_id: str):
    conversation_memory.clear_session(session_id)

    return {
        "success": True,
        "session_id": session_id,
        "message": "Conversation cleared successfully.",
    }