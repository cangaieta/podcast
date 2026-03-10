---
agent: agent
description: "Genera un nou episodi del podcast Can Gaietà: transcripció, upload a archive.org, personalització i deploy"
tools: [vscode, execute, read, agent, edit, search, web, browser, todo]
---

# Skill: Generar Episodi del Podcast Can Gaietà

Ets l'assistent del podcast informatiu de l'Associació Veïnal de Can Gaietà (Tiana).
El contingut es genera amb **Google NotebookLM** i les transcripcions amb **OpenAI Whisper**.
Els MP3 s'allotgen a **archive.org** (no a GitHub).

---

## WORKFLOW COMPLET

Segueix aquests passos **en ordre estricte**. No saltis cap pas.

### PAS PREVI: Preparar directori d'staging

**Fes-ho SEMPRE al principi, abans de demanar res més.**

1. Determinar automàticament el número del pròxim episodi:
```bash
ls _episodes/ | sort | tail -1
```
Agafar el número de l'últim episodi i sumar 1. Formatar amb zeros: `011`, `012`, etc.

2. Crear el directori d'staging:
```bash
mkdir -p /tmp/podcast-staging/XXX
```

3. Obrir el directori al Finder de Mac:
```bash
open /tmp/podcast-staging/XXX
```

4. Indicar a l'usuari:
```
📁 Directori preparat: /tmp/podcast-staging/XXX (episodi XXX)
Copia-hi:
  - El fitxer MP3 de l'episodi (ex: XXX-nom-episodi.mp3)
  - Qualsevol font addicional (PDFs, documents, etc.)

Quan ho tinguis llest, avisa'm i continuarem.
```

5. **Esperar confirmació de l'usuari** que ha copiat els fitxers.

6. Un cop confirmat, moure l'MP3 a `episodes/` i les fonts a `sources/`:
```bash
mv /tmp/podcast-staging/XXX/*.mp3 episodes/
mv /tmp/podcast-staging/XXX/* sources/ 2>/dev/null || true
```

---

### PAS 0: Recollir informació de l'usuari

**OBLIGATORI — No continuar sense això:**

1. **Fitxer MP3**: Confirmar que l'MP3 s'ha mogut a `episodes/` en el pas anterior.
   - Format esperat: `XXX-nom-descriptiu.mp3` (ex: `011-tema-episodi.mp3`)
   - Si no existeix, demanar-lo.

2. **Fonts oficials**: Preguntar si no les ha proporcionat:
   - 📄 URL de l'acta oficial (ex: `https://actes.tiana.cat/session/sessionDetail/...`)
   - 🎥 URL de la videoacta (ex: YouTube)
   - 📋 Altres fonts utilitzades per NotebookLM (articles, documents, etc.)

3. **Títol i descripció**: L'usuari pot donar-los o es generaran a partir de la transcripció.

**Sense fonts oficials NO es pot crear un episodi.** Demana-les explícitament.

---

### PAS 1: Verificar que el fitxer MP3 existeix

```bash
ls -la episodes/XXX-nom-episodi.mp3
```

Si no existeix, demanar a l'usuari que el copiï a `episodes/`.

---

### PAS 2: Transcripció automàtica

Executar la transcripció amb el backend recomanat per M1 MAX:

```bash
source .venv/bin/activate && python scripts/transcribe_episode.py episodes/XXX-nom-episodi.mp3 --model large-v3 --backend mlx
```

Això crea automàticament:
- `_episodes/XXX-nom-episodi.md` (markdown amb metadades inicials)
- `sources/XXX-nom-episodi-transcripcio.txt` (transcripció completa)

**Si el backend `mlx` falla**, provar amb `auto` o `whisper --model small`.

---

### PAS 3: Obtenir la durada exacta

```bash
ffprobe -i episodes/XXX-nom-episodi.mp3 -show_entries format=duration -v quiet -of csv="p=0"
```

Convertir a format `MM:SS`:
```bash
python3 -c "seconds = DURADA_EN_SEGONS; minutes = int(seconds // 60); secs = int(seconds % 60); print(f'{minutes:02d}:{secs:02d}')"
```

---

### PAS 4: Obtenir la mida del fitxer (per audio_size)

```bash
stat -f%z episodes/XXX-nom-episodi.mp3
```

---

### PAS 5: Llegir la transcripció i episodis anteriors per context

1. Llegir `sources/XXX-nom-episodi-transcripcio.txt` per entendre el contingut.
2. Llegir els últims 2-3 episodis a `_episodes/` per buscar **referències creuades** (temes que continuen o es mencionen entre episodis).

---

### PAS 6: Personalitzar el markdown de l'episodi

Editar `_episodes/XXX-nom-episodi.md` amb el format definitiu:

