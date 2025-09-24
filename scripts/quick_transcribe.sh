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
echo "📋 Assegura't que tens Whisper instal·lat: pip install openai-whisper"
echo ""

# Comprovar si Python està disponible
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no trobat"
    exit 1
fi

# Executar script de transcripció
python3 scripts/transcribe_episode.py "$MP3_FILE"