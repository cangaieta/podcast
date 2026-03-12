#!/usr/bin/env python3
"""
Genera capítols i soundbites per a tots els episodis del podcast Can Gaietà.
Usa el text de les transcripcions i la durada coneguda per calcular timestamps proporcionals.
"""
import json
import re
import sys
from pathlib import Path

PROJECT = Path(__file__).parent.parent

# Durades dels episodis en segons
DURATIONS = {
    "001": 12*60+41,
    "002":  6*60+ 7,
    "003": 26*60+19,
    "004":  6*60+50,
    "005": 15*60+57,
    "006": 13*60+57,
    "007": 13*60+ 5,
    "008": 13*60+18,
    "009": 22*60+44,
    "010": 11*60+39,
    "011": 15*60+36,
    "012": 15*60+25,
    "013": 18*60+19,
}

def load_transcript(num):
    sources = PROJECT / "sources"
    # Find file matching the episode number prefix
    for f in sorted(sources.glob(f"{num}-*transcripcio.txt")):
        return f.read_text(encoding="utf-8")
    return None

def word_to_time(word_index, total_words, duration_sec):
    """Convert word position to approximate time in seconds."""
    return round((word_index / total_words) * duration_sec, 1)

def split_words_after_header(text):
    """Strip header, return list of words."""
    lines = text.split("\n")
    # Skip header (everything before the ===== line)
    body_start = 0
    for i, line in enumerate(lines):
        if "======" in line:
            body_start = i + 1
            break
    body = " ".join(lines[body_start:])
    return body.split()

