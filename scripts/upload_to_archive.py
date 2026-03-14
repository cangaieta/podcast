#!/usr/bin/env python3
"""
Script per pujar automàticament tots els episodis del podcast a archive.org
Requereix: pip install internetarchive
Configuració: ia configure (només primera vegada)
"""

import os
import sys
from pathlib import Path
from internetarchive import upload, get_item

# Configuració del podcast
CREATOR = "Associació Veïnal de Can Gaietà"
COLLECTION = None  # No especificar col·lecció - es crearà al compte personal
LICENSE = "http://creativecommons.org/licenses/by/4.0/"
LANGUAGE = "cat"
WEBSITE = "https://cangaieta.cat"
PODCAST_URL = "https://cangaieta.github.io/podcast"

# Definició dels episodis amb les seves metadades
EPISODIS = [
    {
        "num": "001",
        "fitxer": "001-pisos-can-gaieta-caut.mp3",
        "identifier": "podcast-cangaieta-001-pisos-can-gaieta-caut",
        "title": "Episodi 001: Què es va dir realment sobre els pisos de Can Gaietà al CAUT?",
        "description": "Analitzem l'article 'Així seran els pisos de Can Gaietà' i contrastem amb el que realment es va dir a la sessió del CAUT. Una exploració sobre comunicació, transparència i participació veïnal.",
        "date": "2025-09-24",
        "duration": "12:41",
        "tags": ["podcast", "tiana", "ajuntament", "can gaieta", "catalunya", "notebooklm", "informacio municipal", "urbanisme", "habitatge", "participacio ciutadana"]
    },
    {
        "num": "002",
        "fitxer": "002-el-laberint-burocratic.mp3",
        "identifier": "podcast-cangaieta-002-el-laberint-burocratic",
        "title": "Episodi 002: El Laberint Burocràtic - Quan Arreglar uns Bancs es Converteix en una Investigació",
        "description": "Quan una proposta ciutadana tan simple com arreglar uns bancs acaba convertint-se en una investigació sobre transparència municipal. Una història que il·lustra com les contradiccions administratives poden minar la confiança en la participació ciutadana.",
        "date": "2025-09-26",
        "duration": "6:07",
        "tags": ["podcast", "tiana", "ajuntament", "can gaieta", "catalunya", "notebooklm", "transparencia", "pressupostos participatius", "burocràcia"]
    },
    {
        "num": "003",
        "fitxer": "003-ple-octubre-2025.mp3",
        "identifier": "podcast-cangaieta-003-ple-octubre-2025",
        "title": "Episodi 003: Ple Octubre 2025",
        "description": "Anàlisi completa del Ple Municipal del 7 d'octubre de 2025: pujada de taxes de residus, demandes dels veïns dels Bessans, polèmiques sobre licitacions, mocions sobre el català i les ombres a les escoles, i la tensió pre-electoral que marca el debat polític a Tiana.",
        "date": "2025-10-08",
        "duration": "26:19",
        "tags": ["podcast", "tiana", "ajuntament", "can gaieta", "catalunya", "notebooklm", "ple municipal", "taxes", "fiscalitat", "participacio ciutadana"]
    },
    {
        "num": "004",
        "fitxer": "004-puja-fiscal-taxa-residus.mp3",
        "identifier": "podcast-cangaieta-004-puja-fiscal-taxa-residus",
        "title": "Episodi 004: La Puja Fiscal a Tiana - Per Què Pagarem un 60% Més de Taxa de Residus?",
        "description": "Anàlisi de la polèmica pujada del 60% de la taxa de residus aprovada al Ple Municipal del 7 d'octubre de 2025. Un debat tens entre l'obligació legal i la percepció de pagar més sense millora del servei, amb acusacions creuades entre govern i oposició sobre retards en la nova licitació.",
        "date": "2025-10-15",
        "duration": "6:50",
        "tags": ["podcast", "tiana", "ajuntament", "can gaieta", "catalunya", "notebooklm", "taxa residus", "escombraries", "fiscalitat"]
    },
    {
        "num": "005",
        "fitxer": "005-escola-bressol-ibi-deute-ple-tens.mp3",
        "identifier": "podcast-cangaieta-005-escola-bressol-ibi-deute-ple-tens",
        "title": "Episodi 005: Escola Bressol, IBI i Deute - El Ple Tens del 4 de Novembre",
        "description": "Anàlisi del ple municipal del 4 de novembre de 2025: licitació de l'Escola Bressol per 5,6 milions, la polèmica sobre la taxa de residus i l'IBI amb més de 1.000 signatures, i el reconeixement d'un deute de 225.000 euros sense contracte. Un ple marcat per la tensió política i el debat sobre la gestió municipal.",
        "date": "2025-11-06",
        "duration": "15:57",
        "tags": ["podcast", "tiana", "ajuntament", "can gaieta", "catalunya", "notebooklm", "escola bressol", "ibi", "fiscalitat", "contractacio publica"]
    },
    {
        "num": "006",
        "fitxer": "006-batalla-escombraries-barris-oblidats.mp3",
        "identifier": "podcast-cangaieta-006-batalla-escombraries-barris-oblidats",
        "title": "Episodi 006: La Batalla de les Escombraries i els Barris Oblidats",
        "description": "Anàlisi del Ple Municipal de Tiana del 2 de desembre de 2025: la batalla per la revisió de preus del contracte de residus, el model de porta a porta, la invisibilització dels barris perifèrics i la denúncia de doble imposició en la taxa d'escombraries.",
        "date": "2026-01-14",
        "duration": "13:57",
        "tags": ["podcast", "tiana", "ajuntament", "can gaieta", "catalunya", "notebooklm", "residus", "porta a porta", "barris", "invisibilitzacio"]
    },
    {
        "num": "007",
        "fitxer": "007-tiana-triplica-deute-municipal.mp3",
        "identifier": "podcast-cangaieta-007-tiana-triplica-deute-municipal",
        "title": "Episodi 007: Tiana Triplica el Deute Municipal",
        "description": "Anàlisi del Ple Extraordinari de Tiana del 29 de desembre de 2025: aprovació del pressupost 2026 amb un pla per triplicar el deute municipal (250%), confrontació entre la visió d'inversió valenta del govern i la prudència defensada per l'oposició, i un moment de col·laboració en la defensa dels treballadors de les cures.",
        "date": "2026-01-14",
        "duration": "13:05",
        "tags": ["podcast", "tiana", "ajuntament", "can gaieta", "catalunya", "notebooklm", "pressupostos", "deute municipal", "inversio", "finances"]
    },
    {
        "num": "008",
        "fitxer": "008-normes-fantasma-casa-entitats.mp3",
        "identifier": "podcast-cangaieta-008-normes-fantasma-casa-entitats",
        "title": "Episodi 008: Normes Fantasma i el Caos de la Casa d'Entitats",
        "description": "Quan una associació de veïns intenta fer la seva assemblea anual i es troba amb un mur de normes contradictòries, restriccions horàries inexplicables i regles fantasma que ningú ha aprovat. Anàlisi d'un cas que revela com els equipaments públics poden convertir-se en obstacles burocràtics en lloc de punts de trobada ciutadana.",
        "date": "2026-01-15",
        "duration": "13:18",
        "tags": ["podcast", "tiana", "ajuntament", "can gaieta", "catalunya", "notebooklm", "equipaments", "participacio", "transparencia", "entitats"]
    },
    {
        "num": "009",
        "fitxer": "009-festa-a-dit-bar-irregular-ridicul-solar.mp3",
        "identifier": "podcast-cangaieta-009-festa-a-dit-bar-irregular-ridicul-solar",
        "title": "Episodi 009: Festa a dit, bar irregular i ridícul solar",
        "description": "Anàlisi del ple municipal del 13 de gener de 2026 a Tiana. La síndica de greuges denuncia la passivitat de l'Ajuntament amb La Centraleta, un bar que funciona des del 2020 sense llicència d'activitat, certificat tècnic ni estudi d'impacte acústic. També examinem la polèmica de la comunitat energètica (un quilowatt de potència?), el sistema de porta a porta de residus, i la festa de Cap d'Any amb adjudicació a dit a Descorxats.",
        "date": "2026-01-22",
        "duration": "22:44",
        "tags": ["podcast", "tiana", "ajuntament", "can gaieta", "catalunya", "notebooklm", "sindica", "llicencies", "energia", "festes"]
    },
    {
        "num": "010",
        "fitxer": "010-antifrau-polemica-solar-auditoria-inexistent.mp3",
        "identifier": "podcast-cangaieta-010-antifrau-polemica-solar-auditoria-inexistent",
        "title": "Episodi 010: Antifrau, polèmica solar i l'auditoria inexistent",
        "description": "Anàlisi del ple municipal del 3 de febrer de 2026 a Tiana. L'oficina Antifrau de Catalunya arxiva una denúncia contra l'Ajuntament, però el govern transforma la notícia en un relat de victimisme. La polèmica de la comunitat energètica solar torna: la taxa aprovada no cobreix ni el manteniment. I al final, un veí posa el govern davant del seu propi programa electoral: l'auditoria econòmica promesa fa gairebé 4 anys que no s'ha fet. L'alcalde no respon.",
        "date": "2026-02-19",
        "duration": "11:39",
        "tags": ["podcast", "tiana", "ajuntament", "can gaieta", "catalunya", "notebooklm", "antifrau", "energia solar", "auditoria", "transparencia", "deixalleria", "rodalies"]
    },
    {
        "num": "011",
        "fitxer": "011-playstation-excusa-can-gaieta.mp3",
        "identifier": "podcast-cangaieta-011-playstation-excusa-can-gaieta",
        "title": "Episodi 011: La PlayStation com a excusa",
        "description": "La PlayStation com a excusa: l'Ajuntament de Tiana confessa per escrit que no existeix cap norma que justifiqui la prohibició d'ús de l'Espai Diòptria entre les 17h i les 20:30h. Anàlisi de l'expedient de transparència que revela el doble rasador de l'Ajuntament, les dades reals d'ocupació (11 dies amb 0 joves en 5 mesos) i com l'Associació Veïnal de Can Gaietà ha estat discriminada pel comportament d'altres entitats que ni tan sols s'identifiquen.",
        "date": "2026-03-10",
        "duration": "15:36",
        "tags": ["podcast", "tiana", "ajuntament", "can gaieta", "catalunya", "notebooklm", "transparencia", "equipaments", "espai jove", "dioptria", "participacio ciutadana", "entitats", "normes"]
    },
    {
        "num": "012",
        "fitxer": "012-autobusos-fantasma-lavabos-precintats.mp3",
        "identifier": "podcast-cangaieta-012-autobusos-fantasma-lavabos-precintats",
        "title": "Episodi 012: Autobusos fantasma i lavabos precintats",
        "description": "Anàlisi del ple municipal del 3 de març de 2026 a Tiana. El govern elimina les línies B34 i B35 per crear la nova B32 que connecta amb un CAP i un mercat que encara no existeixen. Un terreny públic de gairebé 4 milions que es cedeix a l'AMB malgrat que la caixa municipal té 7,9 milions en reserva. Lavabos del casal del poble clausurats amb bosses d'escombraries negres. I un alcalde que al final del ple assenyala públicament un veí i el vincula a l'extrema dreta.",
        "date": "2026-03-10",
        "duration": "15:25",
        "tags": ["podcast", "tiana", "ajuntament", "can gaieta", "catalunya", "notebooklm", "autobusos", "mobilitat", "calcfrares", "habitatge social", "residus", "casal", "antifrau", "participacio ciutadana", "ple municipal"]
    },
    {
        "num": "013",
        "fitxer": "013-youtuber-revista-pantalles.mp3",
        "identifier": "podcast-cangaieta-013-youtuber-revista-pantalles",
        "title": "Episodi 013: La contraportada que treballa contra les famílies: pantalles, menors i el problema de salut pública que amplifica",
        "description": "La contraportada de la revista municipal Plaça de la Vila celebra que un jove de Tiana va arribar als 100.000 subscriptors a YouTube havent-hi entrat als 12 anys, sense cap context mèdic ni advertències. En el mateix moment, Austràlia, França i Espanya legislen per prohibir les xarxes per a menors de 16 anys. L'oposició al ple del 3 de març ho qualifica de greu problema de salut pública i denuncia censura i desigualtat de tracte a la revista.",
        "date": "2026-03-11",
        "duration": "21:03",
        "tags": ["podcast", "tiana", "ajuntament", "can gaieta", "catalunya", "notebooklm", "pantalles", "menors", "salut publica", "youtube", "xarxes socials", "revista municipal", "placa de la vila", "pediatria", "dark patterns", "ple municipal"]
    }
]


