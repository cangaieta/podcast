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

def transcribe_audio_whisper_original(audio_path, model_size="medium"):
    """Transcriu l'audio amb openai-whisper (CPU/CUDA)."""
    import torch

    # NOTE: MPS (Apple Silicon) té problemes de compatibilitat amb Whisper
    # Error: "Could not run 'aten::empty.memory_format' with arguments from the 'SparseMPS' backend"
    # Per ara, forcem CPU que és més estable

    # Detectar dispositiu (CUDA per NVIDIA, CPU per defecte)
    if torch.cuda.is_available():
        device = "cuda"
        print(f"🚀 Usant acceleració GPU (CUDA)")
    else:
        device = "cpu"
        if torch.backends.mps.is_available():
            print(f"💻 Usant CPU (MPS/Apple Silicon no compatible amb openai-whisper)")
        else:
            print(f"💻 Usant CPU")

    print(f"🎯 Carregant model Whisper ({model_size})...")
    model = whisper.load_model(model_size, device=device)

    print(f"🎙️  Transcrivint {audio_path}...")
    result = model.transcribe(audio_path, language="ca")

    return result

def transcribe_audio_mlx(audio_path, model_size="large-v3"):
    """Transcriu l'audio amb mlx-whisper (GPU Apple Silicon)."""
    try:
        import mlx_whisper
    except ImportError:
        print("❌ Error: mlx-whisper no està instal·lat")
        print("Instal·la'l amb: pip install mlx-whisper")
        sys.exit(1)

    print(f"🚀 Usant acceleració GPU (MLX/Apple Silicon)")
    print(f"🎯 Carregant model {model_size}...")

    # Models disponibles en Hugging Face MLX Community
    model_map = {
        'large-v3': 'mlx-community/whisper-large-v3-mlx',
        'large': 'mlx-community/whisper-large-v2-mlx',
        'medium': 'mlx-community/whisper-medium-mlx',
        'small': 'mlx-community/whisper-small-mlx',
        'base': 'mlx-community/whisper-base-mlx',
        'tiny': 'mlx-community/whisper-tiny-mlx',
    }

    model_id = model_map.get(model_size, model_map['large-v3'])

    print(f"🎙️  Transcrivint {audio_path}...")
    result = mlx_whisper.transcribe(
        audio_path,
        path_or_hf_repo=model_id,
        language='ca',
        verbose=True
    )

    return result

def transcribe_audio_lightning(audio_path, model_size="large-v3"):
    """Transcriu l'audio amb lightning-whisper-mlx (ultra-ràpid)."""
    try:
        from lightning_whisper_mlx import LightningWhisperMLX
    except ImportError:
        print("❌ Error: lightning-whisper-mlx no està instal·lat")
        print("Instal·la'l amb: pip install lightning-whisper-mlx")
        sys.exit(1)

    print(f"⚡ Usant acceleració GPU ultra-ràpida (Lightning MLX)")
    print(f"🎯 Carregant model {model_size}...")

    whisper_model = LightningWhisperMLX(
        model=model_size,
        batch_size=12,  # M1 MAX pot gestionar batch gran
        quant=None      # Sense quantització, amb 32GB RAM no cal
    )

    print(f"🎙️  Transcrivint {audio_path}...")
    result = whisper_model.transcribe(audio_path, language='ca')

    return result

def transcribe_audio(audio_path, model_size="large-v3", backend="auto"):
    """Transcriu l'audio amb el backend especificat.

    Args:
        audio_path: Ruta al fitxer d'audio
        model_size: Model de Whisper (tiny, base, small, medium, large, large-v3)
        backend: Backend a utilitzar (auto, mlx, lightning, whisper)

    Returns:
        Diccionari amb el resultat de la transcripció
    """
    # Detecció automàtica del backend
    if backend == "auto":
        import platform
        import torch

        # Detectar Apple Silicon
        if platform.processor() == 'arm' and platform.system() == 'Darwin':
            backend = "mlx"
            print(f"🔍 Detecció automàtica: Apple Silicon → backend MLX")
        # Detectar CUDA (NVIDIA GPU)
        elif torch.cuda.is_available():
            backend = "whisper"
            print(f"🔍 Detecció automàtica: NVIDIA GPU → backend whisper amb CUDA")
        # Fallback a CPU
        else:
            backend = "whisper"
            print(f"🔍 Detecció automàtica: CPU → backend whisper")

    # Seleccionar backend
    if backend == "mlx":
        return transcribe_audio_mlx(audio_path, model_size)
    elif backend == "lightning":
        return transcribe_audio_lightning(audio_path, model_size)
    elif backend == "whisper":
        return transcribe_audio_whisper_original(audio_path, model_size)
    else:
        print(f"❌ Error: Backend desconegut '{backend}'")
        print("Backends disponibles: auto, mlx, lightning, whisper")
        sys.exit(1)

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
    parser.add_argument('--model', default='large-v3',
                       choices=['tiny', 'base', 'small', 'medium', 'large', 'large-v3'],
                       help='Model de Whisper a utilitzar (per defecte: large-v3)')
    parser.add_argument('--backend', default='auto',
                       choices=['auto', 'mlx', 'lightning', 'whisper'],
                       help='Backend de transcripció: auto (detecció automàtica), mlx (GPU Apple Silicon), lightning (ultra-ràpid), whisper (CPU/CUDA)')
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
    result = transcribe_audio(args.audio_file, args.model, args.backend)
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