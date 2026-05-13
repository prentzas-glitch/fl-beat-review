"""
Agent team for FL Studio beat review.

Pipeline (3 phases):

  Phase 1 — Research (parallel, web search enabled):
    Artist Research Agent  → signature sound, drum style, mixing, recent releases
    Genre Research Agent   → current trends, top producers, techniques in this genre

  Phase 2 — Specialists (parallel, receive research context from Phase 1):
    Mixing Agent           → EQ, compression, levels, stereo width
    Drums Agent            → groove, feel, pattern, hit weight
    Sound/Key Agent        → sound selection, key fit, harmonic content
    Arrangement Agent      → structure, variation, transitions

  Phase 3 — Coordinator:
    Reads all 6 reports, synthesizes into the final review.

Why research agents?
  Right now the specialists only know the genre label and analysis numbers.
  The research agents give them real context — what the reference artist's
  beats actually sound like, what's trending in the genre right now —
  so feedback is specific and current rather than generic.
"""

import asyncio
import json
from dataclasses import dataclass
from google import genai
from google.genai import types
from genres import SKILL_LEVELS
from ai import MODEL


# ── Agent result ──────────────────────────────────────────────────────────────

@dataclass
class AgentResult:
    name: str    # human-readable label
    key: str     # dict key used in the response JSON
    report: str  # markdown output from this agent


# ── Gemini call — with audio ──────────────────────────────────────────────────
# Used by specialist agents that need to listen to the beat.

def _call_gemini_sync(client: genai.Client, prompt: str, audio_file) -> str:
    response = client.models.generate_content(
        model=MODEL,
        contents=[prompt, audio_file],
    )
    return response.text


# ── Gemini call — with Google Search grounding, no audio ─────────────────────
# Used by research agents. Google Search grounding lets the model search
# the web in real time as part of generating its response.
# This is how the research agents get current, specific information about
# an artist or genre rather than relying only on training data.

def _call_gemini_search_sync(client: genai.Client, prompt: str) -> str:
    response = client.models.generate_content(
        model=MODEL,
        contents=[prompt],
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())]
        ),
    )
    return response.text


# ── Async wrappers ────────────────────────────────────────────────────────────
# run_in_executor pushes the blocking (synchronous) Gemini calls into a
# thread pool so multiple agents can run at the same time instead of waiting
# for each one to finish before starting the next.

async def _run_agent(client, name: str, key: str, prompt: str, audio_file) -> AgentResult:
    """Specialist agent — listens to the audio file."""
    loop = asyncio.get_running_loop()
    try:
        report = await loop.run_in_executor(
            None, _call_gemini_sync, client, prompt, audio_file
        )
    except Exception as e:
        report = f"[{name} could not complete its analysis: {e}]"
    return AgentResult(name=name, key=key, report=report)


async def _run_research_agent(client, name: str, key: str, prompt: str) -> AgentResult:
    """Research agent — searches the web, no audio file needed."""
    loop = asyncio.get_running_loop()
    try:
        report = await loop.run_in_executor(
            None, _call_gemini_search_sync, client, prompt
        )
    except Exception as e:
        report = f"[{name} search could not complete: {e}]"
    return AgentResult(name=name, key=key, report=report)


# ── Research agent prompts ────────────────────────────────────────────────────

def _artist_research_prompt(reference: str, genre: str) -> str:
    return f"""You are a music production researcher. Search the web for detailed production
information about this artist/track: "{reference}" in the context of {genre}.

Find and report on:
- Their signature sound — what makes their beats instantly recognisable
- Typical BPM range and tempo feel they work with
- Key/scale preferences (minor, major, modes)
- Drum programming style — hi-hat patterns, kick placement, snare characteristics, 808 use
- Mixing characteristics — how their beats sound sonically (bright, dark, wide, punchy?)
- Specific FL Studio or production techniques associated with their sound
- How their sound has evolved in recent releases (2024–2026)
- Producers they frequently work with and their shared techniques

Be specific and factual. Focus on actionable production details that a producer could
actually use to compare their beat against. Keep it concise — bullet points preferred."""


