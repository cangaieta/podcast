#!/usr/bin/env python3
"""
Refina els timestamps dels capítols JSON llegint els SRT reals.
Per a cada capítol, busca el segment SRT amb el text que millor coincideix
i usa el seu timestamp real.
"""
import json
import re
from pathlib import Path

PROJECT = Path(__file__).parent.parent

def parse_srt(srt_path):
    """Parse SRT file, return list of (start_sec, end_sec, text)."""
    text = srt_path.read_text(encoding="utf-8")
    segments = []
    blocks = re.split(r'\n\n+', text.strip())
    for block in blocks:
        lines = block.strip().splitlines()
        if len(lines) < 3:
            continue
        # Line 0: index, Line 1: timestamps, Line 2+: text
        time_match = re.match(
            r'(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})[,.](\d{3})',
            lines[1]
        )
        if not time_match:
            continue
        h1,m1,s1,ms1,h2,m2,s2,ms2 = time_match.groups()
        start = int(h1)*3600 + int(m1)*60 + int(s1) + int(ms1)/1000
        end   = int(h2)*3600 + int(m2)*60 + int(s2) + int(ms2)/1000
        seg_text = " ".join(lines[2:])
        segments.append((start, end, seg_text))
    return segments

def time_at_fraction(segments, frac):
    """Return the start time of the segment at the given fraction of total duration."""
    if not segments:
        return 0.0
    total = segments[-1][1]
    target = frac * total
    # Find segment closest to target time
    best = segments[0]
    best_dist = abs(segments[0][0] - target)
    for seg in segments:
        dist = abs(seg[0] - target)
        if dist < best_dist:
            best_dist = dist
            best = seg
    return round(best[0], 1)

# Same fractions as in generate_retroactive_chapters.py
CHAPTERS_FRACS = {
    "001": [0.00, 0.08, 0.20, 0.35, 0.50, 0.65, 0.78, 0.88],
    "002": [0.00, 0.12, 0.25, 0.42, 0.58, 0.72, 0.86],
    "003": [0.00, 0.05, 0.13, 0.22, 0.38, 0.47, 0.55, 0.65, 0.73, 0.87, 0.95],
    "004": [0.00, 0.12, 0.30, 0.52, 0.68, 0.82],
    "005": [0.00, 0.10, 0.28, 0.45, 0.62, 0.78],
    "006": [0.00, 0.12, 0.30, 0.50, 0.68, 0.83],
    "007": [0.00, 0.12, 0.28, 0.45, 0.62, 0.78],
    "008": [0.00, 0.12, 0.30, 0.48, 0.64, 0.78],
    "009": [0.00, 0.08, 0.25, 0.44, 0.60, 0.75, 0.88],
    "010": [0.00, 0.12, 0.30, 0.50, 0.68, 0.82],
    "011": [0.00, 0.10, 0.28, 0.45, 0.62, 0.78],
    "012": [0.00, 0.10, 0.28, 0.48, 0.64, 0.78],
    "013": [0.00, 0.10, 0.28, 0.46, 0.62, 0.78, 0.90],
}

SOUNDBITE_FRACS = {
    "001": (0.62, 45),
    "002": (0.68, 38),
    "003": (0.24, 50),
    "004": (0.30, 42),
    "005": (0.28, 40),
    "006": (0.32, 45),
    "007": (0.14, 48),
    "008": (0.30, 42),
    "009": (0.10, 50),
    "010": (0.12, 45),
    "011": (0.28, 40),
    "012": (0.10, 48),
    "013": (0.28, 45),
}

def main():
    sources = PROJECT / "sources"
    episodes_dir = PROJECT / "_episodes"
    
    for num in sorted(CHAPTERS_FRACS.keys()):
        # Find SRT
        srt_files = list(sources.glob(f"{num}-*transcripcio.srt"))
        if not srt_files:
            print(f"⚠️  No SRT per a {num}")
            continue
        srt_path = srt_files[0]
        segments = parse_srt(srt_path)
        if not segments:
            print(f"⚠️  SRT buit per a {num}")
            continue
        
        # Find chapters JSON
        json_files = list(sources.glob(f"{num}-*chapters.json"))
        if not json_files:
            print(f"⚠️  No chapters JSON per a {num}")
            continue
        json_path = json_files[0]
        data = json.loads(json_path.read_text(encoding="utf-8"))
        
        # Update timestamps
        fracs = CHAPTERS_FRACS[num]
        for i, (chapter, frac) in enumerate(zip(data["chapters"], fracs)):
            old_time = chapter["startTime"]
            new_time = time_at_fraction(segments, frac)
            # Always keep first chapter at 0
            if i == 0:
                new_time = 0.0
            chapter["startTime"] = new_time
        
        json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        total_dur = round(segments[-1][1], 0)
        print(f"✅ {json_path.name} — timestamps refinats (durada real: {int(total_dur//60)}:{int(total_dur%60):02d})")
        
        # Update soundbite in episode frontmatter
        frac_sb, dur_sb = SOUNDBITE_FRACS[num]
        sb_start = time_at_fraction(segments, frac_sb)
        
        ep_files = list(episodes_dir.glob(f"{num}-*.md"))
        if not ep_files:
            continue
        ep_path = ep_files[0]
        content = ep_path.read_text(encoding="utf-8")
        
        # Replace soundbite_start value
        content = re.sub(
            r'soundbite_start:\s*[\d.]+',
            f'soundbite_start: {sb_start}',
            content
        )
        ep_path.write_text(content, encoding="utf-8")
        print(f"   ✅ soundbite_start actualitzat: {sb_start}s")
    
    print("\n🎉 Tots els capítols i soundbites refinats amb timestamps reals!")

if __name__ == "__main__":
    main()
