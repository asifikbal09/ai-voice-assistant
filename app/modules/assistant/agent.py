from langchain_groq import ChatGroq

from app.core.config import settings
from app.modules.assistant.prompts import ASSISTANT_SYSTEM_PROMPT
from app.modules.knowledge.retriever import get_relevant_documents


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


def build_context(documents) -> str:
    if not documents:
        return "No relevant company information was found."

    context_parts = []

    for document in documents:
        context_parts.append(
            f"""
Source: {document.metadata.get("source")}

{document.page_content}
"""
        )

    return "\n\n---\n\n".join(context_parts)


async def generate_ai_response(user_message: str) -> str:
    llm = get_llm()

    documents = get_relevant_documents(
        user_message,
        k=4,
    )

    if not documents:
        return (
            "দুঃখিত, এই বিষয়ে আমাদের কাছে বর্তমানে "
            "পর্যাপ্ত তথ্য নেই।"
        )

    context = build_context(documents)

    user_prompt = f"""
Relevant company knowledge:

{context}

Customer question:

{user_message}

Instructions:
- Answer using only the relevant company knowledge above.
- Do not invent information.
- If the knowledge does not contain the answer, clearly say that the information is unavailable.
- Reply naturally in the customer's language.
"""

    messages = [
        ("system", ASSISTANT_SYSTEM_PROMPT),
        ("human", user_prompt),
    ]

    response = await llm.ainvoke(messages)

    return response.content