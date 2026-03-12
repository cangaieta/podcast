#!/usr/bin/env bash
# Descarrega tots els MP3 des d'archive.org a episodes/
# Ús:
#   ./scripts/download_episodes.sh            # descarrega tots
#   ./scripts/download_episodes.sh --force    # redownload fins i tot si ja existeix

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

FORCE=false
[[ "${1:-}" == "--force" ]] && FORCE=true

mkdir -p episodes

TOTAL=0
SKIP=0
DOWNLOAD=0
FAIL=0

# Llegir URLs des dels frontmatters dels episodis
while IFS= read -r line; do
    url="${line#*audio_file: }"
    url="${url//\"/}"
    url="${url//\'/}"
    url="${url// /}"

    # Només URLs d'archive.org
    [[ "$url" == "https://archive.org/"* ]] || continue

    filename=$(basename "$url")
    dest="episodes/$filename"
    TOTAL=$((TOTAL + 1))

    if [[ -f "$dest" ]] && [[ "$FORCE" == "false" ]]; then
        echo "⏭️  Saltant $filename (ja existeix)"
        SKIP=$((SKIP + 1))
        continue
    fi

    echo ""
    echo "⬇️  Descarregant: $filename"
    if curl -L --progress-bar -o "$dest" "$url"; then
        size=$(du -sh "$dest" | cut -f1)
        echo "   ✅ Desat a $dest ($size)"
        DOWNLOAD=$((DOWNLOAD + 1))
    else
        echo "   ❌ Error descarregant $url"
        FAIL=$((FAIL + 1))
        rm -f "$dest"
    fi

done < <(grep "audio_file:.*archive.org" _episodes/*.md)

echo ""
echo "══════════════════════════════════════════════════"
echo "📊 Resum: $TOTAL episodis | ⬇️ $DOWNLOAD descarregats | ⏭️ $SKIP saltats | ❌ $FAIL errors"
echo "══════════════════════════════════════════════════"
