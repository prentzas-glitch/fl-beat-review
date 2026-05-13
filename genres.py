GENRE_PROFILES = {
    "uk drill":      {"bpm_range": (130, 145), "drum_feel": "half-time, heavy 808 slides, sparse snares on 3, rolling hi-hats with triplet ghost notes"},
    "us drill":      {"bpm_range": (138, 145), "drum_feel": "trap hi-hat rolls, punchy 808, snare on 2 and 4, dark minor melodies"},
    "trap":          {"bpm_range": (130, 170), "drum_feel": "rapid hi-hat triplets, booming 808, snappy claps, layered percs"},
    "hip hop":       {"bpm_range": (80, 110),  "drum_feel": "boom bap kick-snare, sampled breaks, laid-back swing feel"},
    "boom bap":      {"bpm_range": (85, 100),  "drum_feel": "punchy kick on 1 and 3, snare on 2 and 4, vinyl-textured samples, minimal 808"},
    "melodic trap":  {"bpm_range": (130, 155), "drum_feel": "soft 808 melodies, airy hi-hats, emotional chord stacks, light snare"},
    "afrobeats":     {"bpm_range": (95, 115),  "drum_feel": "syncopated kick patterns, percussive layers, rhythmic melodic loops"},
    "phonk":         {"bpm_range": (130, 160), "drum_feel": "cowbell-driven groove, Memphis chopped samples, distorted 808, dark trap hi-hat patterns"},
    "jersey club":   {"bpm_range": (130, 140), "drum_feel": "rapid kick triplets, call-and-response vocal chops, snappy snares, hi-energy percussion"},
    "pluggnb":       {"bpm_range": (55, 75),   "drum_feel": "half-time feel, slow melodic 808s, trap-influenced R&B crossover, minimal sparse drums"},
    "cloud rap":     {"bpm_range": (60, 90),   "drum_feel": "airy washed-out drums, heavy reverb on everything, spacey lo-fi atmosphere"},
    "lo-fi hip hop": {"bpm_range": (70, 90),   "drum_feel": "swinging dusty breaks, vinyl crackle texture, mellow chords, laid-back Rhodes or piano"},
    "r&b":           {"bpm_range": (60, 100),  "drum_feel": "smooth groove, live-sounding drums, soulful chords, warm bass, lush layering"},
    "dancehall":     {"bpm_range": (95, 110),  "drum_feel": "one-drop rhythm, heavy bass, syncopated hi-hats, riddim patterns"},
    "reggaeton":     {"bpm_range": (90, 100),  "drum_feel": "dembow rhythm (kick-snare-kick-kick), heavy low end, looping percussion"},
    "latin trap":    {"bpm_range": (130, 150), "drum_feel": "trap drums with reggaeton dembow influence, 808s, percussive Latin elements"},
    "afro drill":    {"bpm_range": (130, 145), "drum_feel": "UK drill half-time pattern with Afrobeats percussion layered, melodic minor, heavy slides"},
    "amapiano":      {"bpm_range": (110, 116), "drum_feel": "log drum bassline, shuffled open hi-hats, jazzy piano chords, deep house groove"},
    "detroit rap":   {"bpm_range": (70, 95),   "drum_feel": "knocking drums, dark synths, sample-heavy, minimal but hard-hitting patterns"},
    "hyperpop":      {"bpm_range": (140, 175), "drum_feel": "hyper-compressed glitchy drums or 4-on-the-floor, pitch-shifted vocals, heavily distorted 808"},
    "future bass":   {"bpm_range": (140, 160), "drum_feel": "four-on-the-floor kick, supersaw chords with heavy sidechain pumping, bright synths, emotional drops"},
    "hard trap":     {"bpm_range": (135, 165), "drum_feel": "distorted 808, aggressive layered kicks, fast hi-hat rolls, industrial textures"},
}

SKILL_LEVELS = {
    "beginner": {
        "label": "Beginner",
        "description": "new to production, needs plain-English explanations and step-by-step guidance",
        "tone": (
            "- Use plain, simple English. Avoid jargon — if you must use a technical term, explain it in one sentence.\n"
            "- Be encouraging. Frame feedback as 'here's what to try' not 'this is wrong'.\n"
            "- Explain what each plugin does before giving settings.\n"
            "- Give step-by-step instructions (e.g. 'Open Parametric EQ 2 on the mixer channel → click band 3 → set frequency to 200 Hz → drag gain to -3 dB').\n"
            "- Keep each point short and concrete. One thing at a time."
        ),
    },
    "intermediate": {
        "label": "Intermediate",
        "description": "knows FL Studio basics, wants technique-focused feedback",
        "tone": (
            "- Assume the producer knows their way around FL Studio and understands basic mixing concepts.\n"
            "- Be direct. Skip plugin explanations — go straight to settings.\n"
            "- Explain why a fix works in one sentence max per point.\n"
            "- Give exact values (frequencies, dB, ratios, ms) without hand-holding."
        ),
    },
    "advanced": {
        "label": "Advanced",
        "description": "experienced FL Studio producer, wants dense technical feedback with no hand-holding",
        "tone": (
            "- Treat the producer as a peer. Be concise and dense — skip all basics.\n"
            "- No plugin explanations. Just settings and decisions.\n"
            "- Challenge creative choices if they genuinely don't work — be honest and direct.\n"
            "- Focus on nuance: subtle compression decisions, frequency masking, stereo field issues, phase, transient shaping.\n"
            "- Mention parallel processing, mid-side techniques, and advanced routing where relevant."
        ),
    },
}