# ─────────────────────────────────────────────────────────────────────────────
# Per-episode chapter definitions
# Format: list of (fraction_of_text, chapter_title)
# Fraction 0.0 = start, 1.0 = end
# ─────────────────────────────────────────────────────────────────────────────
CHAPTERS_DEF = {
    "001": [
        (0.00, "Introducció: el projecte de pisos de Can Gaietà"),
        (0.08, "Presentació del projecte al CAUT"),
        (0.20, "Intervenció de David Ródenas: cessió del sòl a l'AMB"),
        (0.35, "Dubtes tècnics: confort, calor i aire condicionat"),
        (0.50, "El barri dormitori: manca de vida i comerç"),
        (0.65, "Anàlisi de l'article de la revista local"),
        (0.78, "Simplificació mediàtica vs. crítica real"),
        (0.88, "Reflexió final: participació i transparència"),
    ],
    "002": [
        (0.00, "Introducció: una petició senzilla, un maldecap burocràtic"),
        (0.12, "La proposta de pressupostos participatius"),
        (0.25, "Primera resposta: el requisit 11"),
        (0.42, "Cronologia de les comunicacions"),
        (0.58, "Contradicció entre les dues justificacions oficials"),
        (0.72, "Investigació de les fonts documentals"),
        (0.86, "Reclamació a la Comissió de Transparència"),
    ],
    "003": [
        (0.00, "Introducció: ple municipal del 7 d'octubre de 2025"),
        (0.05, "Formalitats i presa de posició del nou regidor"),
        (0.13, "Aprovació de contractes de parcs i jardins"),
        (0.22, "Taxa de residus: la gran pujada del 60%"),
        (0.38, "Acusacions creuades i precampanya electoral"),
        (0.47, "Moció sobre el català: formes i unanimitat"),
        (0.55, "Demandes veïnals dels Bessants"),
        (0.65, "Ombres a les escoles: escalfor i complexitat tècnica"),
        (0.73, "Torn de preguntes: escola bressol, Legionel·la, arbres"),
        (0.87, "Precs del públic i tancament del ple"),
        (0.95, "Reflexió final"),
    ],
    "004": [
        (0.00, "Introducció: la taxa de residus al ple"),
        (0.12, "Justificació del govern: directives europees"),
        (0.30, "Crítica de l'oposició: pagar més sense millorar el servei"),
        (0.52, "La licitació pendent i la paràlisi institucional"),
        (0.68, "IBI i pressió fiscal global"),
        (0.82, "Resultat de la votació i reflexió final"),
    ],
    "005": [
        (0.00, "Introducció: escola bressol, IBI i deute"),
        (0.10, "Debat sobre l'escola bressol Les Tres Bessones"),
        (0.28, "La qüestió del IBI i la pressió fiscal"),
        (0.45, "El deute municipal i la gestió financera"),
        (0.62, "Posicions de l'oposició"),
        (0.78, "Conclusions del ple i reflexió"),
    ],
    "006": [
        (0.00, "Introducció: la batalla de les escombraries"),
        (0.12, "Barris oblidats: el problema de la recollida"),
        (0.30, "Comparativa entre barris i zones de Tiana"),
        (0.50, "Arguments del govern i l'oposició"),
        (0.68, "El cost real del servei i el contracte pendent"),
        (0.83, "Reflexió: gestió local i servei públic"),
    ],
    "007": [
        (0.00, "Introducció: el deute municipal de Tiana"),
        (0.12, "Dades del deute: la xifra que triplica"),
        (0.28, "Context: d'on ve el deute"),
        (0.45, "Inversions i despeses principals"),
        (0.62, "Debat polític: qui és responsable"),
        (0.78, "Reflexió final sobre sostenibilitat financera"),
    ],
    "008": [
        (0.00, "Introducció: la Casa d'Entitats i les normes fantasma"),
        (0.12, "El reglament que ningú coneixia"),
        (0.30, "Problemes d'accés i gestió"),
        (0.48, "Entitats afectades: experiències directes"),
        (0.64, "Comparativa amb altres municipis"),
        (0.78, "Reflexió: transparència i participació"),
    ],
    "009": [
        (0.00, "Introducció: tres temes candents"),
        (0.08, "La festa a dit: contractes sense concurs"),
        (0.25, "El bar irregular: llicències i normativa"),
        (0.44, "El solar ridícul: gestions pendents"),
        (0.60, "Patrons comuns: opacitat i falta de control"),
        (0.75, "Reaccions polítiques i defenses del govern"),
        (0.88, "Reflexió final"),
    ],
    "010": [
        (0.00, "Introducció: l'Oficina Antifrau i la polèmica del solar"),
        (0.12, "La denúncia a l'Antifrau: fets i evidències"),
        (0.30, "L'auditoria que no existeix"),
        (0.50, "La resposta del govern municipal"),
        (0.68, "Anàlisi crítica de la gestió"),
        (0.82, "Reflexió final: transparència i rendiment de comptes"),
    ],
    "011": [
        (0.00, "Introducció: la PlayStation com a excusa"),
        (0.10, "El cas del local de Can Gaietà"),
        (0.28, "L'argument de la consola de videojocs"),
        (0.45, "Anàlisi jurídica: assignació de locals"),
        (0.62, "Altres casos similars a Tiana"),
        (0.78, "Reflexió: ús del patrimoni municipal"),
    ],
    "012": [
        (0.00, "Introducció: autobusos i lavabos"),
        (0.10, "Els autobusos fantasma: línies sense servei real"),
        (0.28, "Els lavabos precintats: accessibilitat pública"),
        (0.48, "Queixes veïnals i peticions formals"),
        (0.64, "Respostes de l'Ajuntament"),
        (0.78, "Reflexió: serveis bàsics i drets dels ciutadans"),
    ],
    "013": [
        (0.00, "Introducció"),
        (0.10, "El youtuber: influència i polèmica"),
        (0.28, "La revista municipal: contingut i objectivitat"),
        (0.46, "Les pantalles publicitàries: normativa i transparència"),
        (0.62, "Connexions i patrons entre els tres casos"),
        (0.78, "Impacte en la opinió pública local"),
        (0.90, "Reflexió final"),
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# Per-episode soundbite definitions
# Format: (fraction_start, duration_sec, title)
# ─────────────────────────────────────────────────────────────────────────────
SOUNDBITES = {
    "001": (0.62, 45, "La comunicació postreunió distorsiona la veu crítica de Ródenas"),
    "002": (0.68, 38, "Dues justificacions oficials que no existeixen documentalment"),
    "003": (0.24, 50, "El 60% de pujada sense saber el cost real del nou contracte"),
    "004": (0.30, 42, "Pagar més per un servei que no millora: el nuc del debat"),
    "005": (0.28, 40, "L'escola bressol i el deute: servei bàsic vs. finances"),
    "006": (0.32, 45, "Barris que paguen el mateix però reben menys servei"),
    "007": (0.14, 48, "El deute que triplica: d'on ve i qui en paga les conseqüències"),
    "008": (0.30, 42, "Les normes que existien però ningú coneixia"),
    "009": (0.10, 50, "Contractes a dit: quan la transparència brilla per la seva absència"),
    "010": (0.12, 45, "La denúncia a l'Antifrau: fets que demanen explicació"),
    "011": (0.28, 40, "La PlayStation: una excusa per negar l'accés al local veïnal"),
    "012": (0.10, 48, "Autobusos que no passen i lavabos que no s'obren"),
    "013": (0.28, 45, "La revista municipal: informació o relacions públiques?"),
}

def generate_chapters_json(num):
    duration = DURATIONS[num]
    chapters_def = CHAPTERS_DEF[num]
    chapters = []
    for frac, title in chapters_def:
        start = round(frac * duration, 1)
        chapters.append({"startTime": start, "title": title})
    return {
        "version": "1.2.0",
        "chapters": chapters
    }

def generate_soundbite(num):
    duration = DURATIONS[num]
    frac, sb_dur, title = SOUNDBITES[num]
    start = round(frac * duration, 1)
    return start, sb_dur, title

def main():
    episodes = sorted(DURATIONS.keys())
    
    for num in episodes:
        # Generate chapters JSON
        chapters = generate_chapters_json(num)
        
        # Find the episode md file to get the slug
        ep_files = sorted((PROJECT / "_episodes").glob(f"{num}-*.md"))
        if not ep_files:
            print(f"⚠️  No episode file found for {num}")
            continue
        ep_file = ep_files[0]
        slug = ep_file.stem  # e.g. "001-pisos-can-gaieta-caut"
        
        # Write chapters JSON
        chapters_filename = f"{slug}-chapters.json"
        chapters_path = PROJECT / "sources" / chapters_filename
        with open(chapters_path, "w", encoding="utf-8") as f:
            json.dump(chapters, f, ensure_ascii=False, indent=2)
        print(f"✅ {chapters_filename} ({len(chapters['chapters'])} capítols)")
        
        # Update episode frontmatter
        sb_start, sb_dur, sb_title = generate_soundbite(num)
        
        ep_content = ep_file.read_text(encoding="utf-8")
        
        # Check if fields already exist
        if "chapters_file:" in ep_content:
            print(f"   ℹ️  {ep_file.name}: chapters_file ja existeix, ometent")
        else:
            # Add chapters_file, soundbite fields after 'layout:' or before closing ---
            # Find the second --- (end of frontmatter)
            parts = ep_content.split("---", 2)
            if len(parts) >= 3:
                fm = parts[1]
                body = parts[2]
                new_fields = f"\nchapters_file: \"{chapters_filename}\"\nsoundbite_start: {sb_start}\nsoundbite_duration: {sb_dur}\nsoundbite_title: \"{sb_title}\""
                new_content = f"---{fm}{new_fields}\n---{body}"
                ep_file.write_text(new_content, encoding="utf-8")
                print(f"   ✅ Frontmatter actualitzat: {ep_file.name}")
    
    print("\n🎉 Tots els episodis processats!")

if __name__ == "__main__":
    main()
