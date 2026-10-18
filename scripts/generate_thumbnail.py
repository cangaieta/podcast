#!/usr/bin/env python3
"""
Genera un thumbnail per a un episodi del podcast amb Qwen Image 2.1 (Draw Things).

Hi ha dos backends:

  draw-things-cli  (per defecte)  Escriu la imatge directament a --output.
  ollama           (llegat)       Escriu al cwd; cal executar-lo en un temporal
                                  i moure'n el resultat.

Ollama va retirar la generació d'imatges a la versió 0.32.6, així que el backend
d'ollama només funciona amb 0.32.5 o anterior.

Ús:
    python scripts/generate_thumbnail.py \\
        --episodi 013 \\
        --nom 013-youtuber-revista-pantalles \\
        --prompt-suffix "a smartphone and magazine cover celebrating a young youtuber, social media icons"

Requisits (draw-things-cli):
    - brew install draw-things-cli  (26.1011.0 o posterior: les anteriors no
      coneixen Qwen Image 2.1)
    - El model qwen_image_2.1_turbo_q6p.ckpt al directori de models de Draw Things.
      Si falta: draw-things-cli models ensure --model qwen_image_2.1_turbo_q6p.ckpt

Requisits (ollama, llegat):
    - ollama <= 0.32.5 i el model: ollama pull x/z-image-turbo
"""

import os
import sys
import json
import random
import argparse
import subprocess
import glob
import shutil
import time
import tempfile

