#!/usr/bin/env python3
"""
Script per pujar automàticament tots els episodis del podcast a archive.org
Requereix: pip install internetarchive
Configuració: ia configure (només primera vegada)
"""

import os
import sys
import time
from pathlib import Path

import requests
from internetarchive import upload, get_item

# Configuració del podcast
CREATOR = "Associació Veïnal de Can Gaietà"
COLLECTION = None  # No especificar col·lecció - es crearà al compte personal
LICENSE = "http://creativecommons.org/licenses/by/4.0/"
LANGUAGE = "cat"
WEBSITE = "https://cangaieta.cat"
PODCAST_URL = "https://cangaieta.github.io/podcast"

# --- Caràtules -------------------------------------------------------------
# Sufix del nom REMOT de la caràtula a archive.org.
#
# ⚠️ NO fer servir "<nom>.png" a seques: archive.org genera, a partir de l'MP3,
#    un derivat anomenat exactament així (és la forma d'ona). Veure la trampa 2
#    documentada a caratula_confirmada().
COVER_SUFFIX = "-cover.png"

METADATA_API = "https://archive.org/metadata/{}"

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
    },
    {
        "num": "021",
        "fitxer": "021-diners-brossa-pisos-tiana.mp3",
        "identifier": "podcast-cangaieta-021-diners-brossa-pisos-tiana",
        "title": "Episodi 021: Diners, brossa i pisos: qui paga el preu de les etiquetes?",
        "description": "Anàlisi del ple municipal del 7 de juliol de 2026 a Tiana, a pocs mesos de les eleccions, a partir de les etiquetes que posa el govern. La «prudència» d'injectar 1,78 milions de romanent de tresoreria, quan el 60% va a despesa corrent (hores extres de la policia, gasolina, neteja) i en surten 25.000 € per a comunicació i 90.000 € per a festes, tot sostingut pels ingressos del totxo; la «taxa justa» del macrocontracte de neteja i residus de 18,4 milions per a 10 anys, amb un porta a porta de cinc fraccions que no serà obligatori fins al 2028, després de les eleccions, mentre els veïns ja paguen una taxa un 140% més alta; i la «mutació demanial subjectiva» que cedeix gratuïtament a l'AMB, durant 50 anys, la parcel·la de Calçfrares per fer-hi 40 habitatges dotacionals sense un pla per al barri. La pregunta de fons: qui pagarà demà el preu de les etiquetes que els polítics pengen avui?",
        "date": "2026-10-19",
        "duration": "17:19",
        "tags": ["podcast", "tiana", "ajuntament", "can gaieta", "catalunya", "notebooklm", "ple municipal", "majoria absoluta", "romanent de tresoreria", "pressupost", "contracte de neteja", "recollida de residus", "porta a porta", "taxa de residus", "TERSA", "habitatge social", "AMB", "calcfrares", "mutacio demanial", "incendis forestals"]
    },
    {
        "num": "022",
        "fitxer": "022-aigua-publica-retallades-tiana.mp3",
        "identifier": "podcast-cangaieta-022-aigua-publica-retallades-tiana",
        "title": "Episodi 022: L'aigua cap a l'AMB i el milió que cal retallar",
        "description": "Anàlisi del ple ordinari del 8 de setembre de 2026 a Tiana, a les portes de les eleccions i amb un govern amb majoria absoluta. El compte general del 2025 es presenta amb 2,5 milions de superàvit, uns 9 milions de romanent i tres semàfors verds, però l'interventor recomana «revisar la pressió fiscal», el romanent paga fins a un milió de despesa corrent i l'alcalde admet que caldrà retallar gairebé un milió per culpa del contracte de neteja més car de la història. La mutació demanial cedeix totes les instal·lacions de l'aigua a l'AMB per una sentència del TSJC, mentre el PAM del govern dona per complerta al 100% la defensa de l'aigua pública. I la moció del transport públic destapa l'acusació de postureig. I just llavors rebenta una canonada a Can Matas. Si ho deleguem tot, triem gestors o un departament de relacions públiques?",
        "date": "2026-10-19",
        "duration": "23:36",
        "tags": ["podcast", "tiana", "ajuntament", "can gaieta", "catalunya", "notebooklm", "ple municipal", "majoria absoluta", "compte general", "romanent de tresoreria", "pressio fiscal", "retallades", "contracte de neteja", "aigua publica", "mutacio demanial", "AMB", "TSJC", "transport public", "la virreina", "can matas"]
    },
    {
        "num": "023",
        "fitxer": "023-aiguats-polemica-residus-tiana.mp3",
        "identifier": "podcast-cangaieta-023-aiguats-polemica-residus-tiana",
        "title": "Episodi 023: Aiguats, cinc fraccions i la lletra petita de Cals Frares",
        "description": "Anàlisi del ple ordinari del 6 d'octubre de 2026 a Tiana, suspès per una alerta vermella de Protecció Civil mentre queien 327 litres per metre quadrat. A dins, una altra tempesta: el contracte de residus i neteja de més de 18 milions per a 10 anys, amb vehicles elèctrics i més operaris, però lligat al porta a porta de cinc fraccions en un poble que ja recicla al voltant del 90%; el govern diu que l'oposició ja ho va aprovar a l'abril amb l'ordenança marc. Els 12.000 € per entrar a TERSA, sortits de la partida de neteja viària. I la mutació demanial de Cals Frares, on el conveni diu que el terreny revertirà a Tiana, sí, però després que l'AMB hagi amortitzat la inversió. El llenguatge tècnic s'ha convertit en l'eina per desactivar l'opinió ciutadana?",
        "date": "2026-10-20",
        "duration": "13:26",
        "tags": ["podcast", "tiana", "ajuntament", "can gaieta", "catalunya", "notebooklm", "ple municipal", "majoria absoluta", "aiguats", "gota freda", "proteccio civil", "contracte de residus", "neteja viaria", "porta a porta", "cinc fraccions", "FCC", "TERSA", "mutacio demanial", "cals frares", "AMB"]
    }
]


