from langchain_groq import ChatGroq

from app.core.config import settings
from app.modules.assistant.prompts import ASSISTANT_SYSTEM_PROMPT
from app.modules.knowledge.retriever import get_relevant_documents
from app.modules.conversation.memory import conversation_memory
from app.modules.knowledge.query_rewriter import rewrite_query

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


async def generate_ai_response(
    user_message: str,
    session_id: str,
) -> str:

    llm = get_llm()

    history = conversation_memory.get_history(
        session_id
    )

    search_query = await rewrite_query(
    user_message=user_message,
    history=history,
    )

    documents = get_relevant_documents(
        search_query,
        k=4,
    )

    if not documents:
        return (
            "দুঃখিত, এই বিষয়ে আমাদের কাছে বর্তমানে "
            "পর্যাপ্ত তথ্য নেই।"
        )

    context = build_context(documents)

    history_text = ""

    for message in history:
        history_text += (
            f'{message["role"].capitalize()}: '
            f'{message["content"]}\n'
        )

    user_prompt = f"""
Relevant company knowledge:

{context}

Previous conversation:

{history_text}

Customer's latest question:

{user_message}

Instructions:
- Use the company knowledge above.
- Use previous conversation to understand context.
- If the customer uses words like "এটা", "ওটা", "this", "that",
  understand what they are referring to from the conversation.
- Do not invent company information.
- If the knowledge does not contain the answer, clearly say
  that the information is unavailable.
- Reply naturally in the customer's language.
"""

    messages = [
        (
            "system",
            ASSISTANT_SYSTEM_PROMPT,
        ),
        (
            "human",
            user_prompt,
        ),
    ]

    response = await llm.ainvoke(messages)

    answer = response.content

    conversation_memory.add_message(
        session_id=session_id,
        role="user",
        content=user_message,
    )

    conversation_memory.add_message(
        session_id=session_id,
        role="assistant",
        content=answer,
    )

    return answer