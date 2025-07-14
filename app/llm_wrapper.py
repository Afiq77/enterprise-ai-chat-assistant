# app/llm_wrapper.py

import os
import re
import subprocess
from dotenv import load_dotenv

import google.generativeai as genai
import whisper

from app.order_formatter import format_order_record

# === Load environment variables ===
load_dotenv()

# === Gemini Configuration ===
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ Missing GEMINI_API_KEY in .env")

genai.configure(api_key=GEMINI_API_KEY, transport="rest")
gemini_model = genai.GenerativeModel("models/gemini-2.5-flash-preview-05-20")

# === Whisper Voice Transcription (lazy-load) ===
_whisper_model = None

def get_whisper_model(model_name: str = "small"):
    global _whisper_model
    if _whisper_model is None:
        print(f"🔊 Loading Whisper model: {model_name}")
        _whisper_model = whisper.load_model(model_name)
    return _whisper_model

def convert_webm_to_wav(webm_path: str) -> str:
    wav_path = webm_path.replace(".webm", ".wav")
    try:
        subprocess.run(["ffmpeg", "-y", "-i", webm_path, wav_path], check=True, capture_output=True)
        return wav_path
    except subprocess.CalledProcessError as e:
        print("❌ FFmpeg conversion error:", e.stderr.decode())
        raise RuntimeError("Audio conversion failed.")

def transcribe_audio(file_path: str) -> str:
    if file_path.endswith(".webm"):
        file_path = convert_webm_to_wav(file_path)
    model = get_whisper_model()
    result = model.transcribe(file_path)
    return result["text"].strip()

def handle_voice_query(audio_path: str, provider: str = "gemini") -> str:
    try:
        query = transcribe_audio(audio_path)
        if not query:
            return "⚠️ Unable to understand audio clearly."
        return run_llm_query(query, provider=provider)
    except Exception as e:
        return f"❌ Voice query failed: {str(e)}"

# === LLM Unified Entry Point ===
def run_llm_query(query: str, context_chunks: list = None, provider: str = "gemini") -> str:
    if provider == "gemini":
        return _run_with_gemini(query, context_chunks)
    elif provider == "openai":
        return _run_with_openai(query, context_chunks)
    elif provider == "local":
        return _run_with_local_model(query, context_chunks)
    else:
        return f"❌ Unknown LLM provider: '{provider}'"

# === Gemini Backend ===
def _run_with_gemini(query: str, context_chunks: list = None) -> str:
    if not context_chunks:
        return _run_gemini_prompt(query)

    records = []
    for chunk in context_chunks:
        rec = {}
        for part in chunk.split("||"):
            if ":" in part:
                k, v = part.split(":", 1)
                rec[k.strip()] = v.strip()
        records.append(rec)

    context_str = "\n\n".join([format_order_record(r) for r in records])

    prompt = f"""
You are an assistant summarizing order data.

Instructions:
- Preserve all line breaks and field formatting.
- Do not use markdown, symbols, or merge lines.
- Provide a clear response based on the input context.

Context:
{context_str}

Query:
{query}
""".strip()

    try:
        chat = gemini_model.start_chat()
        response = chat.send_message(prompt)
        return response.text.strip().replace("*", "").replace("\\", "").replace("\n", " ")
    except Exception as e:
        return f"❌ Gemini API error: {str(e)}"

def _run_gemini_prompt(prompt: str) -> str:
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini free-form prompt failed: {str(e)}"

# === OpenAI Placeholder ===
def _run_with_openai(query: str, context_chunks: list = None) -> str:
    return "⚠️ OpenAI integration not yet implemented."

# === Local LLM (e.g., Mistral via Ollama) Placeholder ===
def _run_with_local_model(query: str, context_chunks: list = None) -> str:
    return "⚠️ Local model (e.g., Mistral/Ollama) not yet integrated."

# === Title generation ===
def clean_message(message: str) -> str:
    return re.sub(r'\b(order|truck)[^ ]*\b', '', message, flags=re.IGNORECASE).strip()

def generate_title_from_model(message: str, provider: str = "gemini") -> str:
    cleaned = clean_message(message)

    prompt = f"""
Generate a short 3-5 word chat title for this message. Avoid numbers or IDs.

Message:
{cleaned}

Title:
"""
    if provider == "gemini":
        try:
            chat = gemini_model.start_chat()
            response = chat.send_message(prompt)
            return response.text.strip()
        except Exception:
            return "Untitled Chat"
    else:
        return "Untitled Chat"