def crear_metadata(episodi):
    """Crea el diccionari de metadades per archive.org"""
    
    description_completa = f"""{episodi['description']}

⚠️ Aquest contingut ha estat generat amb Google NotebookLM basant-se en fonts oficials de l'Ajuntament de Tiana. Pot contenir interpretacions de la IA que no encaixin completament amb la realitat. Consulta sempre les fonts originals.

Més informació: {WEBSITE}
Podcast: {PODCAST_URL}"""
    
    metadata = {
        'title': f"Podcast Can Gaietà - {episodi['title']}",
        'mediatype': 'audio',
        'creator': CREATOR,
        'description': description_completa,
        'date': episodi['date'],
        'language': LANGUAGE,
        'licenseurl': LICENSE,
        'subject': ';'.join(episodi['tags']),
        'duration': episodi['duration'],
        'external-identifier': f'urn:podcast:cangaieta:{episodi["num"]}',
    }
    
    # Afegir col·lecció només si està definida
    if COLLECTION:
        metadata['collection'] = COLLECTION
    
    return metadata


def pujar_episodi(episodi, episodes_dir, dry_run=False):
    """Puja un episodi a archive.org"""
    
    fitxer_path = episodes_dir / episodi['fitxer']
    
    if not fitxer_path.exists():
        print(f"❌ ERROR: No s'ha trobat el fitxer {fitxer_path}")
        return None
    
    identifier = episodi['identifier']
    metadata = crear_metadata(episodi)
    
    print(f"\n📦 Pujant episodi {episodi['num']}: {episodi['title']}")
    print(f"   Fitxer: {fitxer_path}")
    print(f"   Identifier: {identifier}")
    
    if dry_run:
        print("   🔍 MODE DRY-RUN: No es puja realment")
        print(f"   Metadades: {metadata}")
        url = f"https://archive.org/download/{identifier}/{episodi['fitxer']}"
        return url
    
    try:
        # Comprovar si ja existeix
        item = get_item(identifier)
        if item.exists:
            print(f"   ⚠️  L'ítem ja existeix a archive.org")
            resposta = input("   Vols sobreescriure'l? (s/N): ")
            if resposta.lower() != 's':
                print("   ⏭️  Saltat")
                url = f"https://archive.org/download/{identifier}/{episodi['fitxer']}"
                return url
        
        # Pujar el fitxer
        r = upload(
            identifier,
            files=[str(fitxer_path)],
            metadata=metadata,
            verify=True,
            verbose=True,
            queue_derive=True,
            retries=3
        )
        
        if r[0].status_code == 200:
            url = f"https://archive.org/download/{identifier}/{episodi['fitxer']}"
            print(f"   ✅ Pujat correctament!")
            print(f"   📍 URL: {url}")
            print(f"   🌐 Pàgina: https://archive.org/details/{identifier}")
            return url
        else:
            print(f"   ❌ Error en pujar: {r[0].status_code}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None


def actualitzar_markdown(episodi, url, episodes_md_dir):
    """Actualitza el camp audio_file del markdown de l'episodi"""
    
    md_file = episodes_md_dir / f"{episodi['fitxer'].replace('.mp3', '.md')}"
    
    if not md_file.exists():
        print(f"   ⚠️  No s'ha trobat el markdown: {md_file}")
        return False
    
    try:
        content = md_file.read_text()
        
        # Buscar la línia audio_file i reemplaçar-la
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('audio_file:'):
                old_value = line
                lines[i] = f'audio_file: "{url}"'
                print(f"   ✏️  Actualitzat markdown:")
                print(f"      Abans: {old_value}")
                print(f"      Ara:   {lines[i]}")
                break
        
        md_file.write_text('\n'.join(lines))
        return True
        
    except Exception as e:
        print(f"   ❌ Error actualitzant markdown: {e}")
        return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Puja episodis a archive.org')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Mostra què es faria sense pujar res')
    parser.add_argument('--episodi', type=str,
                       help='Pujar només un episodi específic (ex: 001)')
    parser.add_argument('--no-update-md', action='store_true',
                       help='No actualitzar els fitxers markdown')
    
    args = parser.parse_args()
    
    # Directoris del projecte
    project_dir = Path(__file__).parent.parent
    episodes_dir = project_dir / 'episodes'
    episodes_md_dir = project_dir / '_episodes'
    
    print("🎙️  Script de pujada automàtica a archive.org")
    print("=" * 60)
    
    # Filtrar episodis si s'ha especificat un
    episodis_a_pujar = EPISODIS
    if args.episodi:
        episodis_a_pujar = [e for e in EPISODIS if e['num'] == args.episodi]
        if not episodis_a_pujar:
            print(f"❌ No s'ha trobat l'episodi {args.episodi}")
            sys.exit(1)
    
    print(f"\n📋 Episodis a processar: {len(episodis_a_pujar)}")
    
    if args.dry_run:
        print("\n🔍 MODE DRY-RUN ACTIVAT - No es pujarà res realment\n")
    
    # Processar cada episodi
    urls_generades = {}
    for episodi in episodis_a_pujar:
        url = pujar_episodi(episodi, episodes_dir, dry_run=args.dry_run)
        
        if url:
            urls_generades[episodi['num']] = url
            
            if not args.no_update_md and not args.dry_run:
                actualitzar_markdown(episodi, url, episodes_md_dir)
    
    # Resum final
    print("\n" + "=" * 60)
    print("📊 RESUM")
    print("=" * 60)
    print(f"✅ Episodis processats: {len(urls_generades)}/{len(episodis_a_pujar)}")
    
    if urls_generades:
        print("\n📍 URLs generades:")
        for num, url in sorted(urls_generades.items()):
            print(f"   {num}: {url}")
    
    if not args.dry_run and urls_generades and not args.no_update_md:
        print("\n💡 Recorda fer:")
        print("   git add _episodes/")
        print("   git commit -m 'Migrar URLs a archive.org'")
        print("   git push")


if __name__ == '__main__':
    main()
