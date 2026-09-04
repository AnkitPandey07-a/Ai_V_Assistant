# 🤖 AI V Assistant

An AI-powered content and meeting assistant that processes **YouTube videos and PDF documents**, converts their content into text, and generates AI-powered summaries.

The project combines **Whisper, LangChain, Mistral AI, RAG, FastAPI and React** to build an end-to-end AI application.

---

## 🚀 Features

### 🎥 YouTube Video Processing
- Accept YouTube video URLs
- Extract audio using `yt-dlp`
- Process audio using `FFmpeg`
- Split audio into manageable chunks
- Transcribe audio using OpenAI Whisper

### 📄 PDF Processing
- Upload PDF documents
- Extract text using PyMuPDF
- Process extracted content for AI analysis

### 🤖 AI Summarization
- Generate summaries using Mistral AI
- Use LangChain for LLM workflows
- Convert long content into concise and useful summaries

### 🔎 RAG Pipeline
- HuggingFace embeddings
- ChromaDB vector store
- Retrieval-based document processing
- LangChain-based retrieval workflow

### 🌐 Full-Stack Application
- React + Vite frontend
- FastAPI backend
- REST API architecture
- CORS configuration
- Frontend deployed on Vercel

---

## 🏗️ Architecture

```text
                 ┌─────────────────┐
                 │   YouTube URL   │
                 └────────┬────────┘
                          ↓
                    ┌───────────┐
                    │  yt-dlp   │
                    └─────┬─────┘
                          ↓
                    ┌───────────┐
                    │  FFmpeg   │
                    └─────┬─────┘
                          ↓
                  ┌────────────────┐
                  │ Audio Chunks   │
                  └───────┬────────┘
                          ↓
                    ┌───────────┐
                    │  Whisper  │
                    └─────┬─────┘
                          ↓
                    ┌───────────┐
                    │Transcript │
                    └─────┬─────┘
                          ↓
              ┌──────────────────────┐
              │ LangChain + Mistral  │
              └──────────┬───────────┘
                         ↓
                      Summary


                 ┌─────────────────┐
                 │   PDF Upload    │
                 └────────┬────────┘
                          ↓
                    ┌───────────┐
                    │ PyMuPDF   │
                    └─────┬─────┘
                          ↓
                     ┌─────────┐
                     │  Text   │
                     └────┬────┘
                          ↓
                ┌───────────────────┐
                │ HuggingFace       │
                │ Embeddings        │
                └─────────┬─────────┘
                          ↓
                    ┌───────────┐
                    │ ChromaDB  │
                    └─────┬─────┘
                          ↓
                     RAG Retrieval
                          ↓
                    Mistral AI
                          ↓
                       Answer
🛠️ Tech Stack
Frontend
React.js
Vite
JavaScript
CSS
Backend
Python
FastAPI
Uvicorn
AI / ML
OpenAI Whisper
Mistral AI
LangChain
HuggingFace
ChromaDB
Document & Audio Processing
PyMuPDF
yt-dlp
FFmpeg
Pydub
Development
Git
GitHub
Python Virtual Environment
📂 Project Structure
Ai V Assistant/
│
├── core/
│   ├── transcriber.py
│   ├── summarize.py
│   ├── vector_store.py
│   ├── extractor.py
│   ├── rag_engine.py
│   └── pdf_extractor.py
│
├── utils/
│   └── audio_processor.py
│
├── downloads/
├── uploads/
│
├── frontend/
│   └── src/
│       ├── App.jsx
│       ├── App.css
│       ├── index.css
│       └── main.jsx
│
├── main.py
├── requirements.txt
├── runtime.txt
├── test.py
└── README.md
⚙️ Installation
1. Clone the repository
git clone https://github.com/AnkitPandey07-a/Ai_V_Assistant.git
cd Ai_V_Assistant
2. Create virtual environment
python -m venv .venv
3. Activate virtual environment
Windows PowerShell
.venv\Scripts\Activate.ps1
4. Install dependencies
pip install -r requirements.txt
🔐 Environment Variables

Create a .env file in the project root:

MISTRAL_API_KEY=your_mistral_api_key
WHISPER_MODEL=small

Never commit your .env file or API keys to GitHub.

▶️ Running the Backend

Start FastAPI:

uvicorn main:app --reload

Backend will run at:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs
▶️ Running the Frontend

Go to the frontend directory:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

Frontend will run at:

http://localhost:5173
🔌 API Endpoints
Process YouTube URL
POST /process-url

Accepts:

url
translate

Returns the generated transcript.

Upload PDF
POST /upload

Accepts a PDF file and extracts its text using PyMuPDF.

Generate Summary
POST /summarize

Accepts transcript text and generates an AI-powered summary using Mistral AI.

🧠 What I Learned

Building this project gave me hands-on experience with:

Building AI-powered applications
Speech-to-text using Whisper
LLM integration using Mistral AI
LangChain workflows
RAG architecture
Vector databases
PDF and audio processing
REST API development
React and FastAPI integration
Dependency management
Debugging AI pipelines
Frontend/backend deployment
🐛 Challenges & Debugging

During development, I encountered several real-world issues.

Whisper Audio Chunk Errors

Some generated audio chunks caused Whisper/Torch tensor errors.

I debugged the audio pipeline by validating generated chunks and checking file sizes before sending them to Whisper.

PyMuPDF Dependency

The backend initially failed because the PDF extraction dependency was missing.

Adding the correct PyMuPDF dependency fixed the issue.

Python Compatibility

Deployment exposed compatibility issues involving:

Python 3.14
pydub
pyaudioop

This highlighted the importance of Python version compatibility when deploying ML applications.

Mistral API Rate Limit

The summarization API returned:

HTTP 429 - Rate Limit Exceeded

The integration itself was working, but the API request was limited by the provider.

This showed the importance of implementing proper API error handling, retries and fallbacks in production applications.

Deployment Memory Limitation

The backend uses resource-heavy dependencies such as:

Whisper
PyTorch
ChromaDB
Sentence Transformers

The free Render environment provided only 512 MB RAM, which was insufficient for the complete backend stack and resulted in an out-of-memory error.

The frontend is deployed separately, while the backend can be run locally.

📸 Application Flow
Enter YouTube URL
        ↓
Process Video
        ↓
Extract Audio
        ↓
Whisper Transcription
        ↓
Transcript Ready
        ↓
Generate Summary
        ↓
Mistral AI
        ↓
Summary Ready
🚧 Future Improvements
Better API rate-limit handling
Background processing for long videos
Improved RAG pipeline
Streaming AI responses
Authentication
Persistent vector database
Better deployment architecture
Cloud-based audio processing
Support for additional document formats
🎯 Project Goal

The main goal of this project was to understand how different AI components can be combined into a complete application:

Data → Processing → Transcription → Retrieval → LLM → Response

Rather than only working with individual AI tools, this project helped me understand how they work together inside a real application.

👨‍💻 Author

Ankit Pandey

GitHub:
https://github.com/AnkitPandey07-a