def ruta_caratula(episodi, project_dir):
    """Ruta local de la caràtula (el PNG gran, no la versió reduïda dels llistats)"""
    return project_dir / 'assets' / 'thumbnails' / episodi['fitxer'].replace('.mp3', '.png')


def ruta_caratula_petita(episodi, project_dir):
    """Ruta local de la versió reduïda que fan servir els llistats web"""
    nom = episodi['fitxer'].replace('.mp3', '.webp')
    return project_dir / 'assets' / 'thumbnails' / 'small' / nom


def assegurar_caratula(episodi, project_dir):
    """
    Comprova que la caràtula hi sigui ABANS de pujar res, i genera la versió
    reduïda per als llistats web si falta.

    Retorna (ok: bool, missatge: str). Si retorna False, no s'ha de pujar
    l'episodi: cal generar la caràtula primer.
    """
    cover = ruta_caratula(episodi, project_dir)

    if not cover.exists():
        return False, (
            f"No hi ha caràtula per a l'episodi {episodi['num']}.\n"
            f"      S'esperava: {cover}\n"
            f"\n"
            f"      Genera-la abans de pujar l'episodi:\n"
            f"        python scripts/generate_thumbnail.py \\\n"
            f"          --episodi {episodi['num']} \\\n"
            f"          --nom {episodi['fitxer'].replace('.mp3', '')} \\\n"
            f"          --prompt-suffix \"element visual del tema, en anglès\"\n"
            f"\n"
            f"      (si tens un motiu per publicar sense caràtula: --permet-sense-caratula)"
        )

    # Versió reduïda per als llistats: si falta, la generem aquí mateix
    petita = ruta_caratula_petita(episodi, project_dir)
    if petita.exists():
        return True, f"{cover.name} + {petita.name} (ja hi era)"

    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from generate_thumbnails_small import genera
    except ImportError as e:
        return False, f"no s'ha pogut carregar generate_thumbnails_small.py: {e}"

    resultat = genera(cover, petita)
    if resultat.startswith('error'):
        return False, f"no s'ha pogut generar la versió reduïda: {resultat}"

    return True, (f"{cover.name} + {petita.name} "
                  f"(reduïda generada ara, {petita.stat().st_size / 1024:.0f} KB)")


def nom_remot_caratula(episodi):
    """Nom amb què es desa la caràtula a archive.org"""
    return episodi['fitxer'].replace('.mp3', COVER_SUFFIX)


def obtenir_metadades(identifier, intents=5):
    """Consulta l'API de metadades d'archive.org, amb reintents."""
    ultim_error = None
    for intent in range(1, intents + 1):
        try:
            r = requests.get(METADATA_API.format(identifier), timeout=30)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            ultim_error = e
            if intent < intents:
                time.sleep(min(30, 2 ** intent))
    raise RuntimeError(f"No s'han pogut llegir les metadades de {identifier}: {ultim_error}")


