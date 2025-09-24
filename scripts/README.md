# Scripts d'Automatització del Podcast

## Instal·lació

1. **Instal·la les dependències Python:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Comprova que Whisper funciona:**
   ```bash
   python -c "import whisper; print('Whisper OK')"
   ```

## Ús Ràpid

### Transcriure un nou episodi:

```bash
# Opció 1: Script bash simple
./scripts/quick_transcribe.sh episodes/002-nou-episodi.mp3

# Opció 2: Script Python directe
python scripts/transcribe_episode.py episodes/002-nou-episodi.mp3
```

### El que fa automàticament:

1. **Transcriu l'MP3** amb OpenAI Whisper
2. **Genera una descripció** automàtica dels primers paràgrafs
3. **Crea el fitxer markdown** a `_episodes/XXX-nom-episodi.md`
4. **Guarda la transcripció completa** a `sources/XXX-nom-episodi-transcripcio.txt`

### Després de la transcripció:

1. **Edita l'episodi:** `_episodes/XXX-nom-episodi.md`
   - Revisa el títol i descripció
   - Afegeix les fonts reals utilitzades
   - Ajusta la durada

2. **Commit i push:**
   ```bash
   git add .
   git commit -m "Add episode XXX with auto-transcription"
   git push
   ```

## Opcions Avançades

### Models de Whisper disponibles:
- `tiny` - Més ràpid, menys precís
- `small` - Equilibri velocitat/qualitat
- `medium` - **Recomanat** per català
- `large` - Màxima precisió, més lent

```bash
# Usar model específic
python scripts/transcribe_episode.py episodes/002-nom.mp3 --model large
```

### Personalitzar directoris:
```bash
python scripts/transcribe_episode.py episodes/002-nom.mp3 \
  --output-episode custom_episodes \
  --output-transcript custom_sources
```

## Solució de Problemes

### Error: "No module named 'whisper'"
```bash
pip install openai-whisper
```

### Error: Model massa lent
```bash
# Usa un model més petit
python scripts/transcribe_episode.py episodes/002-nom.mp3 --model small
```

### Error: Arxiu no trobat
- Comprova que el fitxer MP3 existeix
- Usa rutes relatives des de l'arrel del projecte

## Format dels Fitxers

### Noms d'episodis esperats:
- `001-pisos-can-gaieta.mp3` → "Pisos Can Gaieta"
- `002-ple-ajuntament-octubre.mp3` → "Ple Ajuntament Octubre"

### Estructura generada:
```
_episodes/001-pisos-can-gaieta.md     # Episodi amb metadades
sources/001-pisos-can-gaieta-transcripcio.txt  # Transcripció completa
```

## Millores Futures

- [ ] Detecció automàtica de durada
- [ ] Integració amb NotebookLM API
- [ ] Generació automàtica de títols més intel·ligents
- [ ] Detecció de temes principals