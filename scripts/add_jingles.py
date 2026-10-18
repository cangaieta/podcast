#!/usr/bin/env python3
"""
Afegeix el jingle d'entrada al principi i el de sortida al final d'un episodi.

Cal fer-ho ABANS de transcriure (PAS 1b): així l'SRT, els capítols i el
soundbite ja es calculen sobre l'àudio definitiu. Si s'afegeixen després, tots
els temps queden desplaçats uns segons.

Què fa:
  - Mesura la sonoritat de l'episodi (LUFS) i hi iguala els jingles, perquè no
    sonin ni més forts ni més fluixos que les veus.
  - Munta: entrada + 0,4 s de silenci + episodi + 0,6 s de silenci + sortida,
    amb la mateixa freqüència, canals i bitrate que l'MP3 original.
  - Desa l'original a episodes/sense-jingles/ (episodes/ no va a git; és la
    nostra còpia per si mai cal refer-ho).
  - Marca l'MP3 amb l'etiqueta 'jingles' perquè no s'hi afegeixin mai dos cops.

Ús:
    python scripts/add_jingles.py --episodi 039
    python scripts/add_jingles.py episodes/039-nom-episodi.mp3
"""

import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRADA = os.path.join(ROOT, "assets", "audio", "jingle-entrada.wav")
SORTIDA = os.path.join(ROOT, "assets", "audio", "jingle-sortida.wav")
MARCA = "entrada+sortida v1"
SILENCI_ENTRADA = 0.4
SILENCI_SORTIDA = 0.6


def ffprobe(camí, entrades):
    out = subprocess.run(
        ["ffprobe", "-v", "quiet", "-of", "json", "-show_entries", entrades, camí],
        capture_output=True, text=True, check=True,
    ).stdout
    return json.loads(out)


def ja_te_jingles(camí):
    tags = ffprobe(camí, "format_tags").get("format", {}).get("tags", {})
    return any(k.lower() == "jingles" for k in tags)


def sonoritat(camí):
    """Sonoritat integrada (LUFS) amb el filtre loudnorm de ffmpeg."""
    err = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", camí, "-af", "loudnorm=print_format=json", "-f", "null", "-"],
        capture_output=True, text=True, check=True,
    ).stderr
    inici = err.rindex("{")
    dades = json.loads(err[inici:err.index("}", inici) + 1])
    return float(dades["input_i"])


def troba_mp3(episodi):
    trobats = glob.glob(os.path.join(ROOT, "episodes", f"{episodi.zfill(3)}-*.mp3"))
    if len(trobats) != 1:
        print(f"❌ Esperava un MP3 per a l'episodi {episodi} a episodes/, n'he trobat {len(trobats)}")
        sys.exit(1)
    return trobats[0]


def main():
    parser = argparse.ArgumentParser(description="Afegeix els jingles d'entrada i sortida a un episodi")
    parser.add_argument("mp3", nargs="?", help="Camí de l'MP3")
    parser.add_argument("--episodi", help="Número de l'episodi (ex: 039)")
    args = parser.parse_args()

    if not args.mp3 and not args.episodi:
        parser.error("cal un MP3 o --episodi")
    mp3 = args.mp3 or troba_mp3(args.episodi)

    for f in (mp3, ENTRADA, SORTIDA):
        if not os.path.isfile(f):
            print(f"❌ No existeix: {f}")
            sys.exit(1)

    if ja_te_jingles(mp3):
        print(f"⏭️  {os.path.basename(mp3)} ja té els jingles (etiqueta 'jingles'). No faig res.")
        return

    stream = ffprobe(mp3, "stream=sample_rate,channels,bit_rate")["streams"][0]
    sr, canals = int(stream["sample_rate"]), int(stream["channels"])
    kbps = max(64, round(int(stream.get("bit_rate", 128000)) / 1000))
    lufs = sonoritat(mp3)
    print(f"🎚️  {os.path.basename(mp3)}: {lufs:.1f} LUFS, {sr} Hz, {canals} canal(s), {kbps} kbps")

    # Còpia de l'original abans de tocar res
    copia_dir = os.path.join(os.path.dirname(mp3), "sense-jingles")
    os.makedirs(copia_dir, exist_ok=True)
    copia = os.path.join(copia_dir, os.path.basename(mp3))
    if not os.path.exists(copia):
        shutil.copy2(mp3, copia)
        print(f"💾 Original desat a {os.path.relpath(copia, ROOT)}")

    layout = "mono" if canals == 1 else "stereo"
    fmt = f"aformat=sample_rates={sr}:channel_layouts={layout}"
    norm = f"loudnorm=I={lufs:.1f}:TP=-2:LRA=7,{fmt}"
    filtre = (
        f"[0:a]{norm}[ent];"
        f"[2:a]{norm}[sor];"
        f"[1:a]{fmt}[epi];"
        f"anullsrc=r={sr}:cl={layout}:d={SILENCI_ENTRADA}[s1];"
        f"anullsrc=r={sr}:cl={layout}:d={SILENCI_SORTIDA}[s2];"
        f"[ent][s1][epi][s2][sor]concat=n=5:v=0:a=1[out]"
    )

    with tempfile.NamedTemporaryFile(suffix=".mp3", dir=os.path.dirname(mp3), delete=False) as tmp:
        sortida = tmp.name
    try:
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", ENTRADA, "-i", mp3, "-i", SORTIDA,
             "-filter_complex", filtre, "-map", "[out]", "-map_metadata", "1",
             "-metadata", f"jingles={MARCA}", "-id3v2_version", "3",
             "-c:a", "libmp3lame", "-b:a", f"{kbps}k", sortida],
            check=True,
        )
        os.replace(sortida, mp3)
    finally:
        if os.path.exists(sortida):
            os.remove(sortida)

    durada = float(ffprobe(mp3, "format=duration")["format"]["duration"])
    print(f"✅ Jingles afegits: {os.path.relpath(mp3, ROOT)} ({int(durada // 60)}:{int(durada % 60):02d})")


if __name__ == "__main__":
    main()
