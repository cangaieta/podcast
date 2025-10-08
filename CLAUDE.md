# Instruccions per a Claude Code - Podcast Can Gaietà

## Resum del Projecte

Aquest és un podcast informatiu de l'Associació Veïnal de Can Gaietà que ofereix una font d'informació alternativa sobre els esdeveniments de Tiana. El contingut s'genera amb **Google NotebookLM** basant-se en fonts oficials.

## Estructura del Projecte

```
/
├── episodes/           # Fitxers MP3 dels episodis
├── _episodes/          # Fitxers markdown amb metadades dels episodis
├── sources/            # Fonts i transcripcions
├── scripts/            # Scripts d'automatització
├── assets/             # Logo i imatges
├── _layouts/           # Plantilles Jekyll
└── feed.xml           # RSS feed del podcast
```

## Workflow per Nous Episodis

### 1. **Preparar el nou episodi**
```bash
# Pujar l'MP3 a episodes/ amb format: XXX-nom-episodi.mp3
# Exemple: 002-ple-ajuntament-octubre.mp3
```

### 2. **Instal·lar dependències (primera vegada)**
```bash
pip install -r requirements.txt
```

### 3. **Transcripció automàtica**
```bash
# Episodis curts (≤10 minuts) - usar model medium:
python scripts/transcribe_episode.py episodes/002-nom-episodi.mp3 --model medium

# Episodis llargs (>10 minuts) - usar model small:
python scripts/transcribe_episode.py episodes/003-nom-episodi.mp3 --model small

# Opció ràpida (detecta automàticament):
./scripts/quick_transcribe.sh episodes/002-nom-episodi.mp3
```

**Què fa automàticament:**
- Transcriu l'MP3 amb OpenAI Whisper
- Crea `_episodes/002-nom-episodi.md` amb metadades
- Guarda transcripció a `sources/002-nom-episodi-transcripcio.txt`
- Genera descripció automàtica

### 4. **Personalitzar l'episodi**
Editar `_episodes/XXX-nom-episodi.md`:

```yaml
---
title: "Episodi X: Títol Personalitzat"
date: 2024-XX-XX
duration: "XX:XX"  # Actualitzar amb durada real
audio_file: "XXX-nom-episodi.mp3"
description: "Descripció personalitzada basada en el contingut"
sources:
  - title: "Font principal"
    url: "URL_real"
    description: "Descripció de la font"
  - title: "Videoacta sessió"
    url: "https://youtu.be/..."
    description: "..."
---
```

**Contingut a actualitzar:**
- Títol més descriptiu
- Descripció basada en transcripció
- Fonts reals utilitzades per NotebookLM
- Durada exacte de l'episodi
- Contingut principal de l'episodi

### 5. **Afegir fonts utilitzades**
Sempre especificar:
- **Article/document principal** (nom publicació, número, data)
- **Videoactes** (URL YouTube amb timestamp directe)
- **Transcripcions manuals** (si n'hi ha)
- **Documents oficials** (actes, resolucions, etc.)

### 6. **Deploy**
```bash
git add .
git commit -m "Add episode XXX: [títol]"
git push
```

## Consideracions Importants

### **Disclaimer sempre present**
Tots els episodis han d'incloure:
- Contingut generat amb Google NotebookLM
- Basat en fonts oficials reals
- Fonts sempre transparents i accessibles
- Enllaç a la web oficial: https://cangaieta.cat

### **Format de fitxers**
- **MP3**: `XXX-nom-descriptiu.mp3`
- **Episodis**: `_episodes/XXX-nom-descriptiu.md`
- **Transcripcions**: `sources/XXX-nom-descriptiu-transcripcio.txt`

### **Qualitat MP3**
- **Bitrate**: 128 kbps
- **Durada**: ~10 minuts
- **Mida**: ~10-12 MB

## Scripts Disponibles

### **Transcripció**
- `scripts/quick_transcribe.sh` - Script ràpid
- `scripts/transcribe_episode.py` - Script principal amb opcions
- Models Whisper: `tiny`, `small`, `medium` (recomanat), `large`

### **Models de Whisper**

**Acceleració hardware:**
- ⚠️ **Apple Silicon (M1/M2/M3)**: MPS no compatible amb Whisper (error SparseMPS)
- ✅ **CUDA (NVIDIA)**: Suportat i accelerat
- 💻 **CPU**: Mode per defecte en Macs, funciona correctament

**Temps de transcripció (CPU M1/M2):**
- Model `small`: ~5:40 per episodi de 26 min (ràtio ~1:5)
- Model `medium`: més lent, ~1:4 o menys

**Selecció de model:**
- `medium`: **Recomanat per català**, bon equilibri velocitat/qualitat
  - ⚠️ **Limitació**: Només per episodis **≤10 minuts** (timeout 10 min en CPU)
  - Temps: ~2 min per episodi de 10 min
- `small`: **Usar per episodis >10 minuts** (sense limitació de timeout)
  - Exemple: episodi de 26 min → 5:40 min transcripció
  - Qualitat suficient per català
  - **Recomanat per episodis llargs**
- `large`: Màxima precisió, molt més lent
- `tiny`: Només per proves ràpides

## Paleta de Colors (per gràfics/imatges)

- **Terra Cuita**: `#CD6155`
- **Taronja Càlid**: `#E67E22`
- **Rosa Salmó**: `#F1948A`
- **Verd Natura**: `#4C8150`
- **Beix Clar**: `#F5EEDC`
- **Blanc Pur**: `#FFFFFF`

## URLs Importants

- **Web del podcast**: https://cangaieta.github.io/podcast
- **RSS feed**: https://cangaieta.github.io/podcast/feed.xml
- **Repositori**: https://github.com/cangaieta/podcast
- **Web oficial AV**: https://cangaieta.cat
- **Google NotebookLM**: https://notebooklm.google

## Solució de Problemes

### **Error en transcripció**
```bash
# Verificar Whisper
python -c "import whisper; print('Whisper OK')"

# Reinstal·lar si cal
pip install --upgrade openai-whisper
```

### **Error en RSS feed**
- Comprovar caràcters especials en títols/descripcions
- Verificar que tots els camps XML estan ben escapats

### **Error en GitHub Pages**
- Revisar que el YAML dels episodis és vàlid
- Comprovar que no hi ha caràcters especials en noms de fitxers

## Tasques Recurrents

### **Cada episodi:**
1. Transcriure automàticament
2. Personalitzar contingut
3. Verificar fonts
4. Deploy

### **Setmanalment:**
- Revisar que RSS funciona
- Comprovar mètriques web (si n'hi ha)
- Mantenir repositori actualitzat

### **Mensualment:**
- Actualitzar dependències Python
- Revisar documentació
- Backup de transcripcions importants