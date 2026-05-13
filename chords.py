"""
Industry chord progression database.

Covers every genre in the app. Each entry has:
  - typical_scale   — what scale/mode dominates the genre
  - progressions    — list of common progressions with Roman numerals, feel, and artist examples
  - tips            — genre-specific harmonic advice for FL Studio

Roman numeral conventions used:
  i / I   = tonic (minor / major)
  bVII    = flat 7th (one whole tone below tonic)
  bVI     = flat 6th
  bIII    = flat 3rd
  bII     = flat 2nd (Phrygian — very dark)
  iv / IV = 4th degree chord
  V       = dominant (major 5th)
  maj7    = major 7th extension
  7       = dominant 7th extension
"""

PROGRESSIONS: dict[str, dict] = {

    "uk drill": {
        "typical_scale": "Natural minor (Aeolian), sometimes Phrygian for extra darkness",
        "modes": ["Aeolian — standard dark minor", "Phrygian — adds cold, tense feel (bII)"],
        "progressions": [
            {
                "name": "The Standard UK Drill Loop",
                "numerals": "i – bVII – bVI – bVII",
                "feel": "Brooding, repetitive, hypnotic. The most-used progression in the genre.",
                "artists": "Central Cee, Headie One, Unknown T, Digga D",
            },
            {
                "name": "Phrygian Tension",
                "numerals": "i – bII – i – bVII",
                "feel": "Cold and tense. The bII (flat 2nd) gives a Middle Eastern quality — popular in harder drill.",
                "artists": "Pop Smoke (NYC influence), darker Skepta era",
            },
            {
                "name": "Minor Resolution",
                "numerals": "i – bVI – bVII – i",
                "feel": "Resolves back to the tonic — slightly more melodic but still dark.",
                "artists": "Fredo, Loski",
            },
            {
                "name": "Extended Dark Loop",
                "numerals": "i – bVII – iv – bVI",
                "feel": "More harmonic movement than the standard loop — feels musical without losing the dark energy.",
                "artists": "Dave, Stormzy drill-influenced work",
            },
        ],
        "tips": [
            "F# minor, B minor, and C# minor are the most common keys in UK drill.",
            "Keep it 2–4 chords, heavily looped. Repetition is the point.",
            "Avoid major 3rds — they sound too happy. Stick to minor triads and sus chords.",
            "Suspended chords (sus2, sus4) add ambiguity without brightness.",
        ],
    },

    "us drill": {
        "typical_scale": "Natural minor, chromatic minor",
        "modes": ["Aeolian", "harmonic minor (for V chord tension)"],
        "progressions": [
            {
                "name": "Chicago/NY Dark Minor",
                "numerals": "i – bVII – bVI – V",
                "feel": "Darker and more aggressive than UK drill. The major V creates tension.",
                "artists": "Chief Keef era, Pop Smoke, Fivio Foreign",
            },
            {
                "name": "Two-Chord Trap",
                "numerals": "i – bVII",
                "feel": "Minimal and hard. The simplest drill movement — all about the 808 and drums.",
                "artists": "Young Chop, DJ L Chicago era",
            },
            {
                "name": "Minor Descent",
                "numerals": "i – bVII – bVI – bVII",
                "feel": "Shared with UK drill but typically faster and more aggressive in US context.",
                "artists": "Pop Smoke, Sheff G",
            },
        ],
        "tips": [
            "Dark, minor key samples chopped over trap drums define the sound.",
            "Piano and strings are the go-to instruments.",
            "Keep chord voicings dense — power chords or full minor triads.",
        ],
    },

    "trap": {
        "typical_scale": "Natural minor, minor pentatonic",
        "modes": ["Aeolian", "Dorian for slightly warmer minor"],
        "progressions": [
            {
                "name": "Classic Trap Minor",
                "numerals": "i – bVII – bVI – bVII",
                "feel": "The most universal trap progression. Dark and looping.",
                "artists": "Metro Boomin, Southside, TM88, Zaytoven",
            },
            {
                "name": "Atmospheric Vamp",
                "numerals": "i (sustained with melodic movement above)",
                "feel": "Single chord — melody creates the harmonic interest, not the chords. Very modern.",
                "artists": "Playboi Carti era, Travis Scott dark beats",
            },
            {
                "name": "Emotional Trap",
                "numerals": "bVI – bVII – i – bVII",
                "feel": "Sadder and more melodic. Associated with the SoundCloud/emo rap era.",
                "artists": "Juice WRLD type, XXXTentacion influenced",
            },
            {
                "name": "Dorian Warmth",
                "numerals": "i – IV – bVII – IV",
                "feel": "Slightly brighter than pure Aeolian — the natural IV (Dorian) gives warmth.",
                "artists": "Future melodic era, Young Thug",
            },
        ],
        "tips": [
            "808 bass lines often play the same movement as the chord progression — keep them in key.",
            "Chord stabs (short rhythmic hits) work better than sustained pads in most trap.",
            "Layering a piano with a darker synth pad is a genre staple.",
        ],
    },

    "melodic trap": {
        "typical_scale": "Minor for dark, major for emotional crossover",
        "modes": ["Aeolian", "Major (I–V–vi–IV)", "Lydian for dreamy feel"],
        "progressions": [
            {
                "name": "Cinematic Emotional Minor",
                "numerals": "i – bVI – bIII – bVII",
                "feel": "Quintessential melodic trap — building, emotional, cinematic.",
                "artists": "Wheezy, Internet Money, Southside emotional era",
            },
            {
                "name": "Pop Crossover Major",
                "numerals": "I – V – vi – IV",
                "feel": "Major key — optimistic but bittersweet depending on the melody. Universally melodic.",
                "artists": "Gunna lighter work, Young Thug pop crossovers",
            },
            {
                "name": "Aeolian Climb",
                "numerals": "i – bIII – bVII – bVI",
                "feel": "Ascending motion — builds emotional tension and release.",
                "artists": "Lil Baby type beats, Rod Wave influenced",
            },
        ],
        "tips": [
            "Lush, sustained chords work best — let them breathe with long reverb tails.",
            "Counter-melodies (a second melodic line against the hook) are very common.",
            "Chord stacks (layering multiple synth pads on the same chord) create the big emotional sound.",
        ],
    },

    "hip hop": {
        "typical_scale": "Minor, minor pentatonic, sampled harmony",
        "modes": ["Aeolian", "Dorian", "minor pentatonic"],
        "progressions": [
            {
                "name": "Classic Hip Hop Minor",
                "numerals": "i – bVII – bVI – bVII",
                "feel": "Timeless and universal. Works from the 90s to today.",
                "artists": "Dr. Dre, Kanye West, Jay-Z era production",
            },
            {
                "name": "Dorian Soul",
                "numerals": "i – IV",
                "feel": "Two-chord Dorian vamp. The natural IV in a minor context gives deep warmth.",
                "artists": "Kendrick Lamar era, Sounwave, No I.D.",
            },
            {
                "name": "West Coast Bounce",
                "numerals": "I – IV – V",
                "feel": "Major key — bright and bouncy. G-funk influenced.",
                "artists": "Dr. Dre west coast era, DJ Quik",
            },
            {
                "name": "Jazz Minor ii-V-i",
                "numerals": "ii° – V – i",
                "feel": "Sophisticated jazz-influenced hip hop. Resolves with purpose.",
                "artists": "Pete Rock, DJ Premier, Large Professor",
            },
        ],
        "tips": [
            "Samples often define the harmonic content — work with what the sample gives you.",
            "Bass lines that counter the chord movement add depth and character.",
            "Simple progressions with interesting rhythmic placement beat complex ones.",
        ],
    },

    "boom bap": {
        "typical_scale": "Minor, modal jazz, soulful",
        "modes": ["Aeolian", "Dorian", "Mixolydian for brighter feel"],
        "progressions": [
            {
                "name": "Jazz Minor Turnaround",
                "numerals": "ii° – V – i",
                "feel": "Sophisticated, soulful, jazz-rooted. The gold standard of boom bap harmony.",
                "artists": "Pete Rock, DJ Premier, Nas-era production",
            },
            {
                "name": "Soulful Sample Loop",
                "numerals": "i – iv – bVII – bIII",
                "feel": "Warm and nostalgic. Common in sample-based production.",
                "artists": "J Dilla, Madlib, 9th Wonder",
            },
            {
                "name": "Blues Minor",
                "numerals": "i – iv – i – V",
                "feel": "Blues-derived, gritty and real.",
                "artists": "Gang Starr era, early 90s East Coast",
            },
        ],
        "tips": [
            "Swing feel in the drums matters more than harmonic complexity.",
            "Major 6th and 9th chord extensions give a vintage soulful quality.",
            "Vinyl-sampled chords with natural high-frequency rolloff sit better in a boom bap mix.",
        ],
    },

    "r&b": {
        "typical_scale": "Major, Dorian minor, Mixolydian",
        "modes": ["Dorian (warm soulful minor)", "Mixolydian (major with flat 7)", "Major"],
        "progressions": [
            {
                "name": "Neo Soul Jazz Vamp",
                "numerals": "i7 – IV7 – bVII7 – III7",
                "feel": "Rich and jazzy. The 7th extensions are essential — plain triads sound thin here.",
                "artists": "D'Angelo, Erykah Badu, H.E.R., Thundercat",
            },
            {
                "name": "Modern R&B Loop",
                "numerals": "I – iii – vi – IV",
                "feel": "Contemporary. Slightly bittersweet even in major — very versatile.",
                "artists": "SZA, Summer Walker, Bryson Tiller",
            },
            {
                "name": "Classic ii-V-I",
                "numerals": "ii7 – V7 – Imaj7",
                "feel": "Jazz-influenced smooth resolution. Timeless.",
                "artists": "Classic R&B, Ne-Yo era, Frank Ocean chord work",
            },
            {
                "name": "Slow Jam Flow",
                "numerals": "I – IV – vi – V",
                "feel": "Smooth and flowing. Classic slow jam movement.",
                "artists": "Classic R&B, Chris Brown slower era",
            },
        ],
        "tips": [
            "Extended chords (maj7, min7, dom7, 9th, 11th) are essential in R&B — basic triads sound flat.",
            "Voice leading (smooth note movement between chords) is what separates good R&B from great.",
            "Rhodes, Wurlitzer, and clean electric piano are the go-to harmonic instruments.",
        ],
    },

    "afrobeats": {
        "typical_scale": "Major, minor pentatonic, Mixolydian",
        "modes": ["Major (most common)", "Mixolydian", "minor pentatonic for darker feel"],
        "progressions": [
            {
                "name": "Afrobeats Major Loop",
                "numerals": "I – IV – V – IV",
                "feel": "Bright, energetic, uplifting. The most common commercial afrobeats movement.",
                "artists": "Burna Boy, Wizkid, Davido",
            },
            {
                "name": "Afropop Smooth",
                "numerals": "I – vi – IV – V",
                "feel": "Slightly more melancholic major feel — bittersweet and melodic.",
                "artists": "Tems-influenced, Afrobeats crossover acts",
            },
            {
                "name": "Highlife Influence",
                "numerals": "I – II – IV – I",
                "feel": "Traditional West African highlife DNA — bright and rhythmically driven.",
                "artists": "Mr. Eazi, Fela-inspired productions",
            },
        ],
        "tips": [
            "Major keys are the norm — keep it uplifting.",
            "Percussion drives afrobeats more than harmony — chords support, rhythm leads.",
            "Melodic guitar or piano loops often carry the harmonic movement.",
        ],
    },

    "afro drill": {
        "typical_scale": "Natural minor with Afrobeats melodic inflections",
        "modes": ["Aeolian", "pentatonic minor"],
        "progressions": [
            {
                "name": "Afro Drill Dark Loop",
                "numerals": "i – bVII – bVI – bVII",
                "feel": "UK drill foundation with Afrobeats melodic character on top.",
                "artists": "Rema darker work, UK Afro drill scene",
            },
            {
                "name": "African Minor Melody",
                "numerals": "i – iv – bVII – bVI",
                "feel": "More melodic movement — the African melodic sensibility over drill drums.",
                "artists": "Emerging UK Afro drill artists",
            },
        ],
        "tips": [
            "The melody carries the Afrobeats identity — make sure it has that warm, vocal-like quality.",
            "Minor key but with brighter melodic ornaments than pure UK drill.",
        ],
    },

    "amapiano": {
        "typical_scale": "Major, minor, gospel-influenced jazz",
        "modes": ["Major", "Dorian", "gospel harmony with 7ths and 9ths"],
        "progressions": [
            {
                "name": "Gospel-Influenced Major",
                "numerals": "I – IV – vi – V",
                "feel": "Uplifting and spiritual. Gospel roots are strong in amapiano.",
                "artists": "DJ Maphorisa, Kabza De Small, DBN Gogo",
            },
            {
                "name": "Deep Amapiano",
                "numerals": "i – iv – bVII – bIII",
                "feel": "Deeper, more underground feel. Influenced by deep house.",
                "artists": "Underground amapiano, late-night sets",
            },
            {
                "name": "Log Drum Vamp",
                "numerals": "I – iii – IV – V",
                "feel": "The log drum bass line drives this — chords float above with jazzy extensions.",
                "artists": "Focalistic, commercial amapiano",
            },
        ],
        "tips": [
            "The log drum (low synth bass) plays a melodic line — keep it in key with the chords.",
            "Add 9ths and 13ths to piano chords for that jazz/gospel richness.",
            "Call and response between piano and log drum is the defining harmonic characteristic.",
        ],
    },

    "dancehall": {
        "typical_scale": "Major, minor, reggae-influenced",
        "modes": ["Major (most common)", "Mixolydian", "minor for darker riddims"],
        "progressions": [
            {
                "name": "Classic Riddim",
                "numerals": "I – IV – V – IV",
                "feel": "Bright and bouncy. The foundation of dancehall harmonic movement.",
                "artists": "Classic dancehall riddims, Vybz Kartel era",
            },
            {
                "name": "Minor Riddim",
                "numerals": "i – bVII – bVI – V",
                "feel": "Darker dancehall — more intense and aggressive.",
                "artists": "Darker riddim compilations, Popcaan",
            },
        ],
        "tips": [
            "The one-drop rhythm (kick on beat 3 only) defines dancehall — chords follow that groove.",
            "Bass is crucial and usually plays a melodic counter-line.",
            "Major keys dominate commercial dancehall.",
        ],
    },

    "reggaeton": {
        "typical_scale": "Minor, minor pentatonic",
        "modes": ["Aeolian", "minor pentatonic"],
        "progressions": [
            {
                "name": "Reggaeton Minor Standard",
                "numerals": "i – bVII – bVI – bVII",
                "feel": "Standard urban Latin movement over the dembow rhythm.",
                "artists": "Bad Bunny, J Balvin, Daddy Yankee",
            },
            {
                "name": "Latin Romantic Minor",
                "numerals": "i – bVI – bIII – bVII",
                "feel": "More melodic and romantic — common in slower reggaeton.",
                "artists": "Ozuna, Maluma romantic era",
            },
        ],
        "tips": [
            "The dembow rhythm (kick-snare-kick-kick pattern) is everything — chords serve it.",
            "Minor keys with Latin percussion flavour are the standard.",
            "Synthesizer bass lines typically double the chord root notes.",
        ],
    },

    "latin trap": {
        "typical_scale": "Minor, trap-influenced",
        "modes": ["Aeolian", "Phrygian for extra tension"],
        "progressions": [
            {
                "name": "Latin Trap Dark",
                "numerals": "i – bVII – bVI – bVII",
                "feel": "Standard trap movement with Latin melodic character.",
                "artists": "Bad Bunny trap era, Anuel AA, Jhay Cortez",
            },
            {
                "name": "Phrygian Latin",
                "numerals": "i – bII – bVII – i",
                "feel": "Dark and tense with a Spanish/Flamenco quality from the bII.",
                "artists": "Darker Latin trap, urban Latin artists",
            },
        ],
        "tips": [
            "Blend trap drum patterns with Latin percussion elements.",
            "Minor keys, fast trap hi-hats, and melodic 808s define the sound.",
        ],
    },

    "phonk": {
        "typical_scale": "Natural minor, minor pentatonic",
        "modes": ["Aeolian", "Phrygian for coldest feel", "minor pentatonic"],
        "progressions": [
            {
                "name": "Memphis Dark Loop",
                "numerals": "i – bVII – bVI – v",
                "feel": "Dark, hypnotic, slow-burning. The descending movement is characteristic.",
                "artists": "DJ Smokey, Night Lovell, $uicideboy$",
            },
            {
                "name": "Phonk Minimal Vamp",
                "numerals": "i – iv – i – v",
                "feel": "Two-chord vamp with minimal movement — all about the atmosphere.",
                "artists": "Memphis rap samples reworked, Ghostemane era",
            },
            {
                "name": "Cowbell Loop",
                "numerals": "i – bVII – i – bVII",
                "feel": "Back-and-forth between tonic and flat 7. Hypnotic with the cowbell groove.",
                "artists": "Internet phonk, drifting phonk subgenre",
            },
        ],
        "tips": [
            "C minor, D minor, F minor are the most common phonk keys.",
            "Slow movement and heavy repetition matter more than harmonic complexity.",
            "Sample chops and pitch manipulation often replace traditional chord playing.",
        ],
    },

    "lo-fi hip hop": {
        "typical_scale": "Minor, major with jazz extensions",
        "modes": ["Dorian (warm minor)", "Major", "Lydian (dreamy, raised 4th)"],
        "progressions": [
            {
                "name": "Lo-Fi Jazz Loop",
                "numerals": "IVmaj7 – iii7 – vi7 – ii7",
                "feel": "Jazzy, warm, nostalgic. The 7th extensions are non-negotiable.",
                "artists": "Nujabes, J Dilla lo-fi era, ChilledCow aesthetic",
            },
            {
                "name": "Rainy Day Minor",
                "numerals": "i7 – bVImaj7 – bVII – i7",
                "feel": "Melancholic but comforting. The lo-fi study music archetype.",
                "artists": "Standard lo-fi hip hop playlists, Idealism",
            },
            {
                "name": "Dorian Warmth",
                "numerals": "i – IV – i – IV",
                "feel": "Simple Dorian vamp. The major IV in minor context gives warmth without sadness.",
                "artists": "Kiefer-influenced, soulful lo-fi",
            },
        ],
        "tips": [
            "7th and 9th chord extensions are essential — plain triads sound too harsh.",
            "Slightly detuned or tape-saturated piano sits better in a lo-fi mix.",
            "Chord inversions (e.g. first inversion) create smoother voice leading.",
        ],
    },

    "cloud rap": {
        "typical_scale": "Minor, washed-out and ambient",
        "modes": ["Aeolian", "minor pentatonic", "Mixolydian for ethereal feel"],
        "progressions": [
            {
                "name": "Hazy Minor Drift",
                "numerals": "i – bVI – bVII – i",
                "feel": "Slow, spacey, washed in reverb. The movement barely registers — it floats.",
                "artists": "Bones, Xavier Wulf, Edgy era cloud rap",
            },
            {
                "name": "Ethereal Vamp",
                "numerals": "i – bVII (sustained)",
                "feel": "Two chords held for a long time. Atmosphere over movement.",
                "artists": "Yung Lean early era, Bladee",
            },
        ],
        "tips": [
            "Heavy reverb and delay on chords are essential — the chords should feel distant.",
            "Keep movement minimal — repetition and atmosphere define the genre.",
            "Pitch-shifted vocal samples used as harmonic texture rather than melody.",
        ],
    },

    "pluggnb": {
        "typical_scale": "Minor, R&B-influenced",
        "modes": ["Aeolian", "Dorian"],
        "progressions": [
            {
                "name": "Plug R&B Minor",
                "numerals": "i – bVI – bVII – i",
                "feel": "Slow, melodic, half-time. R&B melody over trap-influenced production.",
                "artists": "Yeat influenced, Autumn!",
            },
            {
                "name": "Neo Soul Plug",
                "numerals": "i7 – iv7 – bVII – bVI",
                "feel": "More harmonic depth — the 7th extensions give it an R&B richness.",
                "artists": "Melodic plugg producers",
            },
        ],
        "tips": [
            "Slow BPM and half-time drums — the chords need to breathe.",
            "R&B-influenced chord voicings (7ths, 9ths) over minimal trap production.",
        ],
    },

    "detroit rap": {
        "typical_scale": "Minor, dark and cinematic",
        "modes": ["Aeolian", "harmonic minor for tension"],
        "progressions": [
            {
                "name": "Detroit Dark Minor",
                "numerals": "i – bVII – bVI – v",
                "feel": "Knocking, dark, cinematic. The minor v (lowercase) keeps tension without full resolution.",
                "artists": "Big Sean darker work, Sada Baby, Detroit producers",
            },
            {
                "name": "Cinematic Sample Chop",
                "numerals": "i – bIII – iv – bVII",
                "feel": "Sample-influenced, cinematic movement. Feels like a film score over knocking drums.",
                "artists": "Detroit street rap aesthetic",
            },
        ],
        "tips": [
            "Dark, cinematic samples define the sound — the harmonic content often comes from the sample.",
            "Knocking drums with deep bass — the groove is the priority.",
        ],
    },

    "hyperpop": {
        "typical_scale": "Major, minor, often ignored in favour of melody",
        "modes": ["Major (bright, maximalist)", "minor (dark hyperpop)"],
        "progressions": [
            {
                "name": "Hyperpop Major Blast",
                "numerals": "I – V – vi – IV",
                "feel": "Maximalist pop — huge, distorted, hyper-energetic.",
                "artists": "100 gecs, Charli XCX, Sophie influenced",
            },
            {
                "name": "Dark Hyperpop",
                "numerals": "i – bVI – bVII – i",
                "feel": "Minor key with distorted production on top. Intense and overwhelming.",
                "artists": "Bladee, Ecco2k, darker DRAIN GANG",
            },
        ],
        "tips": [
            "Distortion and saturation on chords is part of the sound — don't clean it up.",
            "Pitch-shifted vocals and extreme processing are harmonic elements in hyperpop.",
            "Push the chords to the extreme — hyperpop is maximalist by design.",
        ],
    },

    "future bass": {
        "typical_scale": "Major, sometimes minor for contrast drops",
        "modes": ["Major (bright EDM feel)", "minor for drops"],
        "progressions": [
            {
                "name": "Future Bass Build",
                "numerals": "I – V – vi – IV",
                "feel": "Uplifting and emotional. The supersaw chords swell with this progression.",
                "artists": "Flume, San Holo, What So Not",
            },
            {
                "name": "Emotional Drop",
                "numerals": "vi – IV – I – V",
                "feel": "Starting on the vi gives a bittersweet quality before resolving — great for drops.",
                "artists": "Marshmello emotional work, Illenium",
            },
        ],
        "tips": [
            "Supersaw chord stabs with heavy sidechain compression define future bass.",
            "Major key dominates — the emotion comes from the chords swelling, not from darkness.",
            "Chord voicings should be wide and lush — use Sytrus or Harmor for the supersaw stack.",
        ],
    },

    "hard trap": {
        "typical_scale": "Minor, chromatic, industrial",
        "modes": ["Aeolian", "Phrygian", "chromatic/atonal for maximum aggression"],
        "progressions": [
            {
                "name": "Aggressive Minor",
                "numerals": "i – bII – bVII – i",
                "feel": "The bII creates maximum tension — cold, industrial, aggressive.",
                "artists": "Travis Scott darker era, Playboi Carti Whole Lotta Red",
            },
            {
                "name": "Dystopian Loop",
                "numerals": "i – bVII – bVI – bVII",
                "feel": "Standard dark minor made harder by distorted sounds and aggressive drums.",
                "artists": "Hard trap producers, underground rap",
            },
        ],
        "tips": [
            "Distorted 808s and layered kicks are the priority — chords serve the aggression.",
            "Minor keys, preferably with Phrygian inflections (bII) for maximum darkness.",
            "Industrial sounds and noise used as harmonic texture.",
        ],
    },

    "jersey club": {
        "typical_scale": "Minor, major, whatever the sample gives",
        "modes": ["Minor (darker tracks)", "Major (energetic club tracks)"],
        "progressions": [
            {
                "name": "Jersey Club Loop",
                "numerals": "i – bVII – bVI – bVII",
                "feel": "Standard minor loop repurposed for the fast jersey club energy.",
                "artists": "DJ Sliink, Uniiqu3, DJ Jayhood",
            },
        ],
        "tips": [
            "Jersey club is more about rhythm and vocal chops than complex harmony.",
            "Keep chord content simple — the drum pattern carries the energy.",
            "Vocal samples often define the harmonic content more than synthesized chords.",
        ],
    },
}