def _genre_research_prompt(genre: str) -> str:
    return f"""You are a music production researcher. Search the web for current production
trends and techniques in {genre} as of 2025–2026.

Find and report on:
- What's trending right now — sounds, techniques, drum patterns, arrangements
- Typical BPM range and tempo feel that defines the genre currently
- Common drum patterns and programming approaches top producers are using
- Popular sounds, synths, samples, and textures being used
- Mixing and mastering trends — how do top {genre} beats sound sonically?
- What separates a top-tier {genre} beat from an average one right now
- Names of 3–5 producers currently defining the genre's sound and what they do differently
- Any specific FL Studio techniques or plugins that are popular in this genre

Be specific and factual. Focus on actionable production details.
Keep it concise — bullet points preferred."""


# ── Specialist prompt builders ────────────────────────────────────────────────
# Each specialist gets:
# - Only the analysis data relevant to its domain (less noise = better focus)
# - The research context from Phase 1 (artist + genre intel)

def _mixing_prompt(genre: str, audio_data: dict, skill: dict, research_context: str) -> str:
    relevant = {k: audio_data[k] for k in
                ("peak", "rms_avg", "rms_std", "frequency_balance",
                 "spectral_centroid_hz", "interpretation")
                if k in audio_data}
    return f"""You are a professional mixing engineer reviewing a {genre} beat.
Focus ONLY on: EQ, compression, levels, stereo width, frequency balance, headroom, and clarity.
Do NOT comment on drums, arrangement, melody, or sound selection — handled by other specialists.

Producer skill level: {skill['label']} — {skill['description']}
Tone guidance: {skill['tone']}

== Research context (use this to calibrate what "good" sounds like for this genre/artist) ==
{research_context}

== Audio analysis data ==
{json.dumps(relevant, indent=2)}

FL Studio plugins: Parametric EQ 2, Fruity Compressor, Maximus, Fruity Stereo Enhancer,
Mixer routing and send tracks.

Rules:
- Use the research context to judge whether the mix matches the target sound.
- Give exact settings: frequencies, dB, Q values, ratios, ms.
- If something sounds fine, say so and move on. Keep it tight.

Write your mixing report in markdown."""


def _drums_prompt(genre: str, genre_profile: dict, audio_data: dict, skill: dict, research_context: str, library_prompt: str = "", drum_candidates: str = "") -> str:
    relevant = {k: audio_data[k] for k in
                ("bpm", "transient_density", "duration_sec", "interpretation")
                if k in audio_data}
    bpm_low, bpm_high = genre_profile["bpm_range"]
    return f"""You are a drums and pattern specialist reviewing a {genre} beat.
Focus ONLY on: groove, feel, hit weight, pattern tightness, hi-hat style, kick and snare placement.
Do NOT comment on mixing levels, arrangement, or melody — handled by other specialists.

Producer skill level: {skill['label']} — {skill['description']}
Tone guidance: {skill['tone']}

Genre baseline:
- Typical BPM for {genre}: {bpm_low}–{bpm_high}
- Typical drum feel: {genre_profile['drum_feel']}

== Research context (current trends and reference artist's drum style) ==
{research_context}

== Audio analysis data ==
{json.dumps(relevant, indent=2)}

FL Studio plugins: FPC, Fruity Compressor (per channel), Parametric EQ 2 (per channel), Gross Beat.

{f"== Producer's drum library (audio-analysed candidates) =={chr(10)}{drum_candidates}{chr(10)}{chr(10)}These sounds were selected from the producer's actual library using audio feature matching.{chr(10)}Reference them by exact filename when suggesting replacements or additions.{chr(10)}For 808s, files marked KEY MATCH are in the same key as the beat — prioritise those." if drum_candidates else ""}

Rules:
- Compare what you hear against the research context — is it on trend or outdated?
- Flag what's wrong AND what's working. Give exact FPC or mixer steps to fix problems.
- If drum candidates are provided, always recommend by exact filename with a brief reason.
- Keep it tight.

Write your drums report in markdown."""


