# Guia per Pujar Episodis a Archive.org

## Per què Archive.org?

**Archive.org (Internet Archive)** és una organització sense ànim de lucre dedicada a preservar la història digital. És ideal per allotjar podcasts perquè:

- ✅ **Gratuït i il·limitat**: No hi ha límits de mida ni bandwidth
- ✅ **Preservació permanent**: Compromís de mantenir el contingut per sempre
- ✅ **URLs estables**: Les URLs no canvien mai
- ✅ **Missió cultural**: Arxiu de contingut educatiu i cultural
- ✅ **No requereix servidor propi**: Estalvi de costos d'allotjament
- ✅ **API disponible**: Per automatitzacions futures

## Automatització amb Script Python ✨

### Primera vegada: Configurar credencials

```bash
# Instal·lar la CLI d'archive.org (ja està al requirements.txt)
pip install internetarchive

# Configurar credencials (només primera vegada)
ia configure
```

T'ha demanarà el teu **email** i **password** d'archive.org.

### Pujar tots els episodis automàticament

```bash
# Mode DRY-RUN (veure què faria sense pujar res)
python scripts/upload_to_archive.py --dry-run

# Pujar TOTS els episodis i actualitzar markdowns
python scripts/upload_to_archive.py

# Pujar només un episodi específic
python scripts/upload_to_archive.py --episodi 009

# Pujar sense actualitzar els markdowns
python scripts/upload_to_archive.py --no-update-md
```

### Què fa l'script automàticament?

✅ **Puja cada MP3** a archive.org amb totes les metadades
✅ **Comprova si ja existeix** l'ítem i pregunta si vols sobreescriure
✅ **Genera les URLs** correctes per cada episodi
✅ **Actualitza automàticament** el camp `audio_file` dels markdowns
✅ **Mostra un resum** amb totes les URLs generades

### Després de pujar

```bash
# Verificar els canvis
git status

# Commit i push
git add _episodes/
git commit -m "Migrar episodis a archive.org"
git push
```

---

## Procés Manual (si prefereixes)

Si prefereixes pujar manualment cadascun, segueix aquest procés:

### 1. Crear Compte (primera vegada)
1. Anar a https://archive.org
2. Clicar "Sign Up" al menú superior dret
3. Crear compte amb email de l'associació
4. Verificar email

### 2. Pujar un Episodi
1. **Login** a archive.org
2. Clicar **"Upload"** al menú superior
3. Emplenar formulari:

#### **Metadades Obligatòries:**

**Identifier** (URL única):
```
podcast-cangaieta-XXX-nom-episodi
```
⚠️ Ha de ser únic, sense espais, només lletres, números i guions

**Title**:
```
Podcast Can Gaietà - Episodi XXX: Títol Complet
```

**Creator**:
```
Associació Veïnal de Can Gaietà
```

**Description**:
```
[Descripció de l'episodi]

⚠️ Aquest contingut ha estat generat amb Google NotebookLM basant-se en fonts oficials de l'Ajuntament de Tiana. Pot contenir interpretacions de la IA que no encaixin completament amb la realitat. Consulta sempre les fonts originals.

Més informació: https://cangaieta.cat
Podcast: https://cangaieta.github.io/podcast
```

**Subject Tags** (separats per comes):
```
podcast, tiana, ajuntament, can gaieta, catalunya, notebooklm, informacio municipal
```

**Collection**:
- Primera opció: `community_audio` (recomanat per podcasts)
- Alternativa: `opensource_audio`

**License**:
```
Creative Commons - Attribution 4.0 International (CC BY 4.0)
```
Permet que altres comparteixin amb atribució

#### **Metadades Recomanades:**

**Language**:
```
Catalan
```

**Date**:
```
2026-01-XX (data de publicació)
```

**Website**:
```
https://cangaieta.cat
```

### 3. Pujar Fitxer MP3
- Arrossegar o seleccionar l'MP3 de `episodes/XXX-nom-episodi.mp3`
- Esperar que es completi la pujada (pot trigar segons mida)

### 4. Obtenir URL Pública
Un cop pujat, la URL serà:
```
https://archive.org/download/podcast-cangaieta-XXX-nom-episodi/XXX-nom-episodi.mp3
```

També es pot obtenir des de:
- Pàgina de l'ítem → Clicar fitxer MP3 → Botó dret → "Copiar enllaç"

### 5. Actualitzar Episodi al Podcast
Editar `_episodes/XXX-nom-episodi.md` i posar la URL completa:
```yaml
audio_file: "https://archive.org/download/podcast-cangaieta-XXX-nom-episodi/XXX-nom-episodi.mp3"
```

## URLs d'Archive.org

### Pàgina de l'ítem:
```
https://archive.org/details/podcast-cangaieta-XXX-nom-episodi
```

### URL directa MP3 (per RSS):
```
https://archive.org/download/podcast-cangaieta-XXX-nom-episodi/XXX-nom-episodi.mp3
```

### Streaming player:
```
https://archive.org/embed/podcast-cangaieta-XXX-nom-episodi
```

## Consideracions

### ✅ Avantatges
- Preservació permanent
- Sense costos
- Bandwidth il·limitat
- Part d'un arxiu cultural

### ⚠️ Limitacions
- El procés de pujada és manual (es pot automatitzar amb API)
- Triga ~10-30 minuts a processar després de pujar
- No es pot editar metadata fàcilment (millor fer-ho bé la primera vegada)

## Automatització amb Script Python ✨

### Primera vegada: Configurar credencials

```bash
# Instal·lar la CLI d'archive.org (ja està al requirements.txt)
pip install internetarchive

# Configurar credencials (només primera vegada)
ia configure
```

T'ha demanarà el teu **email** i **password** d'archive.org.

### Pujar tots els episodis automàticament

```bash
# Mode DRY-RUN (veure què faria sense pujar res)
python scripts/upload_to_archive.py --dry-run

# Pujar TOTS els episodis i actualitzar markdowns
python scripts/upload_to_archive.py

# Pujar només un episodi específic
python scripts/upload_to_archive.py --episodi 009

# Pujar sense actualitzar els markdowns
python scripts/upload_to_archive.py --no-update-md
```

### Què fa l'script automàticament?

✅ **Puja cada MP3** a archive.org amb totes les metadades
✅ **Comprova si ja existeix** l'ítem i pregunta si vols sobreescriure
✅ **Genera les URLs** correctes per cada episodi
✅ **Actualitza automàticament** el camp `audio_file` dels markdowns
✅ **Mostra un resum** amb totes les URLs generades

### Després de pujar

```bash
# Verificar els canvis
git status

# Commit i push
git add _episodes/
git commit -m "Migrar episodis a archive.org"
git push
```

## Automatització Manual (si prefereixes)

Si prefereixes pujar manualment, segueix el procés descrit a continuació.

## Migració d'Episodis Existents

Per episodis anteriors que ja estan a GitHub:

1. Pujar cada MP3 a archive.org seguint aquest procés
2. Actualitzar el camp `audio_file` de cada `_episodes/XXX.md`
3. Fer commit dels canvis
4. Els MP3 locals es mantenen a `episodes/` però no es pugen a GitHub

## Checklist per Cada Episodi

- [ ] MP3 desat localment a `episodes/XXX-nom.mp3`
- [ ] Pujat a archive.org amb metadades correctes
- [ ] URL copiada d'archive.org
- [ ] `audio_file` actualitzat al markdown amb URL completa
- [ ] Commit i push del markdown (sense MP3)
- [ ] Verificar que RSS funciona amb nova URL

## Suport

- **Documentació oficial**: https://help.archive.org/
- **Fòrum**: https://archive.org/about/contact.php
- **Email**: info@archive.org
