from app.modules.assistant.agent import generate_ai_response


async def chat(
    session_id: str,
    message: str,
):
    response = await generate_ai_response(
        user_message=message,
        session_id=session_id,
    )

    return {
        "success": True,
        "message": message,
        "response": response,
    }