```yaml
---
audio_file: ""  # Es completarà al PAS 7 (upload a archive.org)
audio_size: MIDA_BYTES
date: 'YYYY-MM-DD'
description: "Descripció rica i detallada basada en la transcripció"
duration: 'MM:SS'
episode_number: N
season: 1
sources:
- title: "Acta del Ple Municipal de MES ANY"
  url: "URL_ACTA"
  description: "Ordre del dia i acta oficial del ple del DIA de MES de ANY"
- title: "Videoacta del Ple Municipal"
  url: "URL_YOUTUBE"
  description: "Enregistrament complet de la sessió plenària"
- title: "Transcripció automàtica de l'episodi"
  url: "/podcast/sources/XXX-nom-episodi-transcripcio.txt"
  description: "Transcripció completa generada amb OpenAI Whisper (model large-v3)"
title: "Episodi XXX: Títol descriptiu i enganxós"
---

## Introducció

Paràgraf curt que resumeix l'episodi i el context.

## Temes tractats

- **Tema 1**: Descripció breu amb detalls rellevants
- **Tema 2**: Descripció breu, inclou noms i dades concretes
- **Tema 3**: Si un tema apareix en episodis anteriors, afegir referència creuada: Episodi XXX a `/podcast/episodi/XXX-nom-episodi/`

## Fonts

- Títol font (URL_FONT) - Descripció
- Videoacta del Ple Municipal (URL_YOUTUBE) - Enregistrament complet
- Transcripció automàtica (`/podcast/sources/XXX-nom-episodi-transcripcio.txt`) - Generada amb OpenAI Whisper (model large-v3)

---

**Important:** Aquest episodi ha estat generat amb Google NotebookLM basant-se en fonts oficials. La transcripció s'ha generat automàticament amb OpenAI Whisper (model large-v3). Consulta sempre les fonts originals per obtenir la informació completa.
```

**Contingut del body (NO la transcripció sencera al markdown):**
- Secció "Introducció" amb resum curt
- Secció "Temes tractats" amb bullets detallats extrets de la transcripció
- Secció "Fonts" amb enllaços
- Disclaimer final
- **Referències creuades** a episodis anteriors si temes es repeteixen

**IMPORTANT:** Compara amb episodis recents (009, 010) per mantenir el format consistent. L'episodi 009 inclou la transcripció sencera al body; l'episodi 010 NO la inclou (millor patró). Segueix el patró de l'episodi 010 com a referència.

---

### PAS 7: Actualitzar `upload_to_archive.py` amb el nou episodi

**IMPORTANT:** L'script `scripts/upload_to_archive.py` té una llista `EPISODIS` hardcoded. Cal afegir el nou episodi a la llista ABANS de pujar.

Afegir una nova entrada al final de la llista `EPISODIS`:

```python
{
    "num": "XXX",
    "fitxer": "XXX-nom-episodi.mp3",
    "identifier": "podcast-cangaieta-XXX-nom-episodi",
    "title": "Episodi XXX: Títol",
    "description": "Descripció",
    "date": "YYYY-MM-DD",
    "duration": "MM:SS",
    "tags": ["podcast", "tiana", "ajuntament", "can gaieta", "catalunya", "notebooklm", ...tags_específics]
}
```

---

### PAS 8: Pujar MP3 a archive.org

```bash
source .venv/bin/activate && python scripts/upload_to_archive.py --episodi XXX
```

Això:
- Puja l'MP3 a archive.org
- Genera la URL: `https://archive.org/download/podcast-cangaieta-XXX-nom-episodi/XXX-nom-episodi.mp3`
- Actualitza automàticament el camp `audio_file` del markdown

**Si falla per rate limit:** informar l'usuari que cal esperar 30-60 minuts.

Verificar que `audio_file` al markdown s'ha actualitzat correctament. Si no, actualitzar-lo manualment.

---

### PAS 9: Verificació final

Abans de fer deploy, comprovar:

1. ✅ `_episodes/XXX-nom-episodi.md` té tots els camps YAML complets
2. ✅ `audio_file` apunta a archive.org (URL completa amb https://)
3. ✅ `audio_size` conté la mida en bytes
4. ✅ `duration` té el format `MM:SS` correcte
5. ✅ `sources` inclou totes les fonts (acta, videoacta, transcripció)
6. ✅ La transcripció existeix a `sources/`
7. ✅ El contingut del body és correcte (introducció, temes, fonts, disclaimer)
8. ✅ `scripts/upload_to_archive.py` conté el nou episodi a la llista

Mostrar un resum a l'usuari per confirmar.

---

### PAS 10: Deploy (git commit + push)

**Demanar confirmació a l'usuari** abans de fer push.

```bash
git add _episodes/XXX-nom-episodi.md sources/XXX-nom-episodi-transcripcio.txt scripts/upload_to_archive.py
git commit -m "Add episode XXX: [títol]"
git push
```

**RECORDAR:**
- Els fitxers MP3 a `episodes/` NO es pugen a GitHub (estan al .gitignore)
- Només es puja el markdown, la transcripció i l'script actualitzat
- El RSS s'actualitza automàticament amb el push

---

## REGLES IMPORTANTS

- **Idioma**: Tot el contingut en **català**
- **Disclaimer**: Sempre incloure que el contingut és generat amb Google NotebookLM
- **Fonts**: Sempre transparents i accessibles — mai inventar URLs
- **Audio**: Mai incloure MP3 al git — sempre archive.org
- **Format de noms**: `XXX-nom-descriptiu` (3 dígits amb zeros)
- **Transcripció al body**: NO incloure la transcripció sencera al markdown de l'episodi (guardar-la només a `sources/`)
- **CTA**: No cal tocar-lo — ja s'afegeix automàticament al layout i al feed.xml
