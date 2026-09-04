import whisper
import os
from typing import cast

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

_model = None


def load_model():
    """Whisper model ko ek baar load karke reuse karta hai."""

    global _model

    if _model is None:
        print("Loading Whisper model...")
        _model = whisper.load_model(WHISPER_MODEL)
        print("Whisper Model loaded successfully.")

    return _model


def transcribe_chunks(
    chunk_path: str,
    translate: bool = False
) -> str:
    """Ek audio chunk ko Whisper se transcribe karta hai."""

    # Pehle check karo file exist karti hai ya nahi.
    if not os.path.exists(chunk_path):
        raise FileNotFoundError(
            f"Audio chunk not found: {chunk_path}"
        )

    # File ka size check karo.
    file_size = os.path.getsize(chunk_path)

    print(f"Audio chunk: {chunk_path}")
    print(f"Audio chunk size: {file_size} bytes")

    # Empty file Whisper ko mat bhejo.
    if file_size == 0:
        raise ValueError(
            f"Audio chunk is empty: {chunk_path}"
        )

    model = load_model()

    # Translation chahiye to translate,
    # warna original language mein transcription.
    task = "translate" if translate else "transcribe"

    result = model.transcribe(
        chunk_path,
        task=task,
        fp16=False
    )

    return cast(str, result["text"])


def transcribe_all(
    chunks: list,
    translate: bool = False
) -> str:
    """Saare audio chunks ko transcribe karke ek transcript banata hai."""

    if not chunks:
        raise ValueError(
            "No audio chunks were generated."
        )

    full_transcription = ""

    for i, chunk in enumerate(chunks):

        print(
            f"Transcribing chunk {i + 1}/{len(chunks)}"
        )

        text = transcribe_chunks(
            chunk,
            translate=translate
        )

        # Empty transcription ko final text mein add nahi karenge.
        if text and text.strip():
            full_transcription += text.strip() + " "

    print("Transcription completed.")

    return full_transcription.strip()