def caratula_confirmada(identifier, cover_name, mida_local, metadades=None):
    """
    Comprova de debò si la caràtula hi és. Retorna (bool, motiu).

    ⚠️ TRAMPA 2 - COL·LISIÓ DE NOMS (fals positiu)
    archive.org genera, a partir de l'MP3, un derivat anomenat sovint exactament
    igual que la nostra imatge (<nom>.png): és la forma d'ona, d'uns 45 KB.
    Si només comproves que el fitxer existeix (un HEAD, o que surti al llistat de
    fitxers) tindràs un 200 per a TOTS els episodis i te'ls saltaràs tots
    pensant que ja tenen caràtula.

    La comprovació correcta exigeix les dues coses:
      - source == "original"  (no "derivative": això descarta la forma d'ona)
      - size == mida del fitxer local (això descarta una pujada truncada)
    """
    d = metadades if metadades is not None else obtenir_metadades(identifier)

    for f in d.get('files', []):
        if f.get('name') != cover_name:
            continue

        if f.get('source') != 'original':
            return False, (f"hi ha un '{cover_name}' però és source={f.get('source')} "
                           f"— és un derivat d'archive.org, no la nostra caràtula")

        try:
            mida_remota = int(f.get('size', -1))
        except (TypeError, ValueError):
            mida_remota = -1

        if mida_remota != mida_local:
            return False, (f"la mida no coincideix (remot {mida_remota} B, "
                           f"local {mida_local} B) — pujada incompleta")

        return True, f"source=original, {mida_remota} B"

    return False, "no hi és"


def esperes_creixents(timeout, inicial=15, maxim=240):
    """Genera esperes que es dupliquen: 15, 30, 60, 120, 240, 240… segons.

    S'atura quan la suma passaria de `timeout`. Sondejar archive.org a interval
    fix i curt durant minuts sembla un atac; amb esperes creixents els casos
    ràpids es resolen de seguida i els lents fan quatre peticions comptades.
    """
    espera, total = inicial, 0
    while total + espera <= timeout:
        yield espera
        total += espera
        espera = min(espera * 2, maxim)


def _format_espera(segons):
    return f"{segons}s" if segons < 60 else f"{segons // 60} min"


def esperar_caratula(identifier, cover_name, mida_local, timeout=480):
    """
    Sondeja fins que la caràtula surt a l'API de metadades. Retorna (bool, motiu).

    Just després de pujar, l'API triga una estona a llistar els fitxers: una
    comprovació massa d'hora dona fals negatiu (al Podcast del Doctor, el
    2026-09-20, als 30 s encara no hi eren). Amb timeout=480 fa cinc
    comprovacions: als 15 s, 45 s, 1:45, 3:45 i 7:45.
    """
    motiu = "encara no hi és"
    for espera in esperes_creixents(timeout):
        print(f"   ⏳ esperant {_format_espera(espera)} abans de comprovar…")
        time.sleep(espera)
        ok, motiu = caratula_confirmada(identifier, cover_name, mida_local)
        if ok:
            return True, motiu
    return False, motiu


def esperar_derive(identifier, timeout=1200, verbose=True):
    """
    Espera que l'ítem no tingui tasques pendents. Retorna True si està lliure.

    ⚠️ TRAMPA 1 - UN 200 NO VOL DIR QUE EL FITXER HI HAGI ARRIBAT
    Si l'ítem té un derive en curs, upload() retorna 200 i archive.org descarta
    el fitxer EN SILENCI. No hi ha cap error: simplement, després, el fitxer no
    hi és. Per això cal esperar que pending_tasks sigui fals ABANS de pujar,
    i verificar DESPRÉS de pujar.
    """
    esperes = esperes_creixents(timeout)
    while True:
        d = obtenir_metadades(identifier)
        if not d.get('pending_tasks'):
            return True

        espera = next(esperes, None)
        if espera is None:
            return False
        if verbose:
            print(f"   ⏳ derive en curs a archive.org, esperant {_format_espera(espera)}…")
        time.sleep(espera)


def pujar_caratula(episodi, project_dir, dry_run=False, force=False, intents=3):
    """
    Puja la caràtula a un ítem ja existent i verifica que hi hagi arribat.

    Retorna un dels estats: 'ja-hi-era', 'pujada', 'saltat', o 'error: <motiu>'.
    És idempotent: si la caràtula ja hi és (de debò), no fa res.
    """
    identifier = episodi['identifier']
    cover_local = ruta_caratula(episodi, project_dir)
    cover_name = nom_remot_caratula(episodi)

    if not cover_local.exists():
        return f"error: no existeix la caràtula local {cover_local}"

    mida_local = cover_local.stat().st_size

    print(f"\n🖼️  Episodi {episodi['num']} — {identifier}")
    print(f"   Caràtula local: {cover_local.name} ({mida_local / 1024:.0f} KB)")
    print(f"   Nom remot:      {cover_name}")

    try:
        metadades = obtenir_metadades(identifier)
    except RuntimeError as e:
        return f"error: {e}"

    if not metadades.get('files'):
        return "error: l'ítem no existeix a archive.org (puja primer l'MP3)"

    # Idempotència: si ja hi és de debò, saltem
    ja_hi_es, motiu = caratula_confirmada(identifier, cover_name, mida_local, metadades)
    if ja_hi_es and not force:
        print(f"   ⏭️  Ja té caràtula ({motiu}) — saltat")
        return 'ja-hi-era'

    if dry_run:
        print(f"   🔍 DRY-RUN: es pujaria ({motiu})")
        return 'saltat'

    for intent in range(1, intents + 1):
        if intent > 1:
            print(f"   🔁 Reintent {intent}/{intents}")

        # TRAMPA 1: no pugem mai amb un derive en curs
        if not esperar_derive(identifier):
            print("   ⚠️  El derive no ha acabat dins el temps d'espera")
            continue

        try:
            r = upload(
                identifier,
                files={cover_name: str(cover_local)},
                retries=3,
                verbose=False,
                queue_derive=True,   # cal per regenerar __ia_thumb.jpg
            )
            codi = r[0].status_code if r else None
            print(f"   ⬆️  upload() ha retornat {codi} (no és garantia de res)")
        except Exception as e:
            print(f"   ❌ Error pujant: {e}")
            time.sleep(15)
            continue

        # TRAMPA 1+2: verificació real contra l'API de metadades
        ok, motiu = esperar_caratula(identifier, cover_name, mida_local)
        if ok:
            print(f"   ✅ Verificat a l'API de metadades ({motiu})")
            return 'pujada'

        print(f"   ⚠️  Després de pujar, la verificació falla: {motiu}")

    return f"error: no s'ha pogut confirmar la caràtula després de {intents} intents"


def pujar_mp3(episodi, episodes_dir, project_dir, dry_run=False, intents=4, espera=1800):
    """
    Substitueix l'MP3 d'un ítem ja publicat (mateix nom, la URL no canvia) i
    verifica que hi hagi arribat. Si hi ha caràtula local, va a la mateixa
    crida (un sol derive) i també es verifica.

    Serveix per afegir els jingles retroactivament. Retorna True si tot hi és.
    archive.org processa l'MP3 abans de llistar-lo i triga més de 8 min: al
    Podcast del Doctor, amb l'espera de les caràtules (480 s), es donava per
    perdut i es tornava a pujar sencer. Per això aquí 30 min.
    """
    identifier = episodi['identifier']
    mp3 = episodes_dir / episodi['fitxer']
    print(f"\n🎵 MP3 episodi {episodi['num']} — {identifier}")
    if not mp3.exists():
        print(f"   ❌ No s'ha trobat {mp3}")
        return False

    fitxers = {episodi['fitxer']: mp3}
    cover = ruta_caratula(episodi, project_dir)
    if cover.exists():
        fitxers[nom_remot_caratula(episodi)] = cover

    try:
        metadades = obtenir_metadades(identifier)
    except RuntimeError as e:
        print(f"   ❌ {e}")
        return False
    if not metadades.get('files'):
        print("   ❌ L'ítem no existeix a archive.org (puja primer l'episodi)")
        return False

    pendents = {}
    for nom, local in fitxers.items():
        ok, motiu = caratula_confirmada(identifier, nom, local.stat().st_size, metadades)
        if ok:
            print(f"   ⏭️  {nom} ja hi és ({motiu})")
        else:
            pendents[nom] = local
    if not pendents or dry_run:
        if pendents:
            print(f"   🔍 DRY-RUN: es pujaria {', '.join(pendents)}")
        return True

    for intent in range(1, intents + 1):
        print(f"   🔄 Intent {intent}/{intents}: {', '.join(pendents)}")

        # TRAMPA 1: no pugem mai amb un derive en curs
        if not esperar_derive(identifier, timeout=espera):
            print("   ⚠️  El derive no ha acabat dins el temps d'espera")
            continue

        try:
            r = upload(identifier, files={n: str(f) for n, f in pendents.items()},
                       verbose=False, queue_derive=True, retries=3)
            codi = r[0].status_code if r else None
            print(f"   ⬆️  upload() ha retornat {codi} (no és garantia de res)")
        except Exception as e:
            print(f"   ❌ Error pujant: {e}")
            time.sleep(15)
            continue

        # Les esperes comencen quan acaba la pujada: el primer fitxer fa
        # l'espera llarga i els altres normalment ja hi són.
        for nom in list(pendents):
            ok, motiu = esperar_caratula(identifier, nom, pendents[nom].stat().st_size, timeout=espera)
            if ok:
                print(f"   ✅ {nom} verificat ({motiu})")
                del pendents[nom]
            else:
                print(f"   ⚠️  {nom} no confirmat: {motiu}")
        if not pendents:
            return True

    return False


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


