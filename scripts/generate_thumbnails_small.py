#!/usr/bin/env python3
"""
Genera versions reduïdes dels thumbnails per als llistats de la web.

Els thumbnails originals són PNG 1024x1024 d'~1,3 MB. Posar-los tal qual a la
pàgina /episodis (20 episodis) vol dir ~26 MB d'imatges en una sola pàgina.
Aquest script en genera versions WebP 400x400 (~40 KB) a assets/thumbnails/small/.

Qui fa servir cada versió:
  - Llistats web (portada, /episodis)  -> small/XXX-nom.webp
  - Detall de l'episodi, RSS, archive.org -> XXX-nom.png (original)

Ús:
    python scripts/generate_thumbnails_small.py            # només els que falten
    python scripts/generate_thumbnails_small.py --force    # regenera-ho tot
    python scripts/generate_thumbnails_small.py 014        # només un episodi
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("❌ Falta Pillow. Instal·la'l amb: pip install Pillow")
    sys.exit(1)

MIDA = 400          # px, prou per a una targeta de llistat en pantalles retina
QUALITAT = 82       # qualitat WebP


def genera(origen: Path, desti: Path, force: bool = False) -> str:
    """Genera una versió reduïda. Retorna 'creat', 'saltat' o 'error: ...'."""
    if desti.exists() and not force:
        return "saltat"

    try:
        with Image.open(origen) as im:
            im = im.convert("RGB")
            im.thumbnail((MIDA, MIDA), Image.LANCZOS)
            desti.parent.mkdir(parents=True, exist_ok=True)
            im.save(desti, "WEBP", quality=QUALITAT, method=6)
        return "creat"
    except Exception as e:
        return f"error: {e}"


def main():
    parser = argparse.ArgumentParser(
        description="Genera thumbnails reduïts (WebP 400x400) per als llistats"
    )
    parser.add_argument("episodi", nargs="?",
                        help="Número d'episodi concret (ex: 014). Per defecte, tots.")
    parser.add_argument("--force", action="store_true",
                        help="Regenera encara que el fitxer reduït ja existeixi")
    args = parser.parse_args()

    project_dir = Path(__file__).parent.parent
    dir_grans = project_dir / "assets" / "thumbnails"
    dir_petits = dir_grans / "small"

    originals = sorted(dir_grans.glob("*.png"))
    if args.episodi:
        originals = [p for p in originals if p.name.startswith(f"{args.episodi}-")]
        if not originals:
            print(f"❌ No s'ha trobat cap thumbnail per a l'episodi {args.episodi}")
            sys.exit(1)

    print(f"🖼️  Generant thumbnails reduïts ({MIDA}x{MIDA} WebP)")
    print("=" * 60)

    creats = saltats = errors = 0
    pes_gran = pes_petit = 0

    for origen in originals:
        desti = dir_petits / f"{origen.stem}.webp"
        resultat = genera(origen, desti, force=args.force)

        if resultat == "creat":
            creats += 1
            icona = "✅"
        elif resultat == "saltat":
            saltats += 1
            icona = "⏭️ "
        else:
            errors += 1
            print(f"❌ {origen.name}: {resultat}")
            continue

        pes_gran += origen.stat().st_size
        pes_petit += desti.stat().st_size
        print(f"{icona} {origen.name:55} "
              f"{origen.stat().st_size / 1024:7.0f} KB → {desti.stat().st_size / 1024:6.0f} KB")

    print("=" * 60)
    print(f"✅ Creats: {creats}   ⏭️  Ja existien: {saltats}   ❌ Errors: {errors}")
    if pes_gran:
        print(f"📉 Pes total als llistats: "
              f"{pes_gran / 1024 / 1024:.2f} MB → {pes_petit / 1024 / 1024:.2f} MB "
              f"({100 - pes_petit * 100 / pes_gran:.0f}% menys)")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