def _sound_design_prompt(genre: str, reference: str, audio_data: dict, skill: dict, research_context: str, library_prompt: str = "") -> str:
    relevant = {k: audio_data[k] for k in
                ("key", "key_confidence", "spectral_centroid_hz", "interpretation")
                if k in audio_data}
    return f"""You are a sound design and harmony specialist reviewing a {genre} beat.
Focus ONLY on: sound selection, key fit, harmonic content, vibe, and whether the sounds
match the {genre} style and the reference: {reference}.
Do NOT comment on mixing levels, drums, or arrangement — handled by other specialists.

Producer skill level: {skill['label']} — {skill['description']}
Tone guidance: {skill['tone']}

== Research context (reference artist's sonic identity and genre sound palette) ==
{research_context}

== Audio analysis data ==
{json.dumps(relevant, indent=2)}

Key confidence note: if key_confidence is below 0.7, detection was uncertain —
trust your ears over the data.

FL Studio plugins: FLEX, Sytrus, Harmor, Pitcher, Fruity Delay 3, Fruity Reeverb 2.

{f"== Producer's available sounds =={chr(10)}{library_prompt}{chr(10)}{chr(10)}IMPORTANT: When recommending sounds, reference specific files from this library by exact filename. Only suggest FLEX/Sytrus/Harmor if no suitable file exists in the library." if library_prompt else ""}

Rules:
- Use the research context to judge whether the sounds match the reference artist's world.
- Call out anything that clashes or feels out of place.
- If a library is provided, always recommend from it first before suggesting synth patches.
- Files marked '← matches key' are in the same key as the beat — prioritise these.
- Keep it tight.

Write your sound design report in markdown."""


def _arrangement_prompt(genre: str, audio_data: dict, skill: dict, research_context: str) -> str:
    relevant = {k: audio_data[k] for k in
                ("bpm", "duration_sec", "transient_density")
                if k in audio_data}
    return f"""You are an arrangement specialist reviewing a {genre} beat.
Focus ONLY on: structure, variation, transitions, build-ups, drops, fills, and whether
the beat holds a listener's attention from start to finish.
Do NOT comment on mixing, sound selection, or drum patterns — handled by other specialists.

Producer skill level: {skill['label']} — {skill['description']}
Tone guidance: {skill['tone']}

== Research context (how top {genre} beats are arranged right now) ==
{research_context}

== Audio analysis data ==
{json.dumps(relevant, indent=2)}

FL Studio tools: Playlist patterns, automation clips, pattern mutes, fill patterns,
Gross Beat (for transition effects).

Rules:
- Compare the arrangement against what the research says is standard for this genre.
- Comment on intro, main loop, variation points, and outro.
- Suggest specific FL Studio arrangement moves. Keep it tight.

Write your arrangement report in markdown."""


# ── Coordinator prompt ────────────────────────────────────────────────────────

def _coordinator_prompt(
    genre: str,
    reference: str,
    audio_data: dict,
    skill: dict,
    research_reports: dict,
    specialist_reports: dict,
) -> str:
    research_block = "\n\n".join([
        f"=== ARTIST RESEARCH: {reference} ===\n{research_reports.get('artist', '[no data]')}",
        f"=== GENRE RESEARCH: {genre} ===\n{research_reports.get('genre', '[no data]')}",
    ])
    specialist_block = "\n\n".join([
        f"=== MIXING ENGINEER ===\n{specialist_reports.get('mixing', '[no report]')}",
        f"=== DRUMS & PATTERNS ===\n{specialist_reports.get('drums', '[no report]')}",
        f"=== SOUND DESIGN & KEY ===\n{specialist_reports.get('sound_design', '[no report]')}",
        f"=== ARRANGEMENT ===\n{specialist_reports.get('arrangement', '[no report]')}",
    ])

    return f"""You are the lead producer coordinating a full review team for a {genre} beat
(reference: {reference}).

Your team ran in two phases:
- Phase 1: Two research agents gathered real-world context about the artist and genre.
- Phase 2: Four specialist agents analyzed the beat from their domains using that context.

Your job is to synthesize everything into one clean, structured final review.

Producer skill level: {skill['label']} — {skill['description']}
Tone guidance: {skill['tone']}

Detected BPM: {audio_data.get('bpm', 'unknown')}
Detected key: {audio_data.get('key', 'unknown')}

== Research Context ==
{research_block}

== Specialist Reports ==
{specialist_block}

== Synthesis rules ==
- Where specialists agree, state it ONCE confidently.
- Where they conflict, decide which issue has higher impact and say so explicitly.
- Use the research context to calibrate — is the beat actually close to the reference or far off?
- Do NOT paste reports in sequence. Write as one unified voice.
- Keep every section tight. Producers read fast.

== Output format — follow exactly ==

### 1. BPM & Tempo
### 2. Key & Sound Selection
### 3. Drums & Patterns
### 4. Mixing
### 5. Arrangement & Structure
### 6. Overall Score & Priority Fixes
(Score out of 10. Top 3 fixes in order of impact. One honest sentence on the beat's best quality.)
""".strip()


