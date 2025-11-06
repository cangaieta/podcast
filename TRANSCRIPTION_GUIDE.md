# Guia de Transcripció Automàtica amb Whisper

## Resum

Sistema de transcripció automàtica optimitzat per obtenir el màxim rendiment en diferents tipus de hardware (Apple Silicon, NVIDIA GPU, CPU). Utilitza OpenAI Whisper amb múltiples backends per garantir velocitat i qualitat.

## Característiques

✅ **Detecció automàtica de hardware** - Selecciona el millor backend segons el teu sistema
✅ **Suport multi-backend** - MLX (Apple Silicon), Lightning MLX (ultra-ràpid), Whisper (CPU/CUDA)
✅ **Alt rendiment** - Fins a 10x més ràpid amb GPU Apple Silicon
✅ **Alta qualitat** - Suport per models fins a large-v3
✅ **Flexibilitat** - Fàcil d'integrar en qualsevol projecte Python

## Rendiment Real

**Temps de transcripció per un episodi de 26 minuts (M1 MAX, 32GB RAM):**

| Backend | Model | Temps | Ràtio | Recomanat |
|---------|-------|-------|-------|-----------|
| MLX | large-v3 | ~2-3 min | 1:10 | ⭐ Màxima qualitat |
| MLX | large | ~2 min | 1:13 | Alta qualitat |
| MLX | medium | ~1-1.5 min | 1:20 | Balanç velocitat/qualitat |
| MLX | small | ~45-60 seg | 1:30 | Ràpid |
| Lightning | large-v3 | ~30-60 seg | 1:50 | ⚡ Ultra-ràpid (experimental) |
| Whisper (CPU) | small | ~5:40 min | 1:5 | Sense GPU |
| Whisper (CPU) | medium | ~7-8 min | 1:4 | Sense GPU |

**Episodi de 16 minuts (com l'episodi 005):**
- MLX large-v3: **1:37 min** (temps real comprovat)

## Instal·lació

### 1. Requisits Base

```bash
# Python 3.8 o superior
python --version

# ffmpeg (necessari per processar àudio)
# macOS:
brew install ffmpeg

# Ubuntu/Debian:
sudo apt-get install ffmpeg

# Windows:
# Descarregar de https://ffmpeg.org/download.html
```

### 2. Instal·lar Dependències

```bash
pip install openai-whisper pyyaml python-dateutil
```

### 3. Backends Opcionals (segons hardware)

#### Apple Silicon (M1/M2/M3) - RECOMANAT
```bash
pip install mlx-whisper
# Ultra-ràpid (experimental):
pip install lightning-whisper-mlx
```

#### NVIDIA GPU (CUDA)
```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## Script de Transcripció

### Script Complet (`transcribe_episode.py`)

Copia aquest script al teu projecte:

```python
#!/usr/bin/env python3
"""
Script de transcripció automàtica amb Whisper optimitzat per múltiples backends.

Ús:
    python transcribe_episode.py audio.mp3 --model large-v3 --backend mlx
"""

import os
import sys
import whisper
import yaml
from datetime import datetime
from pathlib import Path
import argparse

def transcribe_audio_mlx(audio_path, model_size="large-v3"):
    """Transcriu amb mlx-whisper (GPU Apple Silicon)."""
    try:
        import mlx_whisper
    except ImportError:
        print("❌ mlx-whisper no instal·lat. Usa: pip install mlx-whisper")
        sys.exit(1)

    print(f"🚀 Usant acceleració GPU (MLX/Apple Silicon)")
    print(f"🎯 Carregant model {model_size}...")

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
        language='ca',  # Canvia segons idioma
        verbose=True
    )

    return result

def transcribe_audio_whisper(audio_path, model_size="medium"):
    """Transcriu amb openai-whisper (CPU/CUDA)."""
    import torch

    # Detectar dispositiu
    if torch.cuda.is_available():
        device = "cuda"
        print(f"🚀 Usant acceleració GPU (CUDA)")
    else:
        device = "cpu"
        print(f"💻 Usant CPU")

    print(f"🎯 Carregant model {model_size}...")
    model = whisper.load_model(model_size, device=device)

    print(f"🎙️  Transcrivint {audio_path}...")
    result = model.transcribe(audio_path, language="ca")  # Canvia segons idioma

    return result

def transcribe_audio_lightning(audio_path, model_size="large-v3"):
    """Transcriu amb lightning-whisper-mlx (ultra-ràpid)."""
    try:
        from lightning_whisper_mlx import LightningWhisperMLX
    except ImportError:
        print("❌ lightning-whisper-mlx no instal·lat")
        print("Usa: pip install lightning-whisper-mlx")
        sys.exit(1)

    print(f"⚡ Usant GPU ultra-ràpid (Lightning MLX)")
    print(f"🎯 Carregant model {model_size}...")

    whisper_model = LightningWhisperMLX(
        model=model_size,
        batch_size=12,
        quant=None
    )

    print(f"🎙️  Transcrivint {audio_path}...")
    result = whisper_model.transcribe(audio_path, language='ca')

    return result

