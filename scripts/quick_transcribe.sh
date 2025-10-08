#!/bin/bash

# Script ràpid per transcriure un episodi
# Ús: ./scripts/quick_transcribe.sh episodes/001-nom-episodi.mp3

if [ $# -eq 0 ]; then
    echo "❌ Cal especificar el fitxer MP3"
    echo "Ús: $0 episodes/XXX-nom-episodi.mp3"
    exit 1
fi

MP3_FILE="$1"

if [ ! -f "$MP3_FILE" ]; then
    echo "❌ No es troba el fitxer: $MP3_FILE"
    exit 1
fi

echo "🎙️  Transcrivint $MP3_FILE..."
echo ""

# Comprovar si Python està disponible
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no trobat"
    exit 1
fi

# Detectar arquitectura i seleccionar backend
if [[ $(uname -m) == "arm64" ]]; then
    echo "🚀 Detectat Apple Silicon - usant acceleració GPU (MLX)"
    echo "📋 Assegura't que tens mlx-whisper instal·lat: pip install mlx-whisper"
    echo ""
    python3 scripts/transcribe_episode.py "$MP3_FILE" --backend mlx --model large-v3
else
    echo "💻 Usant backend per defecte (CPU/CUDA)"
    echo "📋 Assegura't que tens Whisper instal·lat: pip install openai-whisper"
    echo ""
    python3 scripts/transcribe_episode.py "$MP3_FILE"
fi