def pujar_episodi(episodi, episodes_dir, dry_run=False, permet_sense_caratula=False):
    """
    Puja un episodi (MP3 + caràtula) a archive.org.

    Si no hi ha caràtula local s'atura i no puja res, tret que
    permet_sense_caratula sigui True. Si falta la versió reduïda per als
    llistats web, la genera automàticament.
    """
    
    fitxer_path = episodes_dir / episodi['fitxer']
    
    if not fitxer_path.exists():
        print(f"❌ ERROR: No s'ha trobat el fitxer {fitxer_path}")
        return None
    
    identifier = episodi['identifier']
    metadata = crear_metadata(episodi)
    project_dir = episodes_dir.parent
    cover_local = ruta_caratula(episodi, project_dir)

    print(f"\n📦 Pujant episodi {episodi['num']}: {episodi['title']}")
    print(f"   Fitxer: {fitxer_path}")
    print(f"   Identifier: {identifier}")

    # ── Comprovació prèvia: sense caràtula no es puja res ──────────────────
    ok_cover, missatge = assegurar_caratula(episodi, project_dir)
    if ok_cover:
        print(f"   Caràtula: {missatge}")
    elif permet_sense_caratula:
        print(f"   ⚠️  {missatge.splitlines()[0]}")
        print("   ⚠️  --permet-sense-caratula: es puja només l'MP3")
    else:
        print(f"   ❌ ATURAT: {missatge}")
        return None

    # La caràtula va al MATEIX upload() que l'MP3: en un ítem nou encara no hi ha
    # cap derive en curs, així que tots dos fitxers hi arriben segurs (trampa 1).
    fitxers = {episodi['fitxer']: str(fitxer_path)}
    if ok_cover:
        fitxers[nom_remot_caratula(episodi)] = str(cover_local)
        print(f"   Nom remot: {nom_remot_caratula(episodi)}")

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
        
        # Pujar els fitxers (MP3 + caràtula)
        r = upload(
            identifier,
            files=fitxers,
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

            # ⚠️ TRAMPA 1: un 200 no és garantia que el fitxer hi hagi arribat.
            #    Verifiquem la caràtula contra l'API de metadades, amb reintents
            #    (la caràtula pot trigar uns segons a aparèixer-hi).
            if ok_cover:
                mida_local = cover_local.stat().st_size
                cover_name = nom_remot_caratula(episodi)
                confirmada, motiu = esperar_caratula(identifier, cover_name, mida_local)

                if confirmada:
                    print(f"   ✅ Caràtula verificada ({motiu})")
                else:
                    print(f"   ⚠️  Caràtula NO confirmada: {motiu}")
                    print(f"      L'MP3 sí que ha pujat. Arregla la caràtula amb:")
                    print(f"        python scripts/upload_to_archive.py "
                          f"--nomes-cover --episodi {episodi['num']}")

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

    # Sortida línia a línia encara que vagi a un fitxer o a una canonada:
    # si no, el progrés de les esperes no es veu fins que l'script acaba.
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except AttributeError:
        pass
    
    parser = argparse.ArgumentParser(description='Puja episodis a archive.org')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Mostra què es faria sense pujar res')
    parser.add_argument('--episodi', type=str,
                       help='Pujar només un episodi específic (ex: 001)')
    parser.add_argument('--no-update-md', action='store_true',
                       help='No actualitzar els fitxers markdown')
    parser.add_argument('--nomes-cover', action='store_true',
                       help='Només pujar la caràtula a ítems JA publicats, sense '
                            'tornar a pujar l\'àudio. Idempotent: salta els que ja en tenen.')
    parser.add_argument('--force-cover', action='store_true',
                       help='Amb --nomes-cover, torna a pujar la caràtula encara que ja hi sigui')
    parser.add_argument('--nomes-mp3', action='store_true',
                       help='Substituir l\'MP3 (i la caràtula, a la mateixa crida) d\'ítems JA '
                            'publicats (ex: jingles retroactius). No pregunta: verifica que hi arriben')
    parser.add_argument('--permet-sense-caratula', action='store_true',
                       help='Permet pujar un episodi sense caràtula. Per defecte, si no '
                            'hi ha caràtula local l\'script s\'atura i no puja res.')

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

    if args.nomes_mp3:
        print("🎵 MODE NOMÉS MP3 - substitueix l'àudio d'ítems ja publicats")
        fallats = [e['num'] for e in episodis_a_pujar
                   if not pujar_mp3(e, episodes_dir, project_dir, dry_run=args.dry_run)]
        print(f"\n✅ MP3 confirmats: {len(episodis_a_pujar) - len(fallats)}/{len(episodis_a_pujar)}")
        if fallats:
            print(f"❌ No confirmats: {', '.join(fallats)}")
        sys.exit(1 if fallats else 0)

    # ------------------------------------------------------------------
    # Mode "només caràtula": per a ítems ja publicats
    # ------------------------------------------------------------------
    if args.nomes_cover:
        print("🖼️  MODE NOMÉS CARÀTULA - no es torna a pujar cap àudio")
        resultats = {}
        for episodi in episodis_a_pujar:
            resultats[episodi['num']] = pujar_caratula(
                episodi, project_dir, dry_run=args.dry_run, force=args.force_cover)

        print("\n" + "=" * 60)
        print("📊 RESUM CARÀTULES")
        print("=" * 60)
        pujades = [n for n, r in resultats.items() if r == 'pujada']
        ja_hi_eren = [n for n, r in resultats.items() if r == 'ja-hi-era']
        errors = {n: r for n, r in resultats.items() if r.startswith('error')}

        print(f"✅ Pujades i verificades: {len(pujades)}   "
              f"⏭️  Ja en tenien: {len(ja_hi_eren)}   ❌ Errors: {len(errors)}")
        if pujades:
            print(f"   Pujades: {', '.join(sorted(pujades))}")
        if ja_hi_eren:
            print(f"   Ja hi eren: {', '.join(sorted(ja_hi_eren))}")
        for num, motiu in sorted(errors.items()):
            print(f"   ❌ {num}: {motiu}")

        print("\n💡 archive.org ha de refer el derive per regenerar __ia_thumb.jpg.")
        print("   Als llistats la caràtula pot trigar a aparèixer; això NO vol dir")
        print("   que hagi fallat. Comprova-ho amb:")
        print("   curl -sIL https://archive.org/services/img/<identifier>")
        print("   (forma d'ona = 180x45 gris; caràtula = 180x180 en color)")

        sys.exit(1 if errors else 0)

    # Processar cada episodi
    urls_generades = {}
    aturats_sense_caratula = []
    for episodi in episodis_a_pujar:
        url = pujar_episodi(episodi, episodes_dir, dry_run=args.dry_run,
                            permet_sense_caratula=args.permet_sense_caratula)

        if url is None and not ruta_caratula(episodi, project_dir).exists():
            aturats_sense_caratula.append(episodi['num'])

        if url:
            urls_generades[episodi['num']] = url
            
            if not args.no_update_md and not args.dry_run:
                actualitzar_markdown(episodi, url, episodes_md_dir)
    
    # Resum final
    print("\n" + "=" * 60)
    print("📊 RESUM")
    print("=" * 60)
    print(f"✅ Episodis processats: {len(urls_generades)}/{len(episodis_a_pujar)}")

    if aturats_sense_caratula:
        print(f"\n❌ ATURATS per falta de caràtula: {', '.join(aturats_sense_caratula)}")
        print("   No s'ha pujat res d'aquests episodis. Genera'ls la caràtula amb")
        print("   scripts/generate_thumbnail.py i torna a executar aquesta comanda.")

    if urls_generades:
        print("\n📍 URLs generades:")
        for num, url in sorted(urls_generades.items()):
            print(f"   {num}: {url}")
    
    if not args.dry_run and urls_generades and not args.no_update_md:
        print("\n💡 Recorda fer:")
        print("   git add _episodes/ assets/thumbnails/")
        print("   git commit -m 'Migrar URLs a archive.org'")
        print("   git push")

    sys.exit(1 if aturats_sense_caratula else 0)


if __name__ == '__main__':
    main()
