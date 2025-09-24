# Directori d'Episodis del Podcast

Aquest directori conté tots els fitxers d'audio dels episodis del podcast.

## Convenció de Nomenclatura

Els fitxers MP3 han de seguir aquest format:

```
[NÚM_EPISODI]-[TÍTOL_CURT]-[DATA].mp3
```

### Exemples:
- `001-pisos-can-gaieta-caut.mp3`
- `002-ple-ajuntament-gener.mp3`
- `003-obres-carrer-major.mp3`

### Components:
- **NÚM_EPISODI**: Número de 3 dígits (001, 002, 003...)
- **TÍTOL_CURT**: Títol descriptiu curt, només lletres minúscules, números i guions
- **DATA**: Opcional, format AAAA-MM-DD o MM-DD

## Recomanacions per als Fitxers MP3

### Qualitat d'Audio:
- **Bitrate**: 128 kbps (bon equilibri qualitat/mida)
- **Freqüència de mostreig**: 44.1 kHz
- **Format**: MP3 (màxima compatibilitat)

### Metadades:
Assegura't que els fitxers MP3 tinguin aquestes etiquetes:
- **Títol**: Nom complet de l'episodi
- **Artista**: "Associació Veïnal de Can Gaietà"
- **Àlbum**: "Podcast Can Gaietà"
- **Any**: Any de publicació
- **Gènere**: "Podcast" o "News & Politics"
- **Número de pista**: Número de l'episodi

### Mida dels Fitxers:
- Episodis de ~10 minuts: ~10-12 MB
- Si superes els 15 MB, considera reduir el bitrate a 96 kbps

## Estructura Actual:

```
episodes/
├── README.md                        # Aquest fitxer
├── 001-pisos-can-gaieta-caut.mp3   # Episodi 1 (quan el pujis)
└── [futurs episodis]
```

## Còpia de Seguretat

Recorda mantenir sempre una còpia de seguretat dels fitxers originals abans de pujar-los al repositori, ja que GitHub té límits de mida de fitxer (100 MB màxim per fitxer).