# Prompt base — escena del barri de Can Gaietà amb els headphones icònics
BASE_PROMPT = (
    "The Can Gaietà neighborhood of Tiana. The design features the traditional white Catalan masía "
    "with terracotta roof on one side, and multiple modern red brick duplex, triples and walk-up buildings of different "
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


# Qwen Image 2.1 Turbo ja ve destil·lat per a pocs passos: no cal LoRA.
# Paràmetres explícits perquè, sense passar-los, draw-things-cli aplica els
# "recommended settings" del model, que no són els que fa servir el David a
# l'app de Draw Things. Aquests en són una còpia, amb la resolució baixada a
# 1024 perquè tot el catàleg de thumbnails és 1024x1024.
DT_MODEL = "qwen_image_2.1_turbo_q6p.ckpt"
DT_STEPS = 8
DT_SAMPLER = 16
DT_SHIFT = 6.5
DT_GUIDANCE = 1
DT_SIZE = 1024
DT_TIMEOUT = 1800


def _resolve_backend(backend):
    """'auto' tria draw-things-cli si hi és; si no, ollama."""
    if backend != "auto":
        return backend
    if shutil.which("draw-things-cli"):
        return "draw-things"
    if shutil.which("ollama"):
        return "ollama"
    print("❌ No s'ha trobat ni 'draw-things-cli' ni 'ollama' al PATH.")
    print("   Instal·la: brew install draw-things-cli")
    sys.exit(1)


def _generate_draw_things(full_prompt, dest_image, seed):
    """draw-things-cli escriu directament a --output; no cal temporal."""
    config = {
        "model": DT_MODEL,
        "sampler": DT_SAMPLER,
        "steps": DT_STEPS,
        "guidanceScale": DT_GUIDANCE,
        "shift": DT_SHIFT,
        "resolutionDependentShift": False,
        "width": DT_SIZE,
        "height": DT_SIZE,
        "batchCount": 1,
        "batchSize": 1,
        "strength": 1,
        "loras": [],
    }

    cmd = [
        "draw-things-cli", "generate",
        "--model", DT_MODEL,
        "--config-json", json.dumps(config),
        "--prompt", full_prompt,
        "--seed", str(seed),
        "--output", dest_image,
    ]

    try:
        subprocess.run(cmd, check=True, timeout=DT_TIMEOUT)
    except subprocess.TimeoutExpired:
        print(f"❌ Error: draw-things-cli ha superat el temps límit ({DT_TIMEOUT}s)")
        print("   Comprova la memòria lliure: si el swap va ple, el model fa thrashing.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error de draw-things-cli (codi {e.returncode})")
        print("   Comprova que el model hi és: draw-things-cli models list --downloaded-only")
        print("   Si diu 'Could not resolve --model': brew upgrade draw-things-cli")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Error: 'draw-things-cli' no trobat al PATH.")
        print("   Instal·la'l amb: brew install draw-things-cli")
        sys.exit(1)

    if not os.path.exists(dest_image):
        print(f"❌ draw-things-cli ha acabat bé però no hi ha cap fitxer a {dest_image}")
        sys.exit(1)
    return dest_image


def _generate_ollama(full_prompt, dest_image, episodi):
    """Ollama escriu al cwd: l'executem en un temporal i en movem el resultat."""
    with tempfile.TemporaryDirectory(prefix=f"podcast_thumb_{episodi}_") as tmpdir:
        try:
            subprocess.run(
                ["ollama", "run", "x/z-image-turbo", full_prompt],
                cwd=tmpdir,
                check=True,
                timeout=900,
            )
        except subprocess.TimeoutExpired:
            print("❌ Error: ollama ha superat el temps límit (900s)")
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error d'ollama (codi {e.returncode})")
            print("   Recorda que ollama va retirar la generació d'imatges a la 0.32.6.")
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
        shutil.copy2(image_files[0], dest_image)
    return dest_image


def generate_thumbnail(episodi, nom, prompt_suffix, output_dir="assets/thumbnails",
                       backend="auto", seed=None):
    """Genera un thumbnail i el desa a output_dir."""

    full_prompt = BASE_PROMPT
    if prompt_suffix:
        full_prompt = f"{BASE_PROMPT}. In the foreground or as a visual element: {prompt_suffix}"

    backend = _resolve_backend(backend)

    # Sempre una llavor explícita: draw-things-cli no la reporta, i sense això
    # no es pot reproduir ni ajustar un thumbnail que gairebé funciona.
    if seed is None:
        seed = random.randrange(2**31)

    print(f"🎨 Generant thumbnail per episodi {episodi} ({nom})")
    print(f"🖼️ Suffix: {prompt_suffix}")
    print(f"📝 Prompt (primeres 150 chars): {full_prompt[:150]}...")
    print(f"⚙️ Backend: {backend}")
    print(f"🎲 Seed: {seed}")
    print("⏳ Generant...")

    os.makedirs(output_dir, exist_ok=True)
    dest_image = os.path.join(output_dir, f"{nom}.png")

    start = time.perf_counter()
    if backend == "draw-things":
        _generate_draw_things(full_prompt, dest_image, seed)
    else:
        _generate_ollama(full_prompt, dest_image, episodi)
    elapsed = time.perf_counter() - start

    print(f"✅ Thumbnail guardat a: {dest_image}  ({elapsed:.1f}s, backend {backend}, seed {seed})")
    return dest_image


def main():
    parser = argparse.ArgumentParser(
        description="Genera thumbnail per episodi de podcast amb Qwen Image 2.1 (Draw Things)"
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
    parser.add_argument(
        "--backend",
        choices=["auto", "draw-things", "ollama"],
        default="auto",
        help="Motor de generació (per defecte: auto — draw-things-cli si hi és)",
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Llavor per a resultats reproduïbles (només backend draw-things)",
    )

    args = parser.parse_args()

    dest = generate_thumbnail(
        args.episodi, args.nom, args.prompt_suffix, args.output_dir,
        backend=args.backend, seed=args.seed,
    )
    ext = os.path.splitext(dest)[1]
    print(f"\n🔧 Afegeix al frontmatter de _episodes/{args.nom}.md:")
    print(f'thumbnail: "/{args.output_dir}/{args.nom}{ext}"')


if __name__ == "__main__":
    main()
