from fastapi import APIRouter, File, Form, UploadFile

from app.modules.voice.service import transcribe_audio

router = APIRouter()


@router.post("/transcribe")
async def transcribe(
    audio: UploadFile = File(...),
    language: str | None = Form(default=None),
):

    text = await transcribe_audio(
        audio=audio,
        language=language,
    )

    return {
        "success": True,
        "language": language,
        "text": text,
    }