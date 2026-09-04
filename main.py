from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pathlib import Path
import shutil

# PDF text extraction
from core.pdf_extractor import extract_pdf_text

# Audio processing:
# YouTube URL -> download -> WAV -> chunks
from utils.audio_processor import process_input

# Whisper transcription
from core.transcriber import transcribe_all

# AI Summary
from core.summarize import summarize


# FASTAPI APP
app = FastAPI(
    title="AI V Assistant",
    description="AI Meeting Assistant Backend",
    version="1.0.0",
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# UPLOAD DIRECTORY
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


# ROOT ENDPOINT
@app.get("/")
def root():
    return {
        "message": "AI V Assistant API is running"
    }


# HEALTH CHECK
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# PROCESS YOUTUBE / URL
@app.post("/process-url")
def process_url(
    url: str = Form(...),
    translate: bool = Form(False),
):
    try:

        print(f"Processing URL: {url}")

        # STEP 1
        # Download + Convert + Chunk
        chunks = process_input(url)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="Audio chunks could not be created."
            )

        # STEP 2
        # Whisper Transcription
        print("Starting transcription...")

        transcription = transcribe_all(
            chunks,
            translate=translate
        )

        print("Transcription completed.")

        # Summary yahan generate nahi karenge.
        # Frontend par Generate Summary button ke baad
        # /summarize endpoint call hoga.

        return {
            "success": True,
            "source": "url",
            "chunks": len(chunks),
            "transcription": transcription,
        }

    except HTTPException:
        raise

    except Exception as e:
        print(f"Error: {e}")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# UPLOAD PDF
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
):
    try:

        # STEP 1
        # Check filename
        filename = file.filename

        if not filename:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file must have a filename."
            )

        # STEP 2
        # Check file extension
        file_path = UPLOAD_DIR / filename

        extension = file_path.suffix.lower()

        if extension != ".pdf":
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported."
            )

        # STEP 3
        # Save uploaded PDF
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        print(f"PDF saved: {file_path}")

        # STEP 4
        # Extract text from PDF
        print("Extracting text from PDF...")

        transcription = extract_pdf_text(
            str(file_path)
        )

        if not transcription.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from PDF."
            )

        print("PDF text extraction completed.")

        # Summary yahan generate nahi karenge.
        # Frontend par Generate Summary button ke baad
        # /summarize endpoint call hoga.

        return {
            "success": True,
            "source": "upload",
            "filename": filename,
            "chunks": 0,
            "transcription": transcription,
        }

    except HTTPException:
        raise

    except Exception as e:
        print(f"PDF Error: {e}")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# GENERATE SUMMARY
@app.post("/summarize")
def summarize_transcript(
    transcript: str = Form(...)
):
    try:

        # Check transcript
        if not transcript.strip():
            raise HTTPException(
                status_code=400,
                detail="Transcript cannot be empty."
            )

        # Generate Summary using Mistral
        print("Generating meeting summary...")

        summary = summarize(transcript)

        print("Summary generated successfully.")

        return {
            "success": True,
            "summary": summary,
        }

    except HTTPException:
        raise

    except Exception as e:
        print(f"Summary Error: {e}")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )