import asyncio
import os
import tempfile
import threading
import uuid
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google import genai

from analysis import analyze_audio, SUPPORTED_FORMATS
from genres import GENRE_PROFILES, SKILL_LEVELS
from agents import run_agent_team
from library import scan_library, format_library_for_prompt
from drum_indexer import build_index, load_index, find_candidates, format_candidates_for_prompt
from ai import MODEL

app = FastAPI()

BASE_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

gemini_client = genai.Client()

# In-memory job store — good enough for a demo
jobs: dict[str, dict] = {}


@app.get("/")
def index():
    return FileResponse(str(BASE_DIR / "static" / "index.html"))


@app.get("/genres")
def get_genres():
    return {"genres": sorted(GENRE_PROFILES.keys())}


class ScanLibraryRequest(BaseModel):
    folder_path: str

@app.post("/scan-library")
def scan_library_endpoint(req: ScanLibraryRequest):
    try:
        library = scan_library(req.folder_path)
        return {"library": library, "success": True}
    except FileNotFoundError as e:
        raise HTTPException(400, str(e))
    except ValueError as e:
        raise HTTPException(400, str(e))


class IndexDrumsRequest(BaseModel):
    folder_path: str

@app.post("/index-drums")
def index_drums(req: IndexDrumsRequest):
    try:
        summary = build_index(req.folder_path)
        return {"summary": summary, "success": True}
    except FileNotFoundError as e:
        raise HTTPException(400, str(e))
    except ValueError as e:
        raise HTTPException(400, str(e))


class CheckIndexRequest(BaseModel):
    folder_path: str

@app.post("/check-drum-index")
def check_drum_index(req: CheckIndexRequest):
    index = load_index(req.folder_path)
    if index is None:
        return {"exists": False}
    summary = {cat: len(sounds) for cat, sounds in index.items()}
    summary["total"] = sum(summary.values())
    return {"exists": True, "summary": summary}


def _run_review_job(job_id: str, tmp_path: str, genre: str, reference: str,
                    genre_profile: dict, skill_level: str,
                    library_path: str, drum_library_path: str):
    try:
        try:
            audio_data = analyze_audio(tmp_path)
            print(f"[job {job_id[:8]}] audio analyzed — BPM={audio_data.get('bpm')}, key={audio_data.get('key')}")
            with open(tmp_path, "rb") as f:
                audio_bytes = f.read()
            suffix = Path(tmp_path).suffix.lower()
            mime_map = {".wav": "audio/wav", ".mp3": "audio/mpeg", ".flac": "audio/flac",
                        ".aiff": "audio/aiff", ".ogg": "audio/ogg"}
            mime_type = mime_map.get(suffix, "audio/wav")
            print(f"[job {job_id[:8]}] audio ready ({len(audio_bytes)//1024}KB), starting agents…")
        finally:
            os.unlink(tmp_path)

        library_prompt = ""
        if library_path.strip():
            try:
                library = scan_library(library_path.strip())
                library_prompt = format_library_for_prompt(library, audio_data.get("key", ""))
            except Exception:
                pass

        drum_candidates_prompt = ""
        if drum_library_path.strip():
            try:
                index = load_index(drum_library_path.strip())
                if index:
                    candidates = find_candidates(index, target_key=audio_data.get("key", ""), n=3)
                    drum_candidates_prompt = format_candidates_for_prompt(candidates, audio_data.get("key", ""))
            except Exception:
                pass

        print(f"[job {job_id[:8]}] starting agent team…")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(run_agent_team(
                client=gemini_client,
                audio_bytes=audio_bytes,
                mime_type=mime_type,
                genre=genre,
                reference=reference,
                genre_profile=genre_profile,
                audio_data=audio_data,
                skill_level=skill_level,
                library_prompt=library_prompt,
                drum_candidates_prompt=drum_candidates_prompt,
            ))
        finally:
            loop.close()

        print(f"[job {job_id[:8]}] done!")
        jobs[job_id] = {
            "status": "done",
            "audio_data": audio_data,
            "review": result["final_review"],
            "prompt": result["coordinator_prompt"],
            "genre": genre,
            "research_reports": result["research_reports"],
            "specialist_reports": result["specialist_reports"],
        }
    except Exception as e:
        jobs[job_id] = {"status": "error", "error": str(e)}


@app.post("/review")
async def review(
    file: UploadFile = File(...),
    genre: str = Form(...),
    reference: str = Form(...),
    skill_level: str = Form(...),
    library_path: str = Form(default=""),
    drum_library_path: str = Form(default=""),
):
    filename = file.filename or ""
    if not filename.lower().endswith(SUPPORTED_FORMATS):
        raise HTTPException(400, f"Unsupported format. Supported: {', '.join(SUPPORTED_FORMATS)}")
    if skill_level not in SKILL_LEVELS:
        raise HTTPException(400, "Invalid skill level.")

    genre = genre.strip().lower()
    genre_profile = GENRE_PROFILES.get(genre, GENRE_PROFILES["trap"])

    suffix = Path(filename).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "pending"}

    t = threading.Thread(
        target=_run_review_job,
        args=(job_id, tmp_path, genre, reference, genre_profile,
              skill_level, library_path, drum_library_path),
        daemon=False,
    )
    t.start()

    return {"job_id": job_id}


@app.get("/result/{job_id}")
def get_result(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    return job


class ChatRequest(BaseModel):
    message: str
    prompt: str
    history: list[dict]


@app.post("/chat")
def chat(req: ChatRequest):
    gemini_history = [
        {"role": "user", "parts": [{"text": req.prompt}]},
    ]
    for turn in req.history:
        role = "model" if turn["role"] == "assistant" else "user"
        gemini_history.append({"role": role, "parts": [{"text": turn["content"]}]})

    chat_session = gemini_client.chats.create(model=MODEL, history=gemini_history)
    response = chat_session.send_message(req.message)
    return {"reply": response.text}
