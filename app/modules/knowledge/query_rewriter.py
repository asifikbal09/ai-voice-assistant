from langchain_groq import ChatGroq

from app.core.config import settings


QUERY_REWRITE_PROMPT = """
You rewrite customer questions into standalone search queries.

The customer may use:
- Bangla
- English
- Banglish
- Pronouns such as "এটা", "ওটা", "this", "that"
- Short follow-up questions

Use the previous conversation to understand what the customer
is referring to.

Return ONLY the rewritten standalone search query.

Do not answer the customer.
Do not add explanations.
Do not invent information.
"""


def get_query_rewriter() -> ChatGroq:
    if not settings.groq_api_key:
        raise ValueError("GROQ_API_KEY is not configured.")

    if not settings.groq_model:
        raise ValueError("GROQ_MODEL is not configured.")

    return ChatGroq(
        model=settings.groq_model,
        api_key=settings.groq_api_key,
        temperature=0,
    )


async def rewrite_query(
    user_message: str,
    history: list[dict],
) -> str:

    if not history:
        return user_message

    history_text = ""

    for message in history:
        history_text += (
            f'{message["role"].capitalize()}: '
            f'{message["content"]}\n'
        )

    prompt = f"""
Previous conversation:

{history_text}

Latest customer question:

{user_message}

Rewrite the latest question as a standalone search query.
"""

    llm = get_query_rewriter()

    response = await llm.ainvoke(
        [
            ("system", QUERY_REWRITE_PROMPT),
            ("human", prompt),
        ]
    )

    return response.content.strip()