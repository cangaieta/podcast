#!/usr/bin/env bash
# Genera fitxers SRT per a tots els episodis existents.
# Requereix que els fitxers MP3 estiguin a episodes/
#
# Ús:
#   ./scripts/generate_all_srt.sh             # processa tots els MP3 de episodes/
#   ./scripts/generate_all_srt.sh --force     # regenera fins i tot si el SRT ja existeix

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

# Activar venv si existeix
[[ -f .venv/bin/activate ]] && source .venv/bin/activate

# Detectar backend
BACKEND_ARGS=""
if [[ "$(uname -m)" == "arm64" ]]; then
    BACKEND_ARGS="--backend mlx --model large-v3"
    echo "🍎 Apple Silicon detectat → backend MLX + model large-v3"
else
    echo "💻 Usant backend per defecte (auto)"
fi

FORCE=false
[[ "${1:-}" == "--force" ]] && FORCE=true

TOTAL=0
SUCCESS=0
SKIP=0
FAIL=0

for mp3 in episodes/*.mp3; do
    [[ -f "$mp3" ]] || { echo "⚠️  No s'han trobat fitxers MP3 a episodes/"; break; }
    TOTAL=$((TOTAL + 1))
    filename=$(basename "$mp3" .mp3)
    srt_path="sources/${filename}-transcripcio.srt"

    if [[ -f "$srt_path" ]] && [[ "$FORCE" == "false" ]]; then
        echo "⏭️  Saltant ${filename} (SRT ja existeix, usa --force per regenerar)"
        SKIP=$((SKIP + 1))
        continue
    fi

    echo ""
    echo "══════════════════════════════════════════════════"
    echo "🎙️  Processant: $mp3"
    echo "══════════════════════════════════════════════════"

    if python scripts/transcribe_episode.py "$mp3" $BACKEND_ARGS --srt-only; then
        SUCCESS=$((SUCCESS + 1))
        echo "✅ SRT creat: $srt_path"
    else
        FAIL=$((FAIL + 1))
        echo "❌ Error processant: $mp3"
    fi
done

echo ""
echo "══════════════════════════════════════════════════"
echo "📊 Resum: $TOTAL episodis trobats"
echo "   ✅ SRTs nous: $SUCCESS"
echo "   ⏭️  Saltats (ja existien): $SKIP"
echo "   ❌ Errors: $FAIL"
echo "══════════════════════════════════════════════════"
if [[ $SUCCESS -gt 0 ]]; then
    echo ""
    echo "🔧 Pròxim pas: afegir els SRTs al repositori:"
    echo "   git add sources/*-transcripcio.srt && git commit -m 'Add SRT subtitle files for all episodes'"
fi
