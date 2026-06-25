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
    },
    {
        "num": "014",
        "fitxer": "014-multes-750-euros-busos-inutils.mp3",
        "identifier": "podcast-cangaieta-014-multes-750-euros-busos-inutils",
        "title": "Episodi 014: Multes de 750 € i autobusos que no caben pel poble",
        "description": "Anàlisi de la tertúlia política d'abril de 'Ara i aquí' (La Local Ràdio Tiana) sobre la nova ordenança de residus i neteja viària de Tiana, aprovada inicialment el 21 d'abril de 2026. Multes de 750 a 3.000 euros que ningú podrà aplicar perquè no hi ha policia, una 'taxa justa' que duplica el rebut (de 180 a 330 €) per culpa d'un contracte caducat, ecocàmeres com a solucionisme tecnològic d'aparador i una línia d'autobús B32 que el primer dia rascava els baixos contra l'asfalt al Camí dels Francesos. La cadira buida del govern al debat ho diu tot.",
        "date": "2026-05-03",
        "duration": "15:23",
        "tags": ["podcast", "tiana", "ajuntament", "can gaieta", "catalunya", "notebooklm", "ordenança residus", "neteja viaria", "multes", "taxa justa", "ecocàmeres", "autobus", "b32", "mobilitat", "tertulia politica", "la local radio tiana", "majoria absoluta"]
    },
    {
        "num": "015",
        "fitxer": "015-b32-cap-fantasma.mp3",
        "identifier": "podcast-cangaieta-015-b32-cap-fantasma",
        "title": "Episodi 015: La línia B32 i el CAP fantasma",
        "description": "Anàlisi de la tertúlia política de La Local Ràdio Tiana sobre la nova línia d'autobús B32, fruit de la fusió de la B34 i la B35. El govern justifica el traçat dient que passa pel futur CAP, un edifici que ni tan sols està en obres i que pot trigar fins a 15 anys a ser una realitat. L'oposició s'assabenta del canvi el mateix divendres de l'anunci, no es coneixen les dades més bàsiques (a quina hora surt el primer bus?), els barris històrics queden aïllats, i el bus directe a Barcelona només el feien servir 35 persones a la setmana.",
        "date": "2026-05-03",
        "duration": "13:40",
        "tags": ["podcast", "tiana", "ajuntament", "can gaieta", "catalunya", "notebooklm", "autobus", "b32", "b34", "b35", "mobilitat", "amb", "cap", "centre atencio primaria", "tertulia politica", "la local radio tiana", "majoria absoluta", "competencies", "participacio ciutadana"]
    },
    {
        "num": "016",
        "fitxer": "016-informe-antifrau-contractes-verbals.mp3",
        "identifier": "podcast-cangaieta-016-informe-antifrau-contractes-verbals",
        "title": "Episodi 016: L'informe d'Antifrau i els contractes verbals",
        "description": "Anàlisi del ple municipal de Tiana del 23 d'abril de 2026 sobre l'informe de l'Oficina Antifrau de Catalunya i la pràctica dels contractes verbals a l'Ajuntament. Episodi pendent de personalització.",
        "date": "2026-05-03",
        "duration": "20:08",
        "tags": ["podcast", "tiana", "ajuntament", "can gaieta", "catalunya", "notebooklm", "antifrau", "contractes verbals", "ple municipal", "transparencia", "fiscalitzacio"]
    },
    {
        "num": "017",
        "fitxer": "017-plaques-solars-multes-ia.mp3",
        "identifier": "podcast-cangaieta-017-plaques-solars-multes-ia",
        "title": "Episodi 017: Plaques solars ruïnoses i multes amb IA",
        "description": "Anàlisi del ple municipal extraordinari del 21 d'abril de 2026 a Tiana, on s'aprova una Comunitat Energètica Solar deficitària (372.000 € d'inversió per amortitzar en 30 anys amb plaques que duren 15) i una nova ordenança de residus amb multes de fins a 3.000 € reforçada per ecocàmeres amb intel·ligència artificial. El radi de 5 km del decret estatal es ven com a victòria local, els blocs de pisos prioritzats deixen el barri de la Virreina sense accés real, l'oposició parla de malbaratament i populisme, i el doble discurs «no tenim afany recaptatori» xoca amb un sistema de vigilància algorítmica per a la brossa.",
        "date": "2026-05-03",
        "duration": "15:52",
        "tags": ["podcast", "tiana", "ajuntament", "can gaieta", "catalunya", "notebooklm", "plaques solars", "comunitat energetica", "energia renovable", "ordenança residus", "ecocàmeres", "intel·ligencia artificial", "vigilancia", "multes", "ple extraordinari", "majoria absoluta", "virreina"]
    },
    {
        "num": "018",
        "fitxer": "018-arbrat-escocells-trenta-graus.mp3",
        "identifier": "podcast-cangaieta-018-arbrat-escocells-trenta-graus",
        "title": "Episodi 018: Trenta graus de diferència per un arbre",
        "description": "Dossier sobre la gestió de l'arbrat urbà a Tiana. El 2 de juliol de 2025 un veí va sortir al carrer amb una càmera tèrmica FLIR: l'asfalt del carrer de Cals Frares marcava 57,2 °C i, a quatre carrers, sota els arbres de Can Mates, 26,8 °C. A partir d'aquesta evidència, l'episodi creua les mesures veïnals amb l'inventari oficial d'arbrat 2024 (4.726 arbres vius i 541 baixes, un 10% del cens, amb 56 escocells pavimentats), la confessió del propi consultor que la causa principal d'alteració són les podes agressives i els escocells insuficients, el plàtan al 24% que l'inventari recomana no plantar més, el patró opac de les tales (Alt d'Alella, el garrofer centenari desaparegut sense rastre), els refugis climàtics que no refresquen i el Reglament UE 2024/1991 que converteix les 541 baixes en un deute forestal davant Europa.",
        "date": "2026-05-23",
        "duration": "16:21",
        "tags": ["podcast", "tiana", "ajuntament", "can gaieta", "catalunya", "notebooklm", "arbrat", "arbres", "escocells", "verd urba", "poda", "inventari arbrat", "camera termica", "flir", "refugis climatics", "canvi climatic", "patrimoni", "reglament UE 2024/1991"]
    },
    {
        "num": "019",
        "fitxer": "019-dopatge-financer-fira-atraccions.mp3",
        "identifier": "podcast-cangaieta-019-dopatge-financer-fira-atraccions",
        "title": "Episodi 019: Dopatge financer i la fira d'atraccions desterrada",
        "description": "Anàlisi del ple municipal ordinari del 5 de maig de 2026 a Tiana, llegit des de la lletra petita: com un govern amb majoria absoluta controla el relat institucional. Actes que donen tres respostes diferents a una mateixa pregunta sobre el bar del Casal; la modificació de plantilla (eliminar set places C2 i crear-ne quatre de C1) que el regidor Albert Sales qualifica de «dopatge financer» perquè es paga amb romanent de tresoreria; la «discreció» sobre la residència de Sant Cebrià; una moció d'educació que és un còpia i enganxa d'un text autonòmic; i la moció d'ERC per tornar la fira d'atraccions al centre, rebutjada amb excuses canviants (seguretat, urbanisme, culpa dels firaires) mentre els macroconcerts —el veritable focus d'inseguretat— continuen. Tot rematat pel contrast entre l'advertència tova al bar del Casal i el ROM utilitzat com a arma contra el regidor en el «miracle dels escosells».",
        "date": "2026-06-24",
        "duration": "14:40",
        "tags": ["podcast", "tiana", "ajuntament", "can gaieta", "catalunya", "notebooklm", "ple municipal", "majoria absoluta", "dopatge financer", "plantilla", "romanent de tresoreria", "residencia sant cebria", "fira atraccions", "macroconcerts", "moció educació", "bar del casal", "escocells", "rom", "actes", "transparencia"]
    },
    {
        "num": "020",
        "fitxer": "020-tiana-aillada-escola-bressol.mp3",
        "identifier": "podcast-cangaieta-020-tiana-aillada-escola-bressol",
        "title": "Episodi 020: Tiana aïllada i sense escola bressol",
        "description": "Anàlisi del ple municipal del 2 de juny de 2026 a Tiana, en plena precampanya, llegit des de la lletra petita. El fil conductor: un govern amb majoria absoluta que, davant de cada gran crisi, assenyala un tercer actor. El «xec en blanc» del camí dels frares, on l'Ajuntament cedeix el control del pla urbanístic a l'AMB i es compromet a pagar tota la urbanització sense estudi econòmic, mentre l'informe del secretari adverteix que la reserva de pisos per a gent de Tiana no consta al conveni; la moció d'ERC d'auditoria externa esquivada amb l'excusa de la «viabilitat tècnica» quan el pressupost ha pujat 3 milions des del 2022 a base de romanent; els 47 nadons sense plaça d'escola bressol amb la regidora carregant la culpa a la Generalitat i oferint xecs per a la privada; la nova línia B32 que deixa barris sencers incomunicats; i, als precs i preguntes, el requeriment sense sanció al Casal i els 27.000 € del mur de les monges maquillats com un «esforç compartit». La pregunta de fons: si tot depèn d'un altre, quina és la sobirania real d'aquest Ajuntament?",
        "date": "2026-06-25",
        "duration": "19:58",
        "tags": ["podcast", "tiana", "ajuntament", "can gaieta", "catalunya", "notebooklm", "ple municipal", "majoria absoluta", "escola bressol", "habitatge social", "AMB", "cami dels frares", "auditoria externa", "romanent de tresoreria", "linia b32", "transport public", "mobilitat", "mur de les monges", "precs i preguntes", "sobirania municipal"]
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
