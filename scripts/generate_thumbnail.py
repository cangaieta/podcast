#!/usr/bin/env python3
"""
Genera un thumbnail per a un episodi del podcast amb Krea 2 / Qwen Image 2.1 (Draw Things).

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
    - Els models al directori de models de Draw Things. Si falten:
        draw-things-cli models ensure --model krea_2_turbo_q6p.ckpt
        draw-things-cli models ensure --model qwen_image_2.1_turbo_q6p.ckpt  (--model qwen)

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

# Prompt base. Qwen Image i Krea 2 volen prompts llargs i descrits per parts:
# amb l'antic (escena + "In the foreground or as a visual element: <sufix>")
# Qwen 2.1 gairebé ometia el tema de l'episodi (es va veure provant el 013).
# Ara el tema té secció pròpia, mida i posició explícites, i la paleta va al
# final perquè no la tapi.
STYLE_PROMPT = (
    "Square flat vector illustration for a local news podcast cover, clean minimalist "
    "editorial style with flat colors, crisp dark outlines and no gradients, designed to "
    "stay readable as a tiny 110-pixel thumbnail."
)

SETTING_PROMPT = (
    "Setting: the Can Gaietà neighbourhood of Tiana, a small Mediterranean town near "
    "Barcelona, on a hillside under a pale light-blue sky. On the left stands a traditional "
    "whitewashed Catalan masia farmhouse with a terracotta tile roof, green wooden shutters "
    "and a small arched doorway. On the right, climbing the slope behind it, a cluster of "
    "modern red-brick apartment blocks of three and four storeys with small balconies. On "
    "the hilltop in the background, a few Mediterranean umbrella pines (Pinus pinea) with "
    "tall bare trunks and wide flat-topped olive-green canopies; no fir trees, no Christmas "
    "trees."
)

MASCOT_PROMPT = (
    "Mascot: the white masia wears a pair of oversized futuristic headphones as if the house "
    "were a character, the matte navy-blue headband arching over the terracotta roof and the "
    "two large round ear cups pressed against the side walls, with thin glowing cyan rings "
    "around the ear cups."
)

THEME_PROMPT = (
    "Episode theme, large and in the foreground, occupying the lower right third of the "
    "image: {suffix}"
)

PALETTE_PROMPT = (
    "Colour palette limited to white, red brick, terracotta, olive green, light sky blue and "
    "navy blue, with accents of glowing cyan and the episode's own colours. Strong "
    "silhouettes, high contrast, uncluttered composition with the masia and the episode "
    "theme as the two clear focal points."
)


def build_prompt(prompt_suffix):
    parts = [STYLE_PROMPT, SETTING_PROMPT, MASCOT_PROMPT]
    if prompt_suffix:
        parts.append(THEME_PROMPT.format(suffix=prompt_suffix))
    parts.append(PALETTE_PROMPT)
    return "\n\n".join(parts)


# Models de Draw Things, provats amb el 013 (2026-10):
#
#   krea   Krea 2 Turbo. Per defecte: sempre correcte (masia, maó, pins, tema
#          sencer) i estil pla com el catàleg antic. ~4 min per imatge.
#   qwen   Qwen Image 2.1 Turbo. Imatges més interessants, però de tant en tant
#          en surt una de malament. ~2 min. Per triar a mà entre llavors.
#
# Krea 2 fa servir els "recommended settings" del model; només se'n fixa la
# mida. Els de Qwen 2.1 són els que fa servir el David a l'app de Draw Things.
# Tot el catàleg de thumbnails és 1024x1024.
DT_SIZE = 1024
DT_MODELS = {
    "krea": {"model": "krea_2_turbo_q6p.ckpt"},
    "qwen": {
        "model": "qwen_image_2.1_turbo_q6p.ckpt",
        "sampler": 16,
        "steps": 8,
        "guidanceScale": 1,
        "shift": 6.5,
        "resolutionDependentShift": False,
        "loras": [],
    },
}
DT_DEFAULT_MODEL = "krea"
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


def _generate_draw_things(full_prompt, dest_image, seed, model):
    """draw-things-cli escriu directament a --output; no cal temporal."""
    config = dict(DT_MODELS[model])
    config.update({
        "width": DT_SIZE,
        "height": DT_SIZE,
        "batchCount": 1,
        "batchSize": 1,
        "strength": 1,
    })

    cmd = [
        "draw-things-cli", "generate",
        "--model", config["model"],
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
                       backend="auto", seed=None, model=DT_DEFAULT_MODEL):
    """Genera un thumbnail i el desa a output_dir."""

    full_prompt = build_prompt(prompt_suffix)

    backend = _resolve_backend(backend)

    # Sempre una llavor explícita: draw-things-cli no la reporta, i sense això
    # no es pot reproduir ni ajustar un thumbnail que gairebé funciona.
    if seed is None:
        seed = random.randrange(2**31)

    print(f"🎨 Generant thumbnail per episodi {episodi} ({nom})")
    print(f"🖼️ Suffix: {prompt_suffix}")
    print(f"📝 Prompt (primeres 150 chars): {full_prompt[:150]}...")
    print(f"⚙️ Backend: {backend}" + (f" ({model})" if backend == "draw-things" else ""))
    print(f"🎲 Seed: {seed}")
    print("⏳ Generant...")

    os.makedirs(output_dir, exist_ok=True)
    dest_image = os.path.join(output_dir, f"{nom}.png")

    start = time.perf_counter()
    if backend == "draw-things":
        _generate_draw_things(full_prompt, dest_image, seed, model)
    else:
        _generate_ollama(full_prompt, dest_image, episodi)
    elapsed = time.perf_counter() - start

    print(f"✅ Thumbnail guardat a: {dest_image}  ({elapsed:.1f}s, backend {backend}, seed {seed})")
    return dest_image


def main():
    parser = argparse.ArgumentParser(
        description="Genera thumbnail per episodi de podcast amb Krea 2 / Qwen Image 2.1 (Draw Things)"
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
        help="Escena del tema de l'episodi, en anglès i DETALLADA: què hi surt, com és, "
             "quines persones hi ha i què fan, quin text curt hi apareix (ex: 'a giant "
             "smartphone leaning against the masia, its screen showing a red subscribe "
             "button and a big counter reading 100K, next to an open municipal "
             "magazine whose back cover shows a smiling teenage boy holding a camera')",
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
        "--model",
        choices=sorted(DT_MODELS),
        default=DT_DEFAULT_MODEL,
        help="Model de Draw Things (per defecte: krea — sempre correcte; qwen — més "
             "interessant però irregular, per triar a mà entre llavors)",
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Llavor per a resultats reproduïbles (només backend draw-things)",
    )

    args = parser.parse_args()

    dest = generate_thumbnail(
        args.episodi, args.nom, args.prompt_suffix, args.output_dir,
        backend=args.backend, seed=args.seed, model=args.model,
    )
    ext = os.path.splitext(dest)[1]
    print(f"\n🔧 Afegeix al frontmatter de _episodes/{args.nom}.md:")
    print(f'thumbnail: "/{args.output_dir}/{args.nom}{ext}"')


if __name__ == "__main__":
    main()
