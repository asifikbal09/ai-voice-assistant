from app.modules.assistant.agent import get_llm


STT_NORMALIZER_PROMPT = """
You are a speech-to-text correction assistant for a customer voice assistant.

Your job is ONLY to clean and correct a raw speech transcription.

Rules:
1. Preserve the user's original meaning and intent.
2. Correct obvious speech-recognition and spelling errors.
3. Convert phonetic Banglish/Bengali transcription into natural Bengali
   when the user is clearly speaking Banglish.
4. Preserve English words when they are naturally used in the sentence.
5. Do NOT add information that the user did not say.
6. Do NOT answer the user's question.
7. Do NOT explain your corrections.
8. Return ONLY the corrected user sentence.
9. Keep proper nouns, company names, project names, service names,
   and technical terms when they are recognizable.
10. If the transcription is already correct, return it unchanged.

Examples:

Raw:
আপনদের ইন্য়ের ডিয়েন সেনে এক্টো ডিটিল্স বালেন

Corrected:
আপনাদের ইন্টেরিয়র ডিজাইন সার্ভিস নিয়ে একটু ডিটেইলস বলুন

Raw:
আমি আমার এপাট্মেন্টের জন্ন্ন্য় ইন্টারিয়ের ডিজাইন করতে চায়
আপনা রকি কন্সাল্টেশন প্রো঵াইড করেন

Corrected:
আমি আমার অ্যাপার্টমেন্টের জন্য ইন্টেরিয়র ডিজাইন করতে চাই,
আপনারা কি কনসালটেশন প্রোভাইড করেন?
"""


async def normalize_transcription(text: str) -> str:
    """
    Correct speech-recognition errors while preserving user intent.
    """

    if not text or not text.strip():
        return ""

    llm = get_llm()

    prompt = f"""
{STT_NORMALIZER_PROMPT}

Raw transcription:
{text}

Corrected transcription:
"""

    response = await llm.ainvoke(prompt)

    normalized_text = response.content.strip()

    if not normalized_text:
        return text.strip()

    return normalized_text