from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.modules.voice.service import transcribe_audio
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db
from app.modules.voice.service import (
    transcribe_audio,
    synthesize_speech,
    voice_chat
)

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


@router.post("/synthesize")
async def synthesize(
    text: str = Form(...),
):
    audio = await synthesize_speech(text)

    return Response(
        content=audio,
        media_type="audio/mpeg",
        headers={
            "Content-Disposition": 'attachment; filename="speech.mp3"',
            "Content-Length": str(len(audio)),
        },
    )

@router.post("/chat")
async def voice_conversation(
    audio: UploadFile = File(...),
    session_id: str = Form(...),
    language: str = Form(default="bn"),
    db: Annotated[AsyncSession, Depends(get_db)] = None,
):
    audio_response = await voice_chat(
        audio=audio,
        db=db,
        session_id=session_id,
        language=language,
    )

    return Response(
        content=audio_response,
        media_type="audio/mpeg",
        headers={
            "Content-Disposition": 'attachment; filename="voice-response.mp3"',
            "Content-Length": str(len(audio_response)),
        },
    )