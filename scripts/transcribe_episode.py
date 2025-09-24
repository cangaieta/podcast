#!/usr/bin/env python3
"""
Script per transcriure automàticament episodis de podcast i generar descripcions.

Ús:
    python scripts/transcribe_episode.py episodes/001-nom-episodi.mp3

Requereix:
    pip install -r requirements.txt
"""

import os
import sys
import whisper
import yaml
from datetime import datetime
from pathlib import Path
import argparse

def extract_episode_info_from_filename(mp3_path):
    """Extreu informació de l'episodi del nom del fitxer."""
    filename = Path(mp3_path).stem
    parts = filename.split('-')

    if len(parts) >= 2:
        episode_num = parts[0]
        title_parts = parts[1:]
        title_slug = '-'.join(title_parts)

        # Generar títol llegible
        title = ' '.join([part.capitalize() for part in title_parts])

        return {
            'number': episode_num,
            'slug': title_slug,
            'title': title,
            'filename': filename
        }

    return None

def transcribe_audio(audio_path, model_size="medium"):
    """Transcriu l'audio amb Whisper."""
    print(f"🎯 Carregant model Whisper ({model_size})...")
    model = whisper.load_model(model_size)

    print(f"🎙️  Transcrivint {audio_path}...")
    result = model.transcribe(audio_path, language="ca")

    return result

def generate_description(transcript, max_length=200):
    """Genera una descripció breu a partir de la transcripció."""
    # Primer paràgraf o primers 200 caràcters
    sentences = transcript.split('. ')
    description = sentences[0]

    # Si és massa llarg, tallar
    if len(description) > max_length:
        description = description[:max_length-3] + "..."

    return description

def create_episode_markdown(episode_info, transcript, description, output_dir="_episodes"):
    """Crea el fitxer markdown de l'episodi."""

    # Plantilla del fitxer markdown
    front_matter = {
        'title': f"Episodi {episode_info['number']}: {episode_info['title']}",
        'date': datetime.now().strftime('%Y-%m-%d'),
        'duration': "10:32",  # Caldrà actualitzar manualment
        'audio_file': f"{episode_info['filename']}.mp3",
        'description': description,
        'episode_number': int(episode_info['number']),
        'season': 1,
        'sources': [
            {
                'title': "Font principal",
                'description': "Actualitza amb les fonts reals utilitzades"
            }
        ]
    }

    markdown_content = f"""---
{yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)}---

## Introducció

*[Descripció generada automàticament. Revisa i personalitza segons calgui.]*

{description}

## Transcripció completa

{transcript}

## Fonts

*Actualitza aquesta secció amb les fonts reals utilitzades per generar el contingut amb Google NotebookLM.*

---

**Important:** Aquest episodi ha estat generat amb Google NotebookLM basant-se en fonts oficials. La transcripció s'ha generat automàticament amb OpenAI Whisper. Consulta sempre les fonts originals per obtenir la informació completa.
"""

    # Crear fitxer markdown
    os.makedirs(output_dir, exist_ok=True)
    markdown_path = os.path.join(output_dir, f"{episode_info['filename']}.md")

    with open(markdown_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    return markdown_path

def create_transcription_file(episode_info, transcript, output_dir="sources"):
    """Crea fitxer de transcripció a sources/"""
    os.makedirs(output_dir, exist_ok=True)
    transcript_path = os.path.join(output_dir, f"{episode_info['filename']}-transcripcio.txt")

    with open(transcript_path, 'w', encoding='utf-8') as f:
        f.write(f"Transcripció de l'episodi {episode_info['number']}\n")
        f.write(f"Generat automàticament amb OpenAI Whisper\n")
        f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        f.write(transcript)

    return transcript_path

def main():
    parser = argparse.ArgumentParser(description='Transcriu episodi de podcast')
    parser.add_argument('audio_file', help='Fitxer MP3 a transcriure')
    parser.add_argument('--model', default='medium',
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help='Model de Whisper a utilitzar')
    parser.add_argument('--output-episode', default='_episodes',
                       help='Directori per al fitxer markdown')
    parser.add_argument('--output-transcript', default='sources',
                       help='Directori per al fitxer de transcripció')

    args = parser.parse_args()

    if not os.path.exists(args.audio_file):
        print(f"❌ Error: No es troba el fitxer {args.audio_file}")
        sys.exit(1)

    # Extreure informació de l'episodi
    episode_info = extract_episode_info_from_filename(args.audio_file)
    if not episode_info:
        print("❌ Error: No es pot extreure informació del nom del fitxer")
        print("Format esperat: XXX-nom-episodi.mp3")
        sys.exit(1)

    print(f"📝 Processant episodi {episode_info['number']}: {episode_info['title']}")

    # Transcriure
    result = transcribe_audio(args.audio_file, args.model)
    transcript = result["text"]

    # Generar descripció
    description = generate_description(transcript)

    # Crear fitxers
    markdown_path = create_episode_markdown(episode_info, transcript, description, args.output_episode)
    transcript_path = create_transcription_file(episode_info, transcript, args.output_transcript)

    print(f"✅ Transcripció completada!")
    print(f"📄 Episodi: {markdown_path}")
    print(f"📝 Transcripció: {transcript_path}")
    print(f"\n🔧 Pròxims passos:")
    print(f"1. Revisa i edita {markdown_path}")
    print(f"2. Actualitza les fonts reals utilitzades")
    print(f"3. Ajusta la durada i altres metadades")
    print(f"4. Fes git add, commit i push")

if __name__ == "__main__":
    main()