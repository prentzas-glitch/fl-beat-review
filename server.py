import os
import tempfile
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
    """
    Build a drum index for a folder. Analyzes every audio file with librosa
    and saves drum_index.json inside the folder.
    This runs once — results are cached and reused on every beat review.
    """
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
    """Check if a drum index already exists for a folder."""
    index = load_index(req.folder_path)
    if index is None:
        return {"exists": False}
    summary = {cat: len(sounds) for cat, sounds in index.items()}
    summary["total"] = sum(summary.values())
    return {"exists": True, "summary": summary}


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

    # Save upload to a temp file
    suffix = Path(filename).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        # 1. Analyze locally (librosa needs the file on disk)
        audio_data = analyze_audio(tmp_path)

        # 2. Upload to Gemini once — all agents share this one reference
        audio_file = gemini_client.files.upload(file=tmp_path)
    finally:
        # Local temp file no longer needed after analysis + upload
        os.unlink(tmp_path)

    # 3. Scan general sound library if a path was provided
    library_prompt = ""
    if library_path.strip():
        try:
            library = scan_library(library_path.strip())
            detected_key = audio_data.get("key", "")
            library_prompt = format_library_for_prompt(library, detected_key)
        except (FileNotFoundError, ValueError):
            library_prompt = ""

    # 3b. Load drum index and find candidates if a drum library path was provided
    drum_candidates_prompt = ""
    if drum_library_path.strip():
        try:
            index = load_index(drum_library_path.strip())
            if index:
                detected_key = audio_data.get("key", "")
                candidates   = find_candidates(index, target_key=detected_key, n=3)
                drum_candidates_prompt = format_candidates_for_prompt(candidates, detected_key)
        except Exception:
            drum_candidates_prompt = ""

    # 4. Run the agent team, then clean up the Gemini file
    try:
        result = await run_agent_team(
            client=gemini_client,
            audio_file=audio_file,
            genre=genre,
            reference=reference,
            genre_profile=genre_profile,
            audio_data=audio_data,
            skill_level=skill_level,
            library_prompt=library_prompt,
            drum_candidates_prompt=drum_candidates_prompt,
        )
    finally:
        gemini_client.files.delete(name=audio_file.name)

    return {
        "audio_data": audio_data,
        "review": result["final_review"],
        "prompt": result["coordinator_prompt"],
        "genre": genre,
        "research_reports": result["research_reports"],
        "specialist_reports": result["specialist_reports"],
    }


class ChatRequest(BaseModel):
    message: str
    prompt: str
    history: list[dict]  # [{"role": "user"|"assistant", "content": str}]


@app.post("/chat")
def chat(req: ChatRequest):
    # The coordinator prompt is the opener — it has full beat context
    # (all 4 specialist reports + genre/reference/skill level) so the
    # model can answer follow-up questions with complete knowledge.
    gemini_history = [
        {"role": "user", "parts": [{"text": req.prompt}]},
    ]
    for turn in req.history:
        role = "model" if turn["role"] == "assistant" else "user"
        gemini_history.append({"role": role, "parts": [{"text": turn["content"]}]})

    chat_session = gemini_client.chats.create(model=MODEL, history=gemini_history)
    response = chat_session.send_message(req.message)
    return {"reply": response.text}