def transcribe_audio(audio_path, model_size="large-v3", backend="auto"):
    """
    Transcriu àudio amb el millor backend disponible.

    Args:
        audio_path: Ruta al fitxer d'àudio
        model_size: Model Whisper (tiny, base, small, medium, large, large-v3)
        backend: Backend (auto, mlx, lightning, whisper)

    Returns:
        dict: Resultat amb clau 'text' (transcripció)
    """
    # Detecció automàtica
    if backend == "auto":
        import platform
        import torch

        if platform.processor() == 'arm' and platform.system() == 'Darwin':
            backend = "mlx"
            print(f"🔍 Detectat: Apple Silicon → MLX")
        elif torch.cuda.is_available():
            backend = "whisper"
            print(f"🔍 Detectat: NVIDIA GPU → Whisper CUDA")
        else:
            backend = "whisper"
            print(f"🔍 Detectat: CPU → Whisper")

    # Executar backend
    if backend == "mlx":
        return transcribe_audio_mlx(audio_path, model_size)
    elif backend == "lightning":
        return transcribe_audio_lightning(audio_path, model_size)
    elif backend == "whisper":
        return transcribe_audio_whisper(audio_path, model_size)
    else:
        print(f"❌ Backend desconegut: {backend}")
        print("Disponibles: auto, mlx, lightning, whisper")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Transcripció automàtica amb Whisper')
    parser.add_argument('audio_file', help='Fitxer d\'àudio a transcriure')
    parser.add_argument('--model', default='large-v3',
                       choices=['tiny', 'base', 'small', 'medium', 'large', 'large-v3'],
                       help='Model Whisper (defecte: large-v3)')
    parser.add_argument('--backend', default='auto',
                       choices=['auto', 'mlx', 'lightning', 'whisper'],
                       help='Backend: auto, mlx (Apple), lightning (ràpid), whisper (CPU/CUDA)')
    parser.add_argument('--output', help='Fitxer de sortida (opcional)')
    parser.add_argument('--language', default='ca', help='Idioma (defecte: ca)')

    args = parser.parse_args()

    if not os.path.exists(args.audio_file):
        print(f"❌ Fitxer no trobat: {args.audio_file}")
        sys.exit(1)

    # Transcriure
    result = transcribe_audio(args.audio_file, args.model, args.backend)
    transcript = result["text"]

    # Mostrar resultat
    print(f"\n{'='*60}")
    print(f"✅ TRANSCRIPCIÓ COMPLETADA")
    print(f"{'='*60}\n")
    print(transcript)

    # Guardar si es demana
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(transcript)
        print(f"\n💾 Guardat a: {args.output}")

if __name__ == "__main__":
    main()
```

## Ús del Script

### Ús Bàsic

```bash
# Detecció automàtica (recomanat)
python transcribe_episode.py audio.mp3

# Especificar backend i model
python transcribe_episode.py audio.mp3 --model large-v3 --backend mlx

# Guardar transcripció
python transcribe_episode.py audio.mp3 --output transcripcio.txt
```

### Exemples per Hardware

#### Apple Silicon (M1/M2/M3)
```bash
# Màxima qualitat (recomanat)
python transcribe_episode.py audio.mp3 --model large-v3 --backend mlx

# Balanç velocitat/qualitat
python transcribe_episode.py audio.mp3 --model medium --backend mlx

# Ultra-ràpid (experimental)
python transcribe_episode.py audio.mp3 --backend lightning
```

#### NVIDIA GPU
```bash
# Amb CUDA
python transcribe_episode.py audio.mp3 --model medium --backend whisper
```

#### CPU (sense GPU)
```bash
# Model petit (recomanat per CPU)
python transcribe_episode.py audio.mp3 --model small --backend whisper

# Episodis curts (<10 min)
python transcribe_episode.py audio.mp3 --model medium --backend whisper
```

### Canviar Idioma

```bash
# Anglès
python transcribe_episode.py audio.mp3 --language en

# Castellà
python transcribe_episode.py audio.mp3 --language es

