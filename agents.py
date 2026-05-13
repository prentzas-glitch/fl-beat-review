"""
Agent pipeline for FL Studio beat review.

Two-stage pipeline optimised for the free-tier Gemini quota:

  Stage 1 — Research (1 call, no web search):
    Combines artist + genre context from model knowledge.

  Stage 2 — Review (1 call, listens to the audio):
    Comprehensive review covering mixing, drums, sound design,
    and arrangement in a single structured response.

2 total Gemini calls → completes in 2-4 minutes on free tier.
"""

import asyncio
import json
import time
from google import genai
from google.genai import types
from genres import SKILL_LEVELS
from ai import MODEL


def _with_backoff(fn, *args, max_attempts=4):
    for attempt in range(max_attempts):
        try:
            return fn(*args)
        except Exception as e:
            if "429" in str(e) and attempt < max_attempts - 1:
                wait = 30 * (attempt + 1)
                print(f"[429] attempt {attempt+1}/{max_attempts}, retrying in {wait}s…")
                time.sleep(wait)
            else:
                raise


def _call_gemini_sync(client: genai.Client, prompt: str,
                      audio_bytes: bytes | None = None,
                      mime_type: str = "audio/wav") -> str:
    def _call():
        contents = [prompt]
        if audio_bytes:
            contents.append(types.Part.from_bytes(data=audio_bytes, mime_type=mime_type))
        return client.models.generate_content(model=MODEL, contents=contents).text
    return _with_backoff(_call)


def _research_prompt(genre: str, reference: str) -> str:
    return f"""You are a music production researcher. Using your knowledge, give a concise
production briefing on the following. Focus on actionable details a producer can use.

=== Reference Artist/Track: {reference} ===
- Signature sound and what makes their beats recognisable
- Typical BPM range and tempo feel
- Drum style — hi-hat patterns, kick/snare placement, 808 use
- Mixing characteristics — bright/dark, wide/narrow, punchy?
- Key/scale preferences
- Notable FL Studio or production techniques

=== Genre: {genre} (current trends 2024-2025) ===
- What separates a top-tier {genre} beat from an average one right now
- Typical BPM range and drum feel
- Popular sounds, textures, synth choices
- Mixing/mastering trends — how do top beats in this genre sound?
- 2-3 producers currently defining the genre and what they do differently

Be specific and concise. Bullet points preferred."""


def _review_prompt(genre: str, reference: str, audio_data: dict,
                   genre_profile: dict, skill: dict, research: str,
                   library_prompt: str = "", drum_candidates: str = "") -> str:
    bpm_low, bpm_high = genre_profile["bpm_range"]
    return f"""You are a professional music producer reviewing a {genre} beat
(reference: {reference}). Listen to the audio carefully, then give a full structured review.

Producer skill level: {skill['label']} — {skill['description']}
Tone: {skill['tone']}

== Research Context ==
{research}

== Audio Analysis ==
{json.dumps(audio_data, indent=2)}

Genre baseline BPM: {bpm_low}–{bpm_high} | Drum feel: {genre_profile['drum_feel']}

{f"== Producer's Sound Library =={chr(10)}{library_prompt}" if library_prompt else ""}
{f"== Drum Candidates =={chr(10)}{drum_candidates}" if drum_candidates else ""}

FL Studio tools: Parametric EQ 2, Fruity Compressor, Maximus, FPC, Gross Beat,
FLEX, Sytrus, Fruity Delay 3, Fruity Reeverb 2, Stereo Enhancer, Pitcher.

Rules:
- Use the research context to calibrate what "good" sounds like for this genre/artist.
- Compare the beat against the reference — how close or far is it?
- Give exact FL Studio settings where relevant (frequencies, ratios, ms).
- When recommending sounds, reference files from the library by exact filename.
- Keep every section tight. Producers read fast.

== Output format — follow exactly ==

### 1. BPM & Tempo
### 2. Key & Sound Selection
### 3. Drums & Patterns
### 4. Mixing
### 5. Arrangement & Structure
### 6. Overall Score & Priority Fixes
(Score /10. Top 3 fixes in order of impact. One honest sentence on the beat's best quality.)
""".strip()


async def run_agent_team(
    client: genai.Client,
    audio_bytes: bytes,
    mime_type: str,
    genre: str,
    reference: str,
    genre_profile: dict,
    audio_data: dict,
    skill_level: str,
    library_prompt: str = "",
    drum_candidates_prompt: str = "",
) -> dict:
    skill = SKILL_LEVELS[skill_level]
    loop = asyncio.get_running_loop()

    # Stage 1 — Research (no audio needed)
    print("[agents] Stage 1: research…")
    try:
        research = await loop.run_in_executor(
            None, _call_gemini_sync,
            client, _research_prompt(genre, reference), None, mime_type
        )
    except Exception as e:
        research = f"[Research unavailable: {e}]"
    print("[agents] Stage 1 done.")

    # Stage 2 — Comprehensive review (listens to the audio)
    print("[agents] Stage 2: review…")
    rev_prompt = _review_prompt(
        genre, reference, audio_data, genre_profile, skill, research,
        library_prompt, drum_candidates_prompt
    )
    try:
        final_review = await loop.run_in_executor(
            None, _call_gemini_sync,
            client, rev_prompt, audio_bytes, mime_type
        )
    except Exception as e:
        final_review = f"[Review could not complete: {e}]"
    print("[agents] Stage 2 done.")

    return {
        "research_reports": {"artist": research, "genre": ""},
        "specialist_reports": {},
        "final_review": final_review,
        "coordinator_prompt": rev_prompt,
    }