# ── Main entry point ──────────────────────────────────────────────────────────

async def run_agent_team(
    client: genai.Client,
    audio_file,
    genre: str,
    reference: str,
    genre_profile: dict,
    audio_data: dict,
    skill_level: str,
    library_prompt: str = "",
    drum_candidates_prompt: str = "",
) -> dict:
    """
    Three-phase agent pipeline:

    Phase 1 — Research agents run in parallel.
      They search the web for artist and genre context.
      This is what makes the feedback specific instead of generic.

    Phase 2 — Specialist agents run in parallel.
      Each gets the research context from Phase 1 injected into its prompt.
      They listen to the audio and give domain-focused feedback.

    Phase 3 — Coordinator.
      Reads all 6 reports (2 research + 4 specialist) and writes the final review.
    """
    skill = SKILL_LEVELS[skill_level]

    # ── Phase 1: Research ─────────────────────────────────────────────────────
    # Run both research agents at the same time.
    # They don't need the audio file — just web search.
    research_results: list[AgentResult] = await asyncio.gather(
        _run_research_agent(client, "Artist Research", "artist",
                            _artist_research_prompt(reference, genre)),
        _run_research_agent(client, "Genre Research",  "genre",
                            _genre_research_prompt(genre)),
    )
    research_reports = {r.key: r.report for r in research_results}

    # Combine both research outputs into one context block for the specialists
    research_context = (
        f"--- ARTIST: {reference} ---\n{research_reports['artist']}\n\n"
        f"--- GENRE: {genre} ---\n{research_reports['genre']}"
    )

    # ── Phase 2: Specialists ──────────────────────────────────────────────────
    # All 4 run in parallel. Each gets the research context injected.
    specialist_results: list[AgentResult] = await asyncio.gather(
        _run_agent(client, "Mixing Engineer",               "mixing",
                   _mixing_prompt(genre, audio_data, skill, research_context), audio_file),
        _run_agent(client, "Drums & Patterns Specialist",   "drums",
                   _drums_prompt(genre, genre_profile, audio_data, skill, research_context, library_prompt, drum_candidates_prompt), audio_file),
        _run_agent(client, "Sound Design & Key Specialist", "sound_design",
                   _sound_design_prompt(genre, reference, audio_data, skill, research_context, library_prompt), audio_file),
        _run_agent(client, "Arrangement Specialist",        "arrangement",
                   _arrangement_prompt(genre, audio_data, skill, research_context), audio_file),
    )
    specialist_reports = {r.key: r.report for r in specialist_results}

    # ── Phase 3: Coordinator ──────────────────────────────────────────────────
    # Synthesizes all 6 reports into the final review.
    coord_prompt = _coordinator_prompt(
        genre, reference, audio_data, skill, research_reports, specialist_reports
    )
    loop = asyncio.get_running_loop()
    final_review = await loop.run_in_executor(
        None, _call_gemini_sync, client, coord_prompt, audio_file
    )

    return {
        "research_reports": research_reports,
        "specialist_reports": specialist_reports,
        "final_review": final_review,
        "coordinator_prompt": coord_prompt,
    }