# Fallback for genres not explicitly in the database
_DEFAULT = {
    "typical_scale": "Minor (most genres) or Major (brighter genres)",
    "modes": ["Aeolian (natural minor)", "Major"],
    "progressions": [
        {
            "name": "Universal Minor Loop",
            "numerals": "i – bVII – bVI – bVII",
            "feel": "Works across most urban genres. Dark and melodic.",
            "artists": "Widespread across hip hop, trap, drill, and derivatives",
        },
        {
            "name": "Universal Pop Major",
            "numerals": "I – V – vi – IV",
            "feel": "The most common pop/crossover progression. Works in almost any genre.",
            "artists": "Pop crossover, melodic trap, R&B",
        },
    ],
    "tips": [
        "Match the emotional tone of the genre — dark genres = minor, uplifting genres = major.",
        "Keep progressions short and loop-friendly: 2–4 chords.",
    ],
}


def get_chord_data(genre: str) -> dict:
    return PROGRESSIONS.get(genre.lower().strip(), _DEFAULT)


def format_for_prompt(genre: str, detected_key: str = "") -> str:
    """
    Format the chord database entry for a genre into a readable block
    for the Sound Design agent prompt.
    """
    data = get_chord_data(genre)

    lines = [f"== Industry chord progressions for {genre} =="]

    if detected_key:
        lines.append(
            f"Detected key: {detected_key}\n"
            f"Translate the Roman numeral progressions below into this key "
            f"when advising the producer — give them the actual chord names to play in FL Studio."
        )

    lines.append(f"\nTypical scale: {data['typical_scale']}")

    if data.get("modes"):
        lines.append(f"Common modes: {' | '.join(data['modes'])}")

    lines.append("\nTop progressions used in the industry:")
    for p in data.get("progressions", []):
        lines.append(f"\n  [{p['name']}]")
        lines.append(f"  Numerals : {p['numerals']}")
        lines.append(f"  Feel     : {p['feel']}")
        if p.get("artists"):
            lines.append(f"  Artists  : {p['artists']}")

    if data.get("tips"):
        lines.append("\nHarmonic tips specific to this genre:")
        for tip in data["tips"]:
            lines.append(f"  · {tip}")

    lines.append(
        "\nInstructions: Identify what chord progression the beat is using (by ear). "
        "Compare it to the progressions above. Tell the producer whether it fits the genre, "
        "and if not, give them specific alternative chords to try — transposed to the detected key."
    )

    return "\n".join(lines)
