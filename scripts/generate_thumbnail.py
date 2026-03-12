#!/usr/bin/env python3
"""
Genera un thumbnail per a un episodi del podcast usant ollama x/z-image-turbo.

El model genera una imatge al directori de treball actual (cwd).
El script executa ollama en un directori temporal i mou el resultat a assets/thumbnails/.

Ús:
    python scripts/generate_thumbnail.py \\
        --episodi 013 \\
        --nom 013-youtuber-revista-pantalles \\
        --prompt-suffix "a smartphone and magazine cover celebrating a young youtuber, social media icons"

Requisits:
    - ollama instal·lat: https://ollama.com
    - Model descarregat: ollama pull x/z-image-turbo
"""

import os
import sys
import argparse
import subprocess
import glob
import shutil
import time
import tempfile

# Prompt base — escena del barri de Can Gaietà amb els headphones icònics
BASE_PROMPT = (
    "The Can Gaietà neighborhood of Tiana. The design features the traditional white Catalan masía "
    "with terracotta roof on one side, and multiple modern red brick apartment buildings of different "
    "heights clustered together on the other side going uphill. Mediterranean umbrella pines (Pinus pinea) "
    "with their distinctive flat tops and umbrella-like canopies appear on the hill in the background, "
    "NOT Christmas-like fir or spruce trees. Use a clean, minimalist style with flat colors and defined "
    "outlines suitable for small display. The color palette includes white, red brick, terracotta, olive "
    "green for the pines, and light blue for the sky. The overall composition should balance historic and "
    "contemporary elements, large futuristic blue-black headphones worn by the white house as if it's a "
    "character - the headphones should be oversized and playfully positioned on the house like it's wearing "
    "them. The headphones should have a sleek, futuristic design with clean geometric lines, matte or "
    "metallic finish, and subtle blue glowing details"
)


def generate_thumbnail(episodi, nom, prompt_suffix, output_dir="assets/thumbnails"):
    """Genera un thumbnail usant ollama x/z-image-turbo i el desa a output_dir."""

    full_prompt = BASE_PROMPT
    if prompt_suffix:
        full_prompt = f"{BASE_PROMPT}. In the foreground or as a visual element: {prompt_suffix}"

    print(f"🎨 Generant thumbnail per episodi {episodi} ({nom})")
    print(f"📝 Prompt (primeres 150 chars): {full_prompt[:150]}...")

    # Executar ollama en directori temporal — escriu la imatge al seu cwd
    with tempfile.TemporaryDirectory(prefix=f"podcast_thumb_{episodi}_") as tmpdir:
        print(f"⏳ Executant ollama x/z-image-turbo (pot trigar 30-90 seg)...")

        try:
            subprocess.run(
                ["ollama", "run", "x/z-image-turbo", full_prompt],
                cwd=tmpdir,
                check=True,
                timeout=300,
            )
        except subprocess.TimeoutExpired:
            print("❌ Error: ollama ha superat el temps límit (300s)")
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error d'ollama (codi {e.returncode})")
            sys.exit(1)
        except FileNotFoundError:
            print("❌ Error: 'ollama' no trobat al PATH.")
            print("   Instal·la'l des de: https://ollama.com")
            print("   I descarrega el model: ollama pull x/z-image-turbo")
            sys.exit(1)

        # Cercar la imatge generada al directori temporal
        image_files = []
        for ext in ["*.png", "*.jpg", "*.jpeg", "*.webp"]:
            image_files.extend(glob.glob(os.path.join(tmpdir, ext)))

        if not image_files:
            print(f"❌ No s'ha trobat cap imatge a {tmpdir}")
            print(f"   Fitxers presents: {os.listdir(tmpdir)}")
            print("   Prova manualment: cd /tmp && ollama run x/z-image-turbo 'test'")
            sys.exit(1)

        # Triar la més recent (normalment n'hi ha una sola)
        image_files.sort(key=os.path.getmtime, reverse=True)
        source_image = image_files[0]
        ext = os.path.splitext(source_image)[1].lower() or ".png"

        os.makedirs(output_dir, exist_ok=True)
        dest_image = os.path.join(output_dir, f"{nom}{ext}")
        shutil.copy2(source_image, dest_image)

    print(f"✅ Thumbnail guardat a: {dest_image}")
    return dest_image


def main():
    parser = argparse.ArgumentParser(
        description="Genera thumbnail per episodi de podcast amb ollama x/z-image-turbo"
    )
    parser.add_argument(
        "--episodi", required=True, help="Número de l'episodi (ex: 013)"
    )
    parser.add_argument(
        "--nom",
        required=True,
        help="Nom complet del fitxer sense extensió (ex: 013-youtuber-revista-pantalles)",
    )
    parser.add_argument(
        "--prompt-suffix",
        default="",
        help="Element visual específic per a aquest episodi (en anglès per millors resultats)",
    )
    parser.add_argument(
        "--output-dir",
        default="assets/thumbnails",
        help="Directori de sortida (per defecte: assets/thumbnails)",
    )

    args = parser.parse_args()

    dest = generate_thumbnail(args.episodi, args.nom, args.prompt_suffix, args.output_dir)
    ext = os.path.splitext(dest)[1]
    print(f"\n🔧 Afegeix al frontmatter de _episodes/{args.nom}.md:")
    print(f'thumbnail: "/{args.output_dir}/{args.nom}{ext}"')


if __name__ == "__main__":
    main()
