from langchain_groq import ChatGroq

from app.core.config import settings
from app.modules.assistant.prompts import ASSISTANT_SYSTEM_PROMPT


def get_llm() -> ChatGroq:
    if not settings.groq_api_key:
        raise ValueError("GROQ_API_KEY is not configured.")

    if not settings.groq_model:
        raise ValueError("GROQ_MODEL is not configured.")

    return ChatGroq(
        model=settings.groq_model,
        api_key=settings.groq_api_key,
        temperature=0.2,
    )


async def generate_ai_response(user_message: str) -> str:
    llm = get_llm()

    messages = [
        (
            "system",
            ASSISTANT_SYSTEM_PROMPT,
        ),
        (
            "human",
            user_message,
        ),
    ]

    response = await llm.ainvoke(messages)

    return response.content