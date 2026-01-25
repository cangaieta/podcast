# Script de Pujada Automàtica a Archive.org

Aquest script automatitza completament el procés de pujar episodis del podcast a archive.org.

## Configuració Inicial (només primera vegada)

```bash
# 1. Instal·lar dependències
pip install -r requirements.txt

# 2. Configurar credencials d'archive.org
ia configure
```

T'ha demanarà:
- **Email**: El teu email d'archive.org
- **Password**: La teva contrasenya

Les credencials es guarden a `~/.config/ia.ini` i no cal tornar-les a introduir.

## Ús

### Mode DRY-RUN (recomanat primer cop)

```bash
python scripts/upload_to_archive.py --dry-run
```

Mostra què faria **sense pujar res realment**. Útil per verificar que tot és correcte.

### Pujar tots els episodis

```bash
python scripts/upload_to_archive.py
```

Això:
- Puja els 9 episodis a archive.org
- Crea els ítems amb totes les metadades correctes
- Genera les URLs públiques
- Actualitza automàticament el camp `audio_file` de cada markdown

### Pujar només un episodi específic

```bash
python scripts/upload_to_archive.py --episodi 009
```

### Pujar sense actualitzar els markdowns

```bash
python scripts/upload_to_archive.py --no-update-md
```

## Què fa l'script automàticament?

Per cada episodi:

1. ✅ **Comprova** si el fitxer MP3 existeix
2. ✅ **Crea les metadades** amb format correcte:
   - Title: `Podcast Can Gaietà - Episodi XXX: Títol`
   - Creator: `Associació Veïnal de Can Gaietà`
   - Description amb disclaimer de NotebookLM
   - Tags apropiats
   - Llicència CC BY 4.0
   - Data, durada, idioma...
3. ✅ **Comprova** si l'ítem ja existeix a archive.org
4. ✅ **Puja** el fitxer amb `queue_derive=True` (processament automàtic)
5. ✅ **Genera la URL** pública: `https://archive.org/download/[identifier]/[fitxer].mp3`
6. ✅ **Actualitza** el markdown corresponent amb la nova URL
7. ✅ **Mostra resum** amb totes les URLs generades

## Exemple de sortida

```
🎙️  Script de pujada automàtica a archive.org
============================================================

📋 Episodis a processar: 9

📦 Pujant episodi 001: Què es va dir realment sobre els pisos de Can Gaietà al CAUT?
   Fitxer: /path/to/episodes/001-pisos-can-gaieta-caut.mp3
   Identifier: podcast-cangaieta-001-pisos-can-gaieta-caut
   ✅ Pujat correctament!
   📍 URL: https://archive.org/download/podcast-cangaieta-001-pisos-can-gaieta-caut/001-pisos-can-gaieta-caut.mp3
   🌐 Pàgina: https://archive.org/details/podcast-cangaieta-001-pisos-can-gaieta-caut
   ✏️  Actualitzat markdown

...

============================================================
📊 RESUM
============================================================
✅ Episodis processats: 9/9

📍 URLs generades:
   001: https://archive.org/download/podcast-cangaieta-001-pisos-can-gaieta-caut/001-pisos-can-gaieta-caut.mp3
   002: https://archive.org/download/podcast-cangaieta-002-el-laberint-burocratic/002-el-laberint-burocratic.mp3
   ...

💡 Recorda fer:
   git add _episodes/
   git commit -m 'Migrar URLs a archive.org'
   git push
```

## Després de pujar

```bash
# Verificar els canvis
git status

# Veure les diferències
git diff _episodes/

# Commit i push
git add _episodes/
git commit -m "Migrar episodis a archive.org"
git push
```

## Gestió d'errors

### Si un ítem ja existeix

L'script preguntarà:
```
⚠️  L'ítem ja existeix a archive.org
Vols sobreescriure'l? (s/N):
```

- `s` → Sobreescriu
- `N` → Salta aquest episodi

### Si falta un fitxer MP3

```
❌ ERROR: No s'ha trobat el fitxer /path/to/episodes/XXX.mp3
```

Verifica que el fitxer existeix a `episodes/`.

### Si falla la pujada

L'script reintentarà fins a 3 vegades automàticament. Si continua fallant, mostra l'error i continua amb el següent episodi.

## Opcions avançades

```bash
# Ajuda
python scripts/upload_to_archive.py --help

# Mode verbós (ja està actiu per defecte)
python scripts/upload_to_archive.py --verbose
```

## Estructura de les metadades

Cada episodi es puja amb:

- **Identifier**: `podcast-cangaieta-XXX-nom-episodi` (únic)
- **Title**: Títol complet amb "Podcast Can Gaietà"
- **MediaType**: `audio`
- **Collection**: `community_audio`
- **Creator**: `Associació Veïnal de Can Gaietà`
- **Description**: Descripció + disclaimer NotebookLM + enllaços
- **Date**: Data de publicació original
- **Language**: `cat` (Català)
- **License**: CC BY 4.0
- **Subject**: Tags separats per `;`
- **Duration**: Durada de l'episodi
- **External-ID**: URN únic del podcast

## Recursos

- [Documentació Archive.org API](https://archive.org/services/docs/api/)
- [internetarchive CLI](https://github.com/jjjake/internetarchive)
- [ARCHIVE_ORG.md](../ARCHIVE_ORG.md) - Guia completa d'archive.org
- [ARCHIVE_ORG_METADADES_EPISODIS.md](../ARCHIVE_ORG_METADADES_EPISODIS.md) - Metadades de cada episodi