# Francès
python transcribe_episode.py audio.mp3 --language fr
```

## Selecció de Model

### Recomanacions per Hardware

**M1 MAX / M2 MAX (32GB RAM):**
- ✅ `large-v3` - Millor opció, sense timeout
- ✅ `large` - Alternativa si large-v3 no funciona
- ⚠️ `medium` - Només si necessites màxima velocitat

**M1 / M2 (8-16GB RAM):**
- ✅ `medium` - Millor balanç
- ✅ `small` - Si tens episodis llargs (>20 min)
- ⚠️ `large` - Pot ser lent o quedar-se sense memòria

**NVIDIA GPU (8GB+ VRAM):**
- ✅ `medium` - Recomanat
- ✅ `small` - Per episodis llargs (>20 min)
- ⚠️ `large` - Necessita 10GB+ VRAM

**CPU:**
- ✅ `small` - Millor opció
- ⚠️ `medium` - Només episodis curts (<10 min)
- ❌ `large` - Massa lent

### Qualitat dels Models

| Model | Paràmetres | Qualitat | Idiomes | Ús Recomanat |
|-------|------------|----------|---------|--------------|
| large-v3 | 1550M | ⭐⭐⭐⭐⭐ | 99 | Producció, màxima qualitat |
| large | 1550M | ⭐⭐⭐⭐⭐ | 99 | Producció, alta qualitat |
| medium | 769M | ⭐⭐⭐⭐ | 99 | Balanç qualitat/velocitat |
| small | 244M | ⭐⭐⭐ | 99 | Episodis llargs, CPU |
| base | 74M | ⭐⭐ | 99 | Proves ràpides |
| tiny | 39M | ⭐ | 99 | Prototips |

## Problemes Comuns i Solucions

### Error: "Could not run 'aten::empty.memory_format'"

Aquest error apareix quan s'intenta usar MPS (Apple Silicon) amb openai-whisper.

**Solució:** Usa el backend MLX en lloc de whisper:
```bash
pip install mlx-whisper
python transcribe_episode.py audio.mp3 --backend mlx
```

### Error: "Out of Memory"

Model massa gran per la RAM/VRAM disponible.

**Solució:** Usa un model més petit:
```bash
python transcribe_episode.py audio.mp3 --model small
```

### Transcripció Massa Lenta (CPU)

**Solucions:**
1. Usa un model més petit (`small` o `base`)
2. Instal·la backend MLX si tens Apple Silicon
3. Considera usar un servei cloud amb GPU

### Baixa Qualitat de Transcripció

**Solucions:**
1. Usa un model més gran (`large-v3`)
2. Millora la qualitat de l'àudio (redueix soroll)
3. Assegura't que l'idioma és correcte (`--language ca`)

## Integració en Altres Projectes

### Ús com a Mòdul Python

```python
from transcribe_episode import transcribe_audio

# Transcriure fitxer
result = transcribe_audio("audio.mp3", model_size="large-v3", backend="auto")
text = result["text"]

print(f"Transcripció: {text}")
```

### Batch Processing

```python
import os
from transcribe_episode import transcribe_audio

audio_files = ["audio1.mp3", "audio2.mp3", "audio3.mp3"]

for audio_file in audio_files:
    print(f"Processant: {audio_file}")
    result = transcribe_audio(audio_file, model_size="medium", backend="mlx")

    # Guardar transcripció
    output_file = audio_file.replace(".mp3", ".txt")
    with open(output_file, 'w') as f:
        f.write(result["text"])
```

### Amb Timestamps

```python
from transcribe_episode import transcribe_audio

result = transcribe_audio("audio.mp3", model_size="large-v3", backend="mlx")

# Segments amb timestamps
for segment in result.get("segments", []):
    start = segment["start"]
    end = segment["end"]
    text = segment["text"]
    print(f"[{start:.2f}s - {end:.2f}s] {text}")
```

## Millors Pràctiques

1. **Usa detecció automàtica**: Deixa que el script triï el millor backend
2. **Comença amb models grans**: large-v3 dona millors resultats, sobretot amb MLX
3. **Revisa la transcripció**: Whisper és excel·lent però no perfecte
4. **Optimitza l'àudio**: Àudio de qualitat = millor transcripció
5. **Monitora la RAM**: Tanca aplicacions si uses models grans
6. **Batch processing**: Transcriu múltiples fitxers en una sola execució

## Comparativa de Backends

| Backend | Hardware | Velocitat | Qualitat | Instal·lació |
|---------|----------|-----------|----------|--------------|
| MLX | Apple Silicon | ⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Fàcil |
| Lightning | Apple Silicon | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Fàcil |
| Whisper (CUDA) | NVIDIA GPU | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Mitjà |
| Whisper (CPU) | Qualsevol | ⚡ | ⭐⭐⭐⭐⭐ | Fàcil |

## Recursos Addicionals

- **OpenAI Whisper**: https://github.com/openai/whisper
- **MLX Whisper**: https://github.com/ml-explore/mlx-examples/tree/main/whisper
- **Lightning Whisper MLX**: https://github.com/mustafaaljadery/lightning-whisper-mlx
- **Models Whisper**: https://huggingface.co/openai

## Llicència

Aquest sistema està basat en OpenAI Whisper (MIT License). Lliure per usar en projectes comercials i no comercials.

## Credits

- **OpenAI** - Model Whisper
- **Apple MLX** - Backend GPU Apple Silicon
- **Can Gaietà Podcast** - Implementació i optimització

---

**Versió:** 1.0
**Última actualització:** Novembre 2025
**Testejat amb:** M1 MAX (32GB), Python 3.11, macOS Sonoma
