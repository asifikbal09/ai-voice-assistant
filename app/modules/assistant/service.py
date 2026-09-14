from app.modules.assistant.agent import generate_ai_response


async def chat_with_assistant(user_message: str) -> str:
    response = await generate_ai_response(user_message)

    return response