import random
import re
import unicodedata

def obtener_bandera(pais):
    """Devuelve el emoji de la bandera para un país dado."""
    if not pais: return ""
    
    p = pais.lower().strip()
    mapping = {
        "argentina": "🇦🇷", "arg": "🇦🇷",
        "spain": "🇪🇸", "españa": "🇪🇸", "esp": "🇪🇸",
        "usa": "🇺🇸", "united states": "🇺🇸", "estados unidos": "🇺🇸",
        "italy": "🇮🇹", "italia": "🇮🇹", "ita": "🇮🇹",
        "france": "🇫🇷", "francia": "🇫🇷", "fra": "🇫🇷",
        "germany": "🇩🇪", "alemania": "🇩🇪", "ger": "🇩🇪",
        "brazil": "🇧🇷", "brasil": "🇧🇷", "bra": "🇧🇷",
        "chile": "🇨🇱", "chi": "🇨🇱",
        "uruguay": "🇺🇾", "uru": "🇺🇾",
        "colombia": "🇨🇴", "col": "🇨🇴",
        "peru": "🇵🇪", "per": "🇵🇪",
        "ecuador": "🇪🇨", "ecu": "🇪🇨",
        "mexico": "🇲🇽", "mex": "🇲🇽",
        "great britain": "🇬🇧", "united kingdom": "🇬🇧", "gbr": "🇬🇧", "reino unido": "🇬🇧",
        "australia": "🇦🇺", "aus": "🇦🇺",
        "serbia": "🇷🇸", "srb": "🇷🇸",
        "croatia": "🇭🇷", "cro": "🇭🇷",
        "russia": "🇷🇺", "rus": "🇷🇺",
        "greece": "🇬🇷", "gre": "🇬🇷",
        "poland": "🇵🇱", "pol": "🇵🇱",
        "kazakhstan": "🇰🇿", "kaz": "🇰🇿",
        "canada": "🇨🇦", "can": "🇨🇦",
        "japan": "🇯🇵", "jpn": "🇯🇵",
        "china": "🇨🇳", "chn": "🇨🇳",
        "czech republic": "🇨🇿", "czechia": "🇨🇿", "cze": "🇨🇿",
        "switzerland": "🇨🇭", "sui": "🇨🇭",
        "austria": "🇦🇹", "aut": "🇦🇹",
        "belgium": "🇧🇪", "bel": "🇧🇪",
        "netherlands": "🇳🇱", "ned": "🇳🇱",
        "norway": "🇳🇴", "nor": "🇳🇴",
        "denmark": "🇩🇰", "den": "🇩🇰",
        "bulgaria": "🇧🇬", "bul": "🇧🇬",
        "hungary": "🇭🇺", "hun": "🇭🇺",
        "portugal": "🇵🇹", "por": "🇵🇹",
        "ukraine": "🇺🇦", "ukr": "🇺🇦",
        "belarus": "🇧🇾", "blr": "🇧🇾",
        "slovakia": "🇸🇰", "svk": "🇸🇰",
        "slovenia": "🇸🇮", "slo": "🇸🇮",
        "sweden": "🇸🇪", "swe": "🇸🇪",
        "romania": "🇷🇴", "rou": "🇷🇴",
        "bolivia": "🇧🇴", "bol": "🇧🇴",
        "paraguay": "🇵🇾", "par": "🇵🇾",
        "venezuela": "🇻🇪", "ven": "🇻🇪",
        "finland": "🇫🇮", "fin": "🇫🇮",
        "south africa": "🇿🇦", "rsa": "🇿🇦",
        "neutral": "🏳️", "ana": "🏳️", "itf": "🏳️"
    }
    return mapping.get(p, "")


def es_derbi_argentino(pais1, pais2):
    """Devuelve True si ambos países son Argentina (duelo argentino)."""
    p1 = (pais1 or '').lower().strip()
    p2 = (pais2 or '').lower().strip()
    return p1 in ("argentina", "arg") and p2 in ("argentina", "arg")


# ==============================================================================
# BASE DE DATOS Y VARIANTES DE JUGADORES ARGENTINOS
# ==============================================================================
# Nombres limpios, apodos para festejos y usuarios de Twitter (separados para no
# insertar @handles como sujetos gramaticales en las oraciones).

JUGADORES_ARG = {
    "francisco cerundolo": {
        "nombres": ["Fran Cerúndolo", "Francisco Cerúndolo"],
        "apodo": "Fran",
        "twitter": "@FranCerundolo"
    },
    "sebastian baez": {
        "nombres": ["Seba Báez", "Sebastián Báez"],
        "apodo": "Seba",
        "twitter": "@sebaabaez7"
    },
    "tomas martin etcheverry": {
        "nombres": ["Tomi Etcheverry", "Tomás Etcheverry"],
        "apodo": "El Retu",
        "twitter": "@tometcheverry"
    },
    "mariano navone": {
        "nombres": ["Mariano Navone"],
        "apodo": "La Navoneta",
        "twitter": "@marianonavone1"
    },
    "facundo diaz acosta": {
        "nombres": ["Facu Díaz Acosta", "Facundo Díaz Acosta"],
        "apodo": "Facu",
        "twitter": "@facudiazacosta"
    },
    "camilo ugo carabelli": {
        "nombres": ["Camilo Ugo Carabelli", "Camilo Carabelli"],
        "apodo": "El Brujo",
        "twitter": "@camilougo"
    },
    "federico coria": {
        "nombres": ["Fede Coria", "Federico Coria"],
        "apodo": "La Mojarra",
        "twitter": "@fedeecoria"
    },
    "facundo bagnis": {
        "nombres": ["Facu Bagnis", "Facundo Bagnis"],
        "apodo": "Facu",
        "twitter": "@facubagnis"
    },
    "thiago agustin tirante": {
        "nombres": ["Thiago Tirante"],
        "apodo": "Thiago",
        "twitter": "@TiranteThiago"
    },
    "juan manuel cerundolo": {
        "nombres": ["Juanma Cerúndolo", "Juan Manuel Cerúndolo"],
        "apodo": "Juanma",
        "twitter": "@jmcerundolo"
    },
    "francisco comesana": {
        "nombres": ["Fran Comesaña", "Francisco Comesaña"],
        "apodo": "Fran",
        "twitter": "@fran_comesana"
    },
    "nadia podoroska": {
        "nombres": ["Nadia Podoroska"],
        "apodo": "La Rusa",
        "twitter": "@nadiapodoroska"
    },
    "lourdes carle": {
        "nombres": ["Lourdes Carlé"],
        "apodo": "Lourdes",
        "twitter": "@LourdesCarle"
    },
    "julia riera": {
        "nombres": ["Juli Riera", "Julia Riera"],
        "apodo": "Juli",
        "twitter": "@juliriera02"
    },
    "solana sierra": {
        "nombres": ["Solana Sierra", "Soli Sierra"],
        "apodo": "Soli",
        "twitter": "@solanasierra"
    },
    "federico gomez": {
        "nombres": ["Fede Gómez", "Federico Gómez"],
        "apodo": "Fede",
        "twitter": "@fedegomez96"
    },
    "juan pablo ficovich": {
        "nombres": ["Juampi Ficovich", "Juan Pablo Ficovich"],
        "apodo": "Juampi",
        "twitter": "@juampificovich"
    },
    "lautaro midon": {
        "nombres": ["Lautaro Midón", "Lauti Midón"],
        "apodo": "Lauti",
        "twitter": "@Lautaromidonn"
    },
    "genaro alberto olivieri": {
        "nombres": ["Genaro Olivieri", "Gena Olivieri"],
        "apodo": "Gena",
        "twitter": "@GenaOlivieri4"
    },
    "juan bautista torres": {
        "nombres": ["Bauti Torres", "Juan Bautista Torres"],
        "apodo": "Bauti",
        "twitter": "@_BautiTorres"
    },
    "juan manuel la serna": {
        "nombres": ["Manu La Serna", "Manuel La Serna"],
        "apodo": "Manu",
        "twitter": "@manulaserna3"
    },
    "benjamin chelia": {
        "nombres": ["Benja Chelia", "Benjamín Chelia"],
        "apodo": "Benja",
        "twitter": "@benja_chelia"
    },
    "facundo mena": {
        "nombres": ["Facu Mena", "Facundo Mena"],
        "apodo": "Facu",
        "twitter": "@menafacundo"
    },
    "santiago rodriguez taverna": {
        "nombres": ["Santi Rodríguez Taverna", "Santi Taverna"],
        "apodo": "El Duke",
        "twitter": "@santyelduke"
    },
    "gonzalo villanueva": {
        "nombres": ["Gonza Villanueva", "Gonzalo Villanueva"],
        "apodo": "Gonza",
        "twitter": "@gon_villanueva"
    },
    "luciano emanuel ambrogi": {
        "nombres": ["Lucho Ambrogi", "Luciano Ambrogi"],
        "apodo": "Lucho",
        "twitter": "@ambrogi_lucho"
    },
    "roman andres burruchaga": {
        "nombres": ["Román Burruchaga"],
        "apodo": "Burru",
        "twitter": "@r_burruchaga"
    },
    "marco trungelliti": {
        "nombres": ["Marco Trungelliti"],
        "apodo": "Trunge",
        "twitter": "@marcotrunge"
    },
    "mariano kestelboim": {
        "nombres": ["Mariano Kestelboim"],
        "apodo": "Kestelboim",
        "twitter": "@mkestelboim"
    },
    "jazmin ortenzi": {
        "nombres": ["Jazmín Ortenzi", "Jaz Ortenzi"],
        "apodo": "Jaz",
        "twitter": "@JazOrtenzi"
    },
    "lu giovannini": {
        "nombres": ["Lu Giovannini", "Luisina Giovannini"],
        "apodo": "Lu",
        "twitter": "@lulu_giova06"
    }
}

# Alias comunes desde la API (ej: iniciales o apellidos invertidos)
ALIAS_JUGADORES = {
    "f. cerundolo": "francisco cerundolo",
    "cerundolo f.": "francisco cerundolo",
    "s. baez": "sebastian baez",
    "baez s.": "sebastian baez",
    "t. m. etcheverry": "tomas martin etcheverry",
    "tomas etcheverry": "tomas martin etcheverry",
    "etcheverry t.": "tomas martin etcheverry",
    "m. navone": "mariano navone",
    "navone m.": "mariano navone",
    "f. diaz acosta": "facundo diaz acosta",
    "diaz acosta f.": "facundo diaz acosta",
    "diaz acosta": "facundo diaz acosta",
    "c. ugo carabelli": "camilo ugo carabelli",
    "ugo carabelli c.": "camilo ugo carabelli",
    "f. coria": "federico coria",
    "coria f.": "federico coria",
    "f. bagnis": "facundo bagnis",
    "bagnis f.": "facundo bagnis",
    "t. tirante": "thiago agustin tirante",
    "thiago tirante": "thiago agustin tirante",
    "j. m. cerundolo": "juan manuel cerundolo",
    "j. cerundolo": "juan manuel cerundolo",
    "f. comesaña": "francisco comesana",
    "f. comesana": "francisco comesana",
    "n. podoroska": "nadia podoroska",
    "podoroska n.": "nadia podoroska",
    "l. carle": "lourdes carle",
    "j. riera": "julia riera",
    "s. sierra": "solana sierra",
    "f. gomez": "federico gomez",
    "f. a. gomez": "federico gomez",
    "j. p. ficovich": "juan pablo ficovich",
    "l. midon": "lautaro midon",
    "a. olivieri genaro": "genaro alberto olivieri",
    "alberto olivieri genaro": "genaro alberto olivieri",
    "b. torres juan": "juan bautista torres",
    "bautista torres juan": "juan bautista torres",
    "m. la serna juan": "juan manuel la serna",
    "manuel la serna juan": "juan manuel la serna",
    "b. chelia": "benjamin chelia",
    "f. mena": "facundo mena",
    "s. rodriguez taverna": "santiago rodriguez taverna",
    "g. villanueva": "gonzalo villanueva",
    "e. ambrogi luciano": "luciano emanuel ambrogi",
    "emanuel ambrogi luciano": "luciano emanuel ambrogi",
    "r. burruchaga": "roman andres burruchaga",
    "m. trungelliti": "marco trungelliti",
    "m. kestelboim": "mariano kestelboim",
    "j. ortenzi": "jazmin ortenzi",
    "l. giovannini": "lu giovannini"
}

def normalizar_texto(t):
    """Normaliza texto removiendo acentos y pasando a minúsculas."""
    if not t: return ""
    return "".join(
        c for c in unicodedata.normalize('NFD', t.lower())
        if unicodedata.category(c) != 'Mn'
    ).strip()

def buscar_info_jugador(nombre_original):
    """Busca la información configurada para un jugador argentino."""
    if not nombre_original:
        return None
    norm = normalizar_texto(nombre_original)
    
    # 1. Búsqueda en alias
    if norm in ALIAS_JUGADORES:
        clave = ALIAS_JUGADORES[norm]
        return JUGADORES_ARG.get(clave)
        
    # 2. Búsqueda directa en base principal
    if norm in JUGADORES_ARG:
        return JUGADORES_ARG[norm]
        
    # 3. Búsqueda por sub-cadena
    for clave, data in JUGADORES_ARG.items():
        if clave in norm or norm in clave:
            return data
            
    for alias, clave in ALIAS_JUGADORES.items():
        if alias in norm or norm in alias:
            return JUGADORES_ARG.get(clave)
            
    return None

def obtener_nombre_variante(nombre_original):
    """
    Devuelve un nombre limpio y natural para el jugador argentino.
    NUNCA devuelve @handles en el flujo estándar para evitar que el bot
    suene a scraper o spam de Twitter.
    """
    info = buscar_info_jugador(nombre_original)
    if info and info.get("nombres"):
        return random.choice(info["nombres"])
    return nombre_original

def obtener_apodo_jugador(nombre_original):
    """Devuelve el apodo del jugador para usar en comentarios narrativos de festejo."""
    info = buscar_info_jugador(nombre_original)
    if info and info.get("apodo"):
        return info["apodo"]
    return None

def obtener_twitter_jugador(nombre_original):
    """Devuelve el handle de Twitter (@usuario) para menciones al pie si se desea."""
    info = buscar_info_jugador(nombre_original)
    if info and info.get("twitter"):
        return info["twitter"]
    return None


def traducir_estado_en_vivo(estado_api):
    """Traduce el estado del partido en vivo al español tenístico."""
    if not estado_api: return ""
    est = str(estado_api).lower().strip()
    
    if "1st set" in est: return "1er set"
    if "2nd set" in est: return "2do set"
    if "3rd set" in est: return "3er set"
    if "4th set" in est: return "4to set"
    if "5th set" in est: return "5to set"
    if "delayed" in est: return "Demorado"
    if "suspended" in est: return "Suspendido"
    if "interrupted" in est: return "Interrumpido"
    if "medical" in est or "med" in est: return "Atención médica"
    
    return estado_api


def _formatear_jugador_completo(nombre, bandera, ranking_str):
    """
    Formatea el nombre del jugador junto con su bandera y ranking,
    manteniendo la tipografía limpia sin espacios redundantes.
    """
    nombre_limpio = obtener_nombre_variante(nombre)
    partes = [nombre_limpio.strip()]
    if bandera and bandera.strip():
        partes.append(bandera.strip())
    if ranking_str and ranking_str.strip():
        partes.append(ranking_str.strip())
    return " ".join(partes)


def formatear_sets(scores, con_y=False, invertir=False):
    """
    Convierte la lista de scores de la API en notación tenística estándar.
    Ej: '6-4, 3-6, 6-4' o '6-4, 3-6 y 6-4' si con_y=True.
    Si invertir=True, invierte el orden para mostrar primero los games del ganador.
    Soporta formato de tiebreaks (ej: 7-6(4)).
    """
    if not scores or not isinstance(scores, list):
        return ""
    
    sets = []
    for s in scores:
        s1_raw = str(s.get('score_first', '0')).strip()
        s2_raw = str(s.get('score_second', '0')).strip()
        
        if invertir:
            s1_raw, s2_raw = s2_raw, s1_raw
            
        s1_num = s1_raw.split('.')[0]
        s2_num = s2_raw.split('.')[0]
        
        # Ignorar sets vacíos (0-0)
        if s1_num in ('0', '') and s2_num in ('0', ''):
            continue
            
        # Tiebreak si viene con decimal (ej: 7.4 -> 7-6(4))
        tb_pt = None
        if '.' in s1_raw:
            p = s1_raw.split('.')[1].strip()
            if p and p != '0': tb_pt = p
        elif '.' in s2_raw:
            p = s2_raw.split('.')[1].strip()
            if p and p != '0': tb_pt = p
            
        res_set = f"{s1_num}-{s2_num}"
        if tb_pt and ((s1_num == '7' and s2_num == '6') or (s1_num == '6' and s2_num == '7')):
            res_set += f"({tb_pt})"
            
        sets.append(res_set)
        
    if not sets:
        return ""
        
    if con_y and len(sets) > 1:
        return ", ".join(sets[:-1]) + f" y {sets[-1]}"
    return ", ".join(sets)


def determinar_ganador_partido(partido):
    """
    Determina si el ganador del partido fue el jugador 1 (retorna 1)
    o el jugador 2 (retorna 2), o 0 si no se puede determinar.
    """
    if not partido or not isinstance(partido, dict):
        return 0

    # 1. Campo event_winner oficial de la API
    ev_winner = partido.get('event_winner')
    if ev_winner:
        w_str = str(ev_winner).strip().lower()
        if w_str in ('first player', '1', '1st player', 'first_player', 'player 1', 'player1'):
            return 1
        if w_str in ('second player', '2', '2nd player', 'second_player', 'player 2', 'player2'):
            return 2
        
        # Comparación con player keys
        p1_key = str(partido.get('first_player_key', '')).strip()
        p2_key = str(partido.get('second_player_key', '')).strip()
        if p1_key and str(ev_winner).strip() == p1_key:
            return 1
        if p2_key and str(ev_winner).strip() == p2_key:
            return 2
            
        # Comparación con nombres
        j1_name = str(partido.get('event_first_player', '')).strip().lower()
        j2_name = str(partido.get('event_second_player', '')).strip().lower()
        if j1_name and (w_str == j1_name or w_str in j1_name or j1_name in w_str):
            return 1
        if j2_name and (w_str == j2_name or w_str in j2_name or j2_name in w_str):
            return 2

    # 2. event_final_result (ej: "2 - 1", "0 - 2")
    final_res = str(partido.get('event_final_result', '')).strip()
    if final_res and '-' in final_res:
        try:
            partes = final_res.replace('(', ' ').replace(')', ' ').split('-')
            s1_match = re.findall(r'\d+', partes[0])
            s2_match = re.findall(r'\d+', partes[1])
            if s1_match and s2_match:
                s1, s2 = int(s1_match[0]), int(s2_match[0])
                if s1 > s2:
                    return 1
                elif s2 > s1:
                    return 2
        except Exception:
            pass

    # 3. Analizar lista de scores (sets ganados)
    scores = partido.get('scores', [])
    if isinstance(scores, list) and scores:
        sets_p1, sets_p2 = 0, 0
        for s in scores:
            try:
                g1 = int(str(s.get('score_first', '0')).split('.')[0])
                g2 = int(str(s.get('score_second', '0')).split('.')[0])
                if (g1 >= 6 and g1 - g2 >= 2) or (g1 == 7 and g2 in (5, 6)):
                    sets_p1 += 1
                elif (g2 >= 6 and g2 - g1 >= 2) or (g2 == 7 and g1 in (5, 6)):
                    sets_p2 += 1
            except Exception:
                continue
        if sets_p1 > sets_p2:
            return 1
        elif sets_p2 > sets_p1:
            return 2

    # 4. Analizar event_status si indica quién se retiró
    status = str(partido.get('event_status', '')).strip().lower()
    j1_name = str(partido.get('event_first_player', '')).strip().lower()
    j2_name = str(partido.get('event_second_player', '')).strip().lower()
    if 'retir' in status or 'walkover' in status or 'w.o.' in status:
        if j1_name and any(part in status for part in j1_name.split() if len(part) > 2):
            return 2
        if j2_name and any(part in status for part in j2_name.split() if len(part) > 2):
            return 1

    return 0


def detectar_tipo_finalizacion(partido):
    """
    Determina cómo finalizó el partido:
    - 'normal': Jugando todos los sets
    - 'retiro': Se retiró durante el partido con juego disputado
    - 'walkover': Sin juego o marcador 0-0 previo (W.O.)
    - 'descalificacion': Default / DQ
    """
    if not partido or not isinstance(partido, dict):
        return 'normal'
        
    status = str(partido.get('event_status', '')).strip().lower()
    final_res = str(partido.get('event_final_result', '')).strip()
    scores = partido.get('scores', [])
    
    es_retiro_kw = any(k in status for k in ['retir', 'ret.', 'after ret'])
    es_wo_kw = any(k in status for k in ['walkover', 'w.o.', 'wo'])
    es_dq_kw = any(k in status for k in ['default', 'def.', 'disqualif', 'dq'])
    
    # Verificar si hubo juego efectivo
    hubo_juego = False
    if scores and isinstance(scores, list):
        for s in scores:
            g1 = str(s.get('score_first', '0')).split('.')[0].strip()
            g2 = str(s.get('score_second', '0')).split('.')[0].strip()
            if (g1 not in ('0', '')) or (g2 not in ('0', '')):
                hubo_juego = True
                break
    elif final_res and final_res not in ('0 - 0', '0-0', '0/0', ''):
        try:
            partes = final_res.replace('(', ' ').replace(')', ' ').split('-')
            s1_match = re.findall(r'\d+', partes[0])
            s2_match = re.findall(r'\d+', partes[1])
            if s1_match and s2_match and (int(s1_match[0]) > 0 or int(s2_match[0]) > 0):
                hubo_juego = True
        except Exception:
            pass

    if es_dq_kw:
        return 'descalificacion'
    if es_wo_kw:
        return 'retiro' if hubo_juego else 'walkover'
    if es_retiro_kw:
        return 'retiro' if hubo_juego else 'walkover'
        
    return 'normal'


def extraer_categoria(partido):
    """Extrae la categoría del torneo (ATP, WTA, Challenger, ITF)."""
    name = partido.get('tournament_name', '').upper()
    etype = partido.get('event_type_type', '').upper()
    full = f"{name} {etype}"
    
    if "ATP" in full: return "ATP"
    if "WTA" in full: return "WTA"
    if "CHALLENGER" in full: return "Challenger"
    if "ITF" in full: return "ITF"
    return ""


def traducir_ronda(ronda_api, corto=False):
    """Traduce la ronda de la API al español del tenis argentino."""
    if not ronda_api: return ""
    r = str(ronda_api).lower()
    
    if "final" in r and "quarter" not in r and "semi" not in r and "1/" not in r:
        return "Final"
    if "semi" in r:
        return "Semis" if corto else "Semifinales"
    if "quarter" in r or "1/4" in r:
        return "Cuartos" if corto else "Cuartos de final"
    if "1/8" in r:
        return "Octavos" if corto else "Octavos de final"
    if "1/16" in r:
        return "16avos" if corto else "16avos de final"
    if "1/32" in r:
        return "32avos" if corto else "32avos de final"
    if "1/64" in r:
        return "64avos" if corto else "64avos de final"
    
    if "qualif" in r or "qualy" in r:
        match = re.search(r'\d+', r)
        if match:
            return f"R{match.group()} Qualy"
        return "Qualy"
    
    if "round 1" in r or "1st round" in r:
        return "1ra Ronda" if corto else "Primera ronda"
    if "round 2" in r or "2nd round" in r:
        return "2da Ronda" if corto else "Segunda ronda"
    if "round 3" in r or "3rd round" in r:
        return "3ra Ronda" if corto else "Tercera ronda"
    if "round" in r:
        return "Ronda previa"
        
    return ""


def traducir_nombre_torneo(nombre):
    """Traduce nombres de torneos al español para el público argentino."""
    nombre_low = nombre.lower()
    tiene_junior = "junior" in nombre_low
    
    traducciones = {
        "rome": "Roma",
        "internazionali d'italia": "Roma",
        "indian wells masters": "Indian Wells",
        "miami open": "Miami",
        "monte-carlo masters": "Montecarlo",
        "madrid open": "Madrid",
        "canadian open": "Canadá",
        "toronto": "Toronto",
        "montreal": "Montreal",
        "cincinnati masters": "Cincinnati",
        "shanghai masters": "Shanghai",
        "paris masters": "París",
        "paris": "París",
        "french open": "Roland Garros",
        "australian open": "Australian Open",
        "us open": "US Open",
        "wimbledon": "Wimbledon",
    }
    
    traduccion = nombre
    for en, es in traducciones.items():
        if en in nombre_low:
            traduccion = es
            break
            
    if tiene_junior and "junior" not in traduccion.lower():
        traduccion = f"{traduccion} Junior"
        
    return traduccion


def obtener_hashtag_torneo(nombre_torneo, categoria=""):
    """Mapea nombres de torneos a sus hashtags oficiales o genera uno genérico."""
    nombre = nombre_torneo.lower()
    
    mapping = {
        "roma": "#IBI26",
        "rome": "#IBI26",
        "madrid": "#MMOPEN",
        "monte-carlo": "#MonteCarloMasters",
        "roland garros qualifying": "#RolandGarros",
        "roland garros qualy": "#RolandGarros",
        "qualifying roland garros": "#RolandGarros",
        "french open qualifying": "#RolandGarros",
        "roland garros": "#RolandGarros",
        "french open": "#RolandGarros",
        "wimbledon": "#Wimbledon",
        "us open": "#USOpen",
        "australian open": "#AusOpen",
        "miami": "#MiamiOpen",
        "indian wells": "#IndianWells",
        "buenos aires": "#IEBMasArgOpen",
        "cordoba": "#CordobaOpen"
    }
    
    for key, hashtag in mapping.items():
        if key in nombre:
            return hashtag
            
    nombre_base = nombre_torneo.split(',')[0]
    nombre_sin_prefijo = re.sub(r'^(ITF|ATP|WTA|Challenger|M\d+|W\d+)\s+', '', nombre_base, flags=re.IGNORECASE).strip()
    
    if not nombre_sin_prefijo:
        nombre_sin_prefijo = nombre_base
        
    nombre_final = "".join(char for char in nombre_sin_prefijo if char.isalnum())
    
    if categoria:
        cat_clean = str(categoria).strip()
        if not nombre_final.lower().startswith(cat_clean.lower()):
            nombre_final = cat_clean + nombre_final
            
    return "#" + nombre_final


def obtener_frases_torneo(torneo_original, partidos):
    """
    Retorna conectores y nombres pulidos para el torneo,
    manejando Grand Slams y Qualy con naturalidad.
    """
    torneo = traducir_nombre_torneo(torneo_original)
    cat = extraer_categoria(partidos[0])
    
    es_gs = any(gs in torneo.lower() for gs in ["roland garros", "wimbledon", "us open", "australian open"])
    todos_qualy = all(p.get('es_qualy') for p in partidos)
    
    frases = {}
    
    if es_gs:
        if todos_qualy:
            frases["en"] = f"en la Qualy de {torneo}"
            frases["del"] = f"de la Qualy de {torneo}"
            frases["al"] = f"a la Qualy de {torneo}"
            frases["nombre"] = f"la Qualy de {torneo}"
        else:
            if "us open" in torneo.lower() or "australian open" in torneo.lower():
                frases["en"] = f"en el {torneo}"
                frases["del"] = f"del {torneo}"
                frases["al"] = f"al {torneo}"
                frases["nombre"] = f"el {torneo}"
            else:
                frases["en"] = f"en {torneo}"
                frases["del"] = f"de {torneo}"
                frases["al"] = f"a {torneo}"
                frases["nombre"] = torneo
    else:
        prefijo = f"{cat} " if (cat and not torneo.lower().startswith(cat.lower())) else ""
        if todos_qualy:
            conector = "del " if (cat or "open" in torneo.lower() or "challenger" in torneo.lower()) else "de "
            frases["en"] = f"en la Qualy {conector}{prefijo}{torneo}".strip()
            frases["del"] = f"de la Qualy {conector}{prefijo}{torneo}".strip()
            frases["al"] = f"a la Qualy {conector}{prefijo}{torneo}".strip()
            frases["nombre"] = f"la Qualy {conector}{prefijo}{torneo}".strip()
        else:
            conector = "el " if (cat or "open" in torneo.lower() or "masters" in torneo.lower() or "challenger" in torneo.lower()) else ""
            frases["en"] = f"en {conector}{prefijo}{torneo}".strip() if conector else f"en {prefijo}{torneo}".strip()
            frases["del"] = f"del {prefijo}{torneo}".strip() if conector else f"de {prefijo}{torneo}".strip()
            frases["al"] = f"al {prefijo}{torneo}".strip() if conector else f"a {prefijo}{torneo}".strip()
            frases["nombre"] = f"{conector}{prefijo}{torneo}".strip() if conector else f"{prefijo}{torneo}".strip()
            
    return frases


# ==============================================================================
# ANÁLISIS DE RESULTADOS Y SENTIMIENTO DE PARTIDO
# ==============================================================================

def analizar_resultado_argentino(partido):
    """
    Analiza el resultado del argentino con foco periodístico tenístico:
    Identifica si fue paliza, remontada, batalla a 3 sets, campeonato, o derrota.
    Devuelve (mensaje_corto, gano_bool).
    """
    arg_info = partido.get('arg_info', {})
    j1_es_arg = arg_info.get('jugador_1', {}).get('es_arg', False)
    j2_es_arg = arg_info.get('jugador_2', {}).get('es_arg', False)
    
    if j1_es_arg and j2_es_arg:
        return "", None
        
    ganador = determinar_ganador_partido(partido)
    tipo_fin = detectar_tipo_finalizacion(partido)
    
    gano = None
    if j1_es_arg:
        if ganador == 1: gano = True
        elif ganador == 2: gano = False
    elif j2_es_arg:
        if ganador == 2: gano = True
        elif ganador == 1: gano = False
            
    if gano is None:
        return "", None
        
    nombre_j1 = partido.get('event_first_player', 'Rival')
    nombre_j2 = partido.get('event_second_player', 'Rival')
    rival = nombre_j2 if j1_es_arg else nombre_j1
    
    if tipo_fin == 'walkover':
        if gano:
            return f"Victoria por Walkover (W.O.) ante {rival}", True
        else:
            return "Baja por Walkover (W.O.)", False
            
    if tipo_fin == 'retiro':
        if gano:
            return f"Victoria por retiro de {rival}", True
        else:
            return "Derrota por retiro", False
            
    if tipo_fin == 'descalificacion':
        if gano:
            return f"Victoria por descalificación de {rival}", True
        else:
            return "Derrota por descalificación", False
            
    # Sets ganados
    final_res = partido.get('event_final_result', "0 - 0")
    try:
        partes = final_res.replace('(', ' ').replace(')', ' ').split('-')
        s1 = int(re.findall(r'\d+', partes[0])[0])
        s2 = int(re.findall(r'\d+', partes[1])[0])
    except Exception:
        s1, s2 = 0, 0
        
    sets_arg = s1 if j1_es_arg else s2
    sets_riv = s2 if j1_es_arg else s1
    
    ronda = traducir_ronda(partido.get('tournament_round', ''))
    es_qualy = partido.get('es_qualy', False)
    es_final = (ronda == "Final" and not es_qualy)

    if es_final:
        if gano:
            mensajes = ["¡CAMPEÓN! 🏆🇦🇷", "¡Se consagró campeón! 🏆", "¡El título es argentino! 🏆🇦🇷"]
        else:
            mensajes = ["Subcampeón tras una gran semana 🇦🇷", "Se escapó la final por poco 🇦🇷"]
    else:
        if gano:
            if sets_riv >= 1:
                mensajes = ["¡Triunfazo en tres sets! 💪🇦🇷", "¡Victoria batallada! 🇦🇷🔥", "¡Partidazo y adentro! 👏"]
            else:
                mensajes = ["¡Sólida victoria en sets corridos! 🇦🇷", "¡Gran triunfo y a la siguiente ronda! 👏", "Paso firme y adentro 🇦🇷"]
        else:
            if sets_arg >= 1:
                mensajes = ["Batalló hasta el final pero no alcanzó 🇦🇷", "Se escapó en el cierre de un partidazo 🇦🇷", "Dejó todo en la cancha 🇦🇷"]
            else:
                mensajes = ["Paso en falso hoy 🇦🇷", "Dura derrota en el circuito 🇦🇷", "Fin del torneo para el argentino 🇦🇷"]
                
    return random.choice(mensajes), gano


# ==============================================================================
# FORMATEADOR DE HILOS INTELIGENTE (SIN CORTE HUÉRFANO)
# ==============================================================================

def _formatear_en_hilo(encabezado, lineas_items, cierres, max_chars=280):
    """
    Formatea el contenido en uno o más tweets (hilo).
    Si todo entra en un solo tweet, NO genera hilo.
    Si excede 280 caracteres, divide inteligentemente sin dejar cierres huérfanos.
    """
    cierre = random.choice(cierres) if cierres else ""
    margen_hilo = 14  # margen para numeración de hilos (1/2) 🧵
    limite = max_chars - margen_hilo
    
    # Intento 1: ¿Entra todo en un solo tweet?
    texto_completo = encabezado + "\n\n" + "\n".join(lineas_items)
    if cierre:
        texto_completo += "\n\n" + cierre
        
    if len(texto_completo) <= max_chars:
        return [f"--- INICIO TWEET ---\n{texto_completo.strip()}\n--- FIN TWEET ---"]
        
    # Intento 2: Particionar en tweets respetando el límite
    tweets_raw = []
    current_text = encabezado + "\n\n"
    
    for i, linea in enumerate(lineas_items):
        es_ultimo = (i == len(lineas_items) - 1)
        espacio_requerido = len(linea) + 1
        if es_ultimo and cierre:
            espacio_requerido += len(cierre) + 2
            
        if len(current_text) + espacio_requerido > limite and current_text.strip() != "":
            tweets_raw.append(current_text.strip())
            current_text = "Sigue la lista: 👇\n\n" + linea + "\n"
        else:
            current_text += linea + "\n"
            
    if cierre:
        if len(current_text) + len(cierre) + 2 <= limite:
            current_text += "\n" + cierre
            tweets_raw.append(current_text.strip())
        else:
            tweets_raw.append(current_text.strip())
            tweets_raw.append(cierre.strip())
    else:
        if current_text.strip():
            tweets_raw.append(current_text.strip())
            
    total_tweets = len(tweets_raw)
    hilo_final = []
    for idx, t in enumerate(tweets_raw):
        texto_final = t
        if total_tweets > 1:
            texto_final += f"\n\n({idx+1}/{total_tweets}) 🧵"
        hilo_final.append(f"--- INICIO TWEET ---\n{texto_final}\n--- FIN TWEET ---")
        
    return hilo_final


# ==============================================================================
# BLOQUE 1: AGENDA DE PARTIDOS
# ==============================================================================

def generar_tweet_agenda(torneo_original, partidos):
    """
    Genera el tweet de agenda para la jornada:
    - Si es 1 solo partido: Formato cartelera enfocado en el duelo con gancho.
    - Si son 2 o más: Cartelera visual compacta y limpia (estilo Tenis Twitter).
    """
    if not partidos:
        return []
        
    torneo = traducir_nombre_torneo(torneo_original)
    cat = extraer_categoria(partidos[0])
    tag_torneo = obtener_hashtag_torneo(torneo, cat)
    frases = obtener_frases_torneo(torneo_original, partidos)
    todos_qualy = all(p.get('es_qualy') for p in partidos)
    
    # -------------------------------------------------------------
    # CASO 1: PARTIDO ÚNICO EN LA JORNADA (Formato Cartelera Foco)
    # -------------------------------------------------------------
    if len(partidos) == 1:
        p = partidos[0]
        hora = p.get('event_time', 'S/H')
        hora_str = f"~{hora} hs" if hora != 'S/H' else "Horario a confirmar"
        
        info = p.get('arg_info', {})
        pais1 = info.get('jugador_1', {}).get('pais', '')
        pais2 = info.get('jugador_2', {}).get('pais', '')
        
        flag1 = obtener_bandera(pais1)
        flag2 = obtener_bandera(pais2)
        
        rank1 = info.get('jugador_1', {}).get('ranking')
        rank2 = info.get('jugador_2', {}).get('ranking')
        r1_str = f"({rank1}°)" if rank1 and int(rank1) < 2500 else ""
        r2_str = f"({rank2}°)" if rank2 and int(rank2) < 2500 else ""
        
        j1_raw = p.get('event_first_player')
        j2_raw = p.get('event_second_player')
        j1_nombre = _formatear_jugador_completo(j1_raw, "", r1_str).strip()
        j2_nombre = _formatear_jugador_completo(j2_raw, "", r2_str).strip()
        
        ronda = traducir_ronda(p.get('tournament_round', ''))
        if p.get('es_qualy') and "qualy" not in ronda.lower():
            ronda = f"{ronda} (Qualy)" if ronda else "Qualy"
        ronda_linea = f"🏆 {ronda}\n" if ronda else ""
        
        es_derbi = es_derbi_argentino(pais1, pais2)
        
        if es_derbi:
            j1_nombre = _formatear_jugador_completo(j1_raw, "", r1_str).strip()
            j2_nombre = _formatear_jugador_completo(j2_raw, "", r2_str).strip()
            encabezado = f"🇦🇷🎾 ¡DUELO ARGENTINO EN {torneo.upper()}!"
            ganchos = [
                "Un compatriota asegurado en la próxima ronda. ¿Quién se lo lleva? 🍿🔥",
                "Hermoso choque albiceleste. ¿Por quién van hoy? 🍿🇦🇷",
                "Promesa de partidazo entre compatriotas. ¿Cómo lo ven? 🍿"
            ]
            cuerpo = (
                f"{encabezado}\n\n"
                f"⏰ {hora_str}\n"
                f"⚔️ {j1_nombre} 🇦🇷 vs {j2_nombre} 🇦🇷\n"
                f"{ronda_linea}\n"
                f"{random.choice(ganchos)} {tag_torneo}"
            )
        else:
            j1_es_arg = info.get('jugador_1', {}).get('es_arg', False)
            if j1_es_arg:
                arg_str = _formatear_jugador_completo(j1_raw, "", r1_str).strip()
                riv_str = _formatear_jugador_completo(j2_raw, flag2, r2_str).strip()
            else:
                arg_str = _formatear_jugador_completo(j2_raw, "", r2_str).strip()
                riv_str = _formatear_jugador_completo(j1_raw, flag1, r1_str).strip()
                
            encabezados = [
                f"🇦🇷🎾 ¡Juega {arg_str.split('(')[0].strip()} {frases['en']}!",
                f"🇦🇷 Acción de tenis hoy {frases['en']}:",
                f"🇦🇷 Día de partido para los nuestros {frases['en']}:"
            ]
            ganchos = [
                "¿Cómo lo ven para dar el paso hoy? 🍿🎾",
                "¡A bancar a los nuestros! ¿Pasa de ronda? 💪🇦🇷",
                "Lindo desafío en la cancha. ¿Se mete a la próxima fase? 🍿",
                "Todo listo para seguirlo punto a punto. ¡Vamos! 🇦🇷🎾"
            ]
            cuerpo = (
                f"{random.choice(encabezados)}\n\n"
                f"⏰ {hora_str}\n"
                f"⚔️ {arg_str} vs {riv_str}\n"
                f"{ronda_linea}\n"
                f"{random.choice(ganchos)} {tag_torneo}"
            )
            
        return [f"--- INICIO TWEET ---\n{cuerpo.strip()}\n--- FIN TWEET ---"]

    # -------------------------------------------------------------
    # CASO 2: MÚLTIPLES PARTIDOS EN LA JORNADA (Cartelera Compacta)
    # -------------------------------------------------------------
    rondas_presentes = {traducir_ronda(p.get('tournament_round', '')) for p in partidos if p.get('tournament_round')}
    
    if "Final" in rondas_presentes and not todos_qualy:
        encabezados = [
            f"🏆 ¡Día de FINAL {frases['en']}! Horarios de los argentinos: 🇦🇷",
            f"Se juega la gran final {frases['del']} con presencia argentina: 🏆🇦🇷"
        ]
    elif "Semifinales" in rondas_presentes or "Semis" in rondas_presentes:
        encabezados = [
            f"¡Día de Semifinales {frases['en']}! Juegan los nuestros: 🇦🇷",
            f"Buscando el pase a la final {frases['en']}: 🇦🇷"
        ]
    elif "Cuartos de final" in rondas_presentes or "Cuartos" in rondas_presentes:
        encabezados = [
            f"Cuartos de final {frases['en']}. Así juegan los nuestros: 🇦🇷",
            f"¡Día de Cuartos {frases['en']}! La agenda argentina: 🇦🇷"
        ]
    elif todos_qualy:
        encabezados = [
            f"Agenda de la Qualy {frases['del']}: 🇦🇷",
            f"¡Acción en la clasificación {frases['del']}! Horarios: 🇦🇷"
        ]
    else:
        encabezados = [
            f"🇦🇷 Agenda argentina para hoy {frases['en']}:",
            f"🇦🇷 ¡Juegan los nuestros {frases['en']}! Los horarios:",
            f"🇦🇷 Cartelera de hoy {frases['en']}:"
        ]
        
    encabezado = random.choice(encabezados)
    lineas_partidos = []
    
    for p in partidos:
        hora = p.get('event_time', 'S/H')
        hora_txt = f"~{hora} hs" if hora != 'S/H' else "A confirmar"
        
        info = p.get('arg_info', {})
        pais1 = info.get('jugador_1', {}).get('pais', '')
        pais2 = info.get('jugador_2', {}).get('pais', '')
        flag1 = obtener_bandera(pais1)
        flag2 = obtener_bandera(pais2)
        
        j1_raw = p.get('event_first_player')
        j2_raw = p.get('event_second_player')
        j1_nom = obtener_nombre_variante(j1_raw)
        j2_nom = obtener_nombre_variante(j2_raw)
        
        ronda = traducir_ronda(p.get('tournament_round', ''), corto=True)
        ronda_tag = f" ({ronda})" if ronda else ""
        
        j1_es_arg = info.get('jugador_1', {}).get('es_arg', False)
        
        if es_derbi_argentino(pais1, pais2):
            line = f"• {hora_txt} | 🇦🇷 {j1_nom} vs {j2_nom} (Duelo Argentino){ronda_tag}"
        else:
            if j1_es_arg:
                line = f"• {hora_txt} | {j1_nom} vs {j2_nom} {flag2}{ronda_tag}"
            else:
                line = f"• {hora_txt} | {j2_nom} vs {j1_nom} {flag1}{ronda_tag}"
                
        lineas_partidos.append(line.strip())
        
    cierres = [
        f"¿Quién mete victoria hoy? ¡A bancar a los nuestros! 🍿🇦🇷 {tag_torneo}",
        f"Lindo día para seguir a la legión. ¡Vamos! 🎾💪 {tag_torneo}",
        f"Mucho tenis por delante. ¿Cómo los ven? 🍿🇦🇷 {tag_torneo}",
        f"Todo listo para una gran jornada. ¡A dejar todo! 🇦🇷🎾 {tag_torneo}"
    ]
    
    return _formatear_en_hilo(encabezado, lineas_partidos, cierres)


# ==============================================================================
# BLOQUE 2: ACTUALIZACIÓN EN VIVO
# ==============================================================================

def generar_tweet_actualizacion(torneo_original, partidos):
    """
    Genera el tweet de estado en vivo para partidos en juego:
    Sin corchetes de sistema ni barras diagonales. Notación limpia de tenis.
    """
    if not partidos:
        return []
        
    torneo = traducir_nombre_torneo(torneo_original)
    cat = extraer_categoria(partidos[0])
    tag_torneo = obtener_hashtag_torneo(torneo, cat)
    frases = obtener_frases_torneo(torneo_original, partidos)
    
    # -------------------------------------------------------------
    # CASO 1: UN SOLO PARTIDO EN JUEGO
    # -------------------------------------------------------------
    if len(partidos) == 1:
        p = partidos[0]
        info = p.get('arg_info', {})
        pais1 = info.get('jugador_1', {}).get('pais', '')
        pais2 = info.get('jugador_2', {}).get('pais', '')
        flag1 = obtener_bandera(pais1)
        flag2 = obtener_bandera(pais2)
        
        j1_nom = obtener_nombre_variante(p.get('event_first_player'))
        j2_nom = obtener_nombre_variante(p.get('event_second_player'))
        
        scores_api = p.get('scores', [])
        marcador = formatear_sets(scores_api)
        if not marcador:
            marcador = "0-0"
            
        estado_api = p.get('event_status', '')
        estado_txt = traducir_estado_en_vivo(estado_api)
        estado_str = f" — {estado_txt}" if estado_txt else ""
        
        ronda = traducir_ronda(p.get('tournament_round', ''), corto=True)
        ronda_str = f" ({ronda})" if ronda else ""
        
        es_derbi = es_derbi_argentino(pais1, pais2)
        
        if es_derbi:
            encabezado = f"🎾 En juego en {torneo}{ronda_str} (Duelo Argentino 🇦🇷):"
            linea_score = f"{j1_nom} vs {j2_nom}: {marcador}{estado_str}"
        else:
            j1_es_arg = info.get('jugador_1', {}).get('es_arg', False)
            if j1_es_arg:
                linea_score = f"{j1_nom} 🇦🇷 vs {j2_nom} {flag2}: {marcador}{estado_str}"
            else:
                linea_score = f"{j2_nom} 🇦🇷 vs {j1_nom} {flag1}: {marcador}{estado_str}"
            encabezado = f"🎾 En juego {frases['en']}{ronda_str}:"
            
        cierres_single = [
            f"¡Seguimos el punto a punto! 💪🇦🇷 {tag_torneo}",
            f"¡Vamos carajo, a seguir metiendo! 🇦🇷🎾 {tag_torneo}",
            f"Punto a punto por el pase de ronda 🍿 {tag_torneo}"
        ]
        
        cuerpo = f"{encabezado}\n\n{linea_score}\n\n{random.choice(cierres_single)}"
        return [f"--- INICIO TWEET ---\n{cuerpo.strip()}\n--- FIN TWEET ---"]

    # -------------------------------------------------------------
    # CASO 2: VARIOS PARTIDOS EN JUEGO (Resumen Live)
    # -------------------------------------------------------------
    encabezados = [
        f"🎾 Así marcha la acción en vivo {frases['en']}: 🇦🇷",
        f"🎾 En juego en este momento {frases['en']}:",
        f"🎾 Actualizamos los partidos de los nuestros {frases['en']}:"
    ]
    encabezado = random.choice(encabezados)
    lineas_partidos = []
    
    for p in partidos:
        info = p.get('arg_info', {})
        pais1 = info.get('jugador_1', {}).get('pais', '')
        pais2 = info.get('jugador_2', {}).get('pais', '')
        flag2 = obtener_bandera(pais2)
        flag1 = obtener_bandera(pais1)
        
        j1_nom = obtener_nombre_variante(p.get('event_first_player'))
        j2_nom = obtener_nombre_variante(p.get('event_second_player'))
        
        scores_api = p.get('scores', [])
        marcador = formatear_sets(scores_api) or "0-0"
        
        estado_api = p.get('event_status', '')
        estado_txt = traducir_estado_en_vivo(estado_api)
        estado_str = f" ({estado_txt})" if estado_txt else ""
        
        ronda = traducir_ronda(p.get('tournament_round', ''), corto=True)
        prefijo = f"• [{ronda}] " if ronda else "• "
        
        if es_derbi_argentino(pais1, pais2):
            line = f"{prefijo}🇦🇷 {j1_nom} vs {j2_nom}: {marcador}{estado_str}"
        else:
            j1_es_arg = info.get('jugador_1', {}).get('es_arg', False)
            if j1_es_arg:
                line = f"{prefijo}{j1_nom} vs {j2_nom} {flag2}: {marcador}{estado_str}"
            else:
                line = f"{prefijo}{j2_nom} vs {j1_nom} {flag1}: {marcador}{estado_str}"
                
        lineas_partidos.append(line.strip())
        
    cierres = [
        f"¡A seguir prendidos al minuto a minuto! 🇦🇷💪 {tag_torneo}",
        f"Seguimos punto a punto la jornada. ¡Vamos! 🇦🇷🎾 {tag_torneo}",
        f"¡Mucha garra en la cancha! 🇦🇷 {tag_torneo}"
    ]
    
    return _formatear_en_hilo(encabezado, lineas_partidos, cierres)


# ==============================================================================
# BLOQUE 3: RESULTADOS FINALES
# ==============================================================================

def generar_tweet_finalizado(torneo_original, partidos):
    """
    Genera el tweet para partidos finalizados:
    - Si es 1 solo partido: Tweet periodístico con titular potente, narrativa de tenis y análisis.
    - Si son varios: Resumen limpio y estructurado de la jornada sin clichés repetitivos.
    """
    if not partidos:
        return []
        
    torneo = traducir_nombre_torneo(torneo_original)
    cat = extraer_categoria(partidos[0])
    tag_torneo = obtener_hashtag_torneo(torneo, cat)
    frases = obtener_frases_torneo(torneo_original, partidos)
    
    # -------------------------------------------------------------
    # CASO 1: RESULTADO DE UN SOLO PARTIDO (Formato Noticioso Narrativo)
    # -------------------------------------------------------------
    if len(partidos) == 1:
        p = partidos[0]
        info = p.get('arg_info', {})
        pais1 = info.get('jugador_1', {}).get('pais', '')
        pais2 = info.get('jugador_2', {}).get('pais', '')
        
        j1_raw = p.get('event_first_player')
        j2_raw = p.get('event_second_player')
        j1_nom = obtener_nombre_variante(j1_raw)
        j2_nom = obtener_nombre_variante(j2_raw)
        
        flag1 = obtener_bandera(pais1)
        flag2 = obtener_bandera(pais2)
        
        ganador = determinar_ganador_partido(p)
        tipo_fin = detectar_tipo_finalizacion(p)
        
        scores_api = p.get('scores', [])
        marcador_narrativo = formatear_sets(scores_api, con_y=True, invertir=(ganador == 2)) or p.get('event_final_result', '')
        if str(marcador_narrativo).strip() in ('0-0', '0 - 0', ''):
            marcador_narrativo = ""
            
        ronda = traducir_ronda(p.get('tournament_round', ''))
        ronda_corta = traducir_ronda(p.get('tournament_round', ''), corto=True)
        ronda_txt = f"en {ronda}" if ronda else f"{frases['en']}"
        
        es_derbi = es_derbi_argentino(pais1, pais2)
        
        # A. Duelo Argentino (Derbi)
        if es_derbi:
            ganador_nom = j1_nom if ganador == 1 else (j2_nom if ganador == 2 else j1_nom)
            perdedor_nom = j2_nom if ganador == 1 else (j1_nom if ganador == 2 else j2_nom)
            
            if tipo_fin == 'walkover':
                titular = f"🇦🇷 DERBI: ¡AVANZA {ganador_nom.upper()}! (W.O.)"
                cuerpo = f"{ganador_nom} avanzó {ronda_txt} ante la no presentación (Walkover) de {perdedor_nom}."
            elif tipo_fin == 'retiro':
                titular = f"🇦🇷 DERBI: ¡AVANZA {ganador_nom.upper()} TRAS RETIRO!"
                score_str = f" ({marcador_narrativo})" if marcador_narrativo else ""
                cuerpo = f"{ganador_nom} avanzó {ronda_txt} tras el retiro de {perdedor_nom}{score_str}."
            else:
                titulares_derbi = [
                    f"🇦🇷 DERBI: ¡VICTORIA PARA {ganador_nom.upper()}!",
                    f"🇦🇷 DERBI ALBICELESTE: ¡TRIUNFO DE {ganador_nom.upper()}! 👏",
                    f"🇦🇷 ¡FESTEJA {ganador_nom.upper()} EN EL DUELO DE COMPATRIOTAS! 🔥"
                ]
                titular = random.choice(titulares_derbi)
                cuerpo = f"En un gran cruce argentino {ronda_txt}, {ganador_nom} superó a {perdedor_nom} por {marcador_narrativo}."
                
            remate = f"¡Gran partido de ambos compatriotas! 👏🍿 {tag_torneo}"
            tweet_texto = f"{titular}\n\n{cuerpo}\n\n{remate}"
            return [f"--- INICIO TWEET ---\n{tweet_texto.strip()}\n--- FIN TWEET ---"]

        # B. Partido Internacional (Argentino vs Rival)
        j1_es_arg = info.get('jugador_1', {}).get('es_arg', False)
        arg_nom = j1_nom if j1_es_arg else j2_nom
        riv_nom = j2_nom if j1_es_arg else j1_nom
        riv_flag = flag2 if j1_es_arg else flag1
        
        gano = (ganador == 1) if j1_es_arg else (ganador == 2)
        es_final = (ronda == "Final" and not p.get('es_qualy', False))
        
        # Casos especiales de finalización
        if tipo_fin == 'walkover':
            if gano:
                titular = f"¡TRIUNFO ARGENTINO! 🇦🇷"
                cuerpo = f"{arg_nom} avanzó {ronda_txt} por Walkover (W.O.) ante la baja de {riv_nom} {riv_flag}."
                remate = f"¡Adelante y a pensar en la próxima ronda! 💪 {tag_torneo}"
            else:
                titular = f"BAJA PARA {arg_nom.upper()} 🇦🇷"
                cuerpo = f"{arg_nom} no pudo presentarse por Walkover ante {riv_nom} {riv_flag} y se despidió {frases['del']}."
                remate = f"Pronta recuperación para el argentino. 💪 {tag_torneo}"
            tweet_texto = f"{titular}\n\n{cuerpo}\n\n{remate}"
            return [f"--- INICIO TWEET ---\n{tweet_texto.strip()}\n--- FIN TWEET ---"]
            
        if tipo_fin == 'retiro':
            score_str = f" ({marcador_narrativo})" if marcador_narrativo else ""
            if gano:
                titular = f"¡TRIUNFO Y PASE DE RONDA! 🇦🇷"
                cuerpo = f"{arg_nom} avanzó {ronda_txt} tras el retiro de {riv_nom} {riv_flag}{score_str}."
                remate = f"¡Sigue firme en {torneo}! A por el próximo desafío. 👏 {tag_torneo}"
            else:
                titular = f"RETIRO POR LESIÓN ❌"
                cuerpo = f"{arg_nom} debió retirarse ante {riv_nom} {riv_flag}{score_str} y se despidió {frases['del']}."
                remate = f"Dura noticia para los nuestros. ¡A recuperarse pronto! 🇦🇷💪 {tag_torneo}"
            tweet_texto = f"{titular}\n\n{cuerpo}\n\n{remate}"
            return [f"--- INICIO TWEET ---\n{tweet_texto.strip()}\n--- FIN TWEET ---"]

        # Finales normales (Jugadas)
        if gano:
            if es_final:
                titulares = [
                    f"🏆 ¡CAMPEÓN EN {torneo.upper()}! 🇦🇷",
                    f"¡EL TÍTULO ES ARGENTINO! 🏆🇦🇷",
                    f"🏆 ¡GRI-TA CAM-PEÓN {arg_nom.upper()}! 🇦🇷🔥"
                ]
                remates = [
                    "¡Semana soñada y trofeo a casa! Salud, campeón. 🏆👏",
                    "Cátedra de tenis en la final para levantar el título. ¡Enorme! 🏆🔥"
                ]
            else:
                # Titulares según la ronda o intensidad
                titulares = [
                    f"¡A {ronda_corta.upper()}, {arg_nom.upper()}! 🇦🇷🔥" if ronda_corta else f"¡TRIUNFAZO DE {arg_nom.upper()}! 🇦🇷🔥",
                    f"¡ENORME VICTORIA! 👏🇦🇷",
                    f"¡GRAN PASO EN {torneo.upper()}! 🇦🇷💪"
                ]
                remates = [
                    "¡A seguir por este camino! Gran partido de los nuestros. 👏🎾",
                    "Partidazo y pasaje a la próxima ronda. ¡Vamos con todo! 💪🔥",
                    "Sólido nivel para meterse en la siguiente instancia. ¡A soñar! 🍿🇦🇷"
                ]
            
            titular = random.choice(titulares)
            verbos = ["superó a", "venció a", "derrotó a", "se impuso ante"]
            v = random.choice(verbos)
            cuerpo = f"{arg_nom} {v} {riv_nom} {riv_flag} por {marcador_narrativo} {ronda_txt}."
            remate = random.choice(remates) + f" {tag_torneo}"
            
        else: # Derrota
            if es_final:
                titulares = [
                    f"SUBCAMPEÓN TRAS UNA GRAN SEMANA 🇦🇷",
                    f"NO PUDO SER EN LA FINAL 🇦🇷👏"
                ]
                remates = [
                    "Se escapó el título por poco, pero enorme torneo. ¡Cabeza arriba! 👏🇦🇷",
                    "Gran semana llegando al último día de competencia. ¡A seguir! 💪🇦🇷"
                ]
            else:
                titulares = [
                    f"BATALLÓ PERO NO ALCANZÓ 🇦🇷",
                    f"PASO EN FALSO EN {torneo.upper()} 🇦🇷",
                    f"FIN DEL TORNEO PARA {arg_nom.upper()} 🇦🇷"
                ]
                remates = [
                    "A levantar cabeza y recargar pilas para el próximo torneo. 💪🇦🇷",
                    "Se luchó hasta el final pero no se pudo dar. ¡Siempre bancando! 🇦🇷",
                    "Cierra su participación en el certamen. ¡A pensar en lo que viene! 🎾🇦🇷"
                ]
                
            titular = random.choice(titulares)
            cuerpo = f"{arg_nom} cayó ante {riv_nom} {riv_flag} por {marcador_narrativo} {ronda_txt}."
            remate = random.choice(remates) + f" {tag_torneo}"

        tweet_texto = f"{titular}\n\n{cuerpo}\n\n{remate}"
        return [f"--- INICIO TWEET ---\n{tweet_texto.strip()}\n--- FIN TWEET ---"]

    # -------------------------------------------------------------
    # CASO 2: MÚLTIPLES PARTIDOS (Resumen Compacto de la Jornada)
    # -------------------------------------------------------------
    rondas_presentes = {traducir_ronda(p.get('tournament_round', '')) for p in partidos if p.get('tournament_round')}
    
    if "Final" in rondas_presentes:
        encabezado = f"🏆 Resultados de las FINALES {frases['en']}: 🇦🇷"
    elif "Semifinales" in rondas_presentes or "Semis" in rondas_presentes:
        encabezado = f"Resultados de Semifinales {frases['en']}: 🇦🇷"
    elif "Cuartos de final" in rondas_presentes or "Cuartos" in rondas_presentes:
        encabezado = f"Resultados de Cuartos de final {frases['en']}: 🇦🇷"
    else:
        encabezados_resumen = [
            f"🇦🇷 Resultados de hoy {frases['en']}:",
            f"🇦🇷 Así le fue a los argentinos hoy {frases['en']}:",
            f"🇦🇷 Balance del día {frases['en']}:"
        ]
        encabezado = random.choice(encabezados_resumen)

    lineas_partidos = []
    total_victorias = 0
    total_derrotas = 0

    for p in partidos:
        info = p.get('arg_info', {})
        pais1 = info.get('jugador_1', {}).get('pais', '')
        pais2 = info.get('jugador_2', {}).get('pais', '')
        
        j1_nom = obtener_nombre_variante(p.get('event_first_player'))
        j2_nom = obtener_nombre_variante(p.get('event_second_player'))
        flag1 = obtener_bandera(pais1)
        flag2 = obtener_bandera(pais2)
        
        ganador = determinar_ganador_partido(p)
        tipo_fin = detectar_tipo_finalizacion(p)
        
        scores_api = p.get('scores', [])
        marcador = formatear_sets(scores_api, invertir=(ganador == 2)) or p.get('event_final_result', '')
        if str(marcador).strip() in ('0-0', '0 - 0', ''):
            marcador = ""
        marcador_str = f" ({marcador})" if marcador else ""
        
        ronda_corta = traducir_ronda(p.get('tournament_round', ''), corto=True)
        ronda_tag = f" en {ronda_corta}" if ronda_corta else ""
        
        if es_derbi_argentino(pais1, pais2):
            winner_nom = j1_nom if ganador == 1 else j2_nom
            loser_nom = j2_nom if ganador == 1 else j1_nom
            if tipo_fin == 'walkover':
                line = f"🇦🇷 DERBI: {winner_nom} avanzó por Walkover (W.O.) ante {loser_nom}{ronda_tag}."
            elif tipo_fin == 'retiro':
                line = f"🇦🇷 DERBI: {winner_nom} avanzó tras retiro de {loser_nom}{marcador_str}{ronda_tag}."
            else:
                line = f"🇦🇷 DERBI: {winner_nom} superó a {loser_nom} por {marcador}{ronda_tag}."
        else:
            j1_es_arg = info.get('jugador_1', {}).get('es_arg', False)
            arg_nom = j1_nom if j1_es_arg else j2_nom
            riv_nom = j2_nom if j1_es_arg else j1_nom
            riv_flag = flag2 if j1_es_arg else flag1
            gano = (ganador == 1) if j1_es_arg else (ganador == 2)
            
            if gano:
                total_victorias += 1
                if tipo_fin == 'walkover':
                    line = f"✅ {arg_nom} avanzó por Walkover (W.O.) ante {riv_nom} {riv_flag}{ronda_tag}."
                elif tipo_fin == 'retiro':
                    line = f"✅ {arg_nom} avanzó por retiro de {riv_nom} {riv_flag}{marcador_str}{ronda_tag}."
                else:
                    line = f"✅ {arg_nom} venció a {riv_nom} {riv_flag} por {marcador}{ronda_tag}."
            else:
                total_derrotas += 1
                if tipo_fin == 'walkover':
                    line = f"❌ {arg_nom} no pudo presentarse (Walkover) ante {riv_nom} {riv_flag}{ronda_tag}."
                elif tipo_fin == 'retiro':
                    line = f"❌ {arg_nom} se retiró ante {riv_nom} {riv_flag}{marcador_str}{ronda_tag}."
                else:
                    line = f"❌ {arg_nom} cayó ante {riv_nom} {riv_flag} por {marcador}{ronda_tag}."

        lineas_partidos.append(line.strip())

    # Cierres acordes al balance de la jornada
    if total_victorias > 0 and total_derrotas == 0:
        cierres = [
            f"¡Jornada perfecta para el tenis argentino! 🇦🇷🔥 {tag_torneo}",
            f"¡Pleno de triunfos hoy! A seguir con todo. 🇦🇷💪 {tag_torneo}",
            f"Gran día para los nuestros. ¡Vamos por más! 👏 {tag_torneo}"
        ]
    elif total_victorias == 0 and total_derrotas > 0:
        cierres = [
            f"Día difícil en los resultados, pero siempre bancando a los nuestros 🇦🇷 {tag_torneo}",
            f"A recargar energías para lo que viene. ¡Fuerza muchachos! 💪🇦🇷 {tag_torneo}",
            f"No fue la mejor jornada, a levantar cabeza. 🇦🇷 {tag_torneo}"
        ]
    else:
        cierres = [
            f"Jornada intensa para la legión. Mañana continúa la acción. 🍿🇦🇷 {tag_torneo}",
            f"Con una de cal y una de arena, así cerramos la jornada. 🇦🇷 {tag_torneo}",
            f"Balance del día en la cancha. ¡A seguir metiendo! 🇦🇷💪 {tag_torneo}"
        ]

    return _formatear_en_hilo(encabezado, lineas_partidos, cierres)


# ==============================================================================
# BLOQUE 4: RANKINGS ATP / WTA
# ==============================================================================

def generar_tweet_ranking(datos, tipo="atp"):
    """Genera un tweet con el Top 10 del ranking con tipografía limpia."""
    top_10 = datos[:10]
    cat_str = tipo.upper()
    
    encabezados = [
        f"📊 Top 10 Ranking {cat_str} esta semana:",
        f"🎾 Así quedó el nuevo Top 10 del mundo ({cat_str}):",
        f"Top 10 Ranking {cat_str}:"
    ]
    
    lineas = [random.choice(encabezados), ""]
    
    for p in top_10:
        pos = p.get('place', p.get('player_place'))
        nombre_completo = p.get('player', p.get('player_name', ''))
        
        # Apellido o nombre corto para que entre prolijo
        partes = nombre_completo.split()
        nombre_corto = " ".join(partes[1:]) if len(partes) > 1 else nombre_completo
        
        pais = p.get('country', p.get('player_country'))
        flag = obtener_bandera(pais)
        puntos = p.get('points', p.get('player_points'))
        
        lineas.append(f"{pos}. {nombre_corto} {flag} ({puntos} pts)")
    
    lineas.append("")
    lineas.append(f"#{cat_str}Ranking #Tenis")
    
    texto = "\n".join(lineas)
    return f"--- INICIO TWEET ---\n{texto}\n--- FIN TWEET ---"


def generar_hilo_ranking_argentinos(datos, tipo="atp"):
    """
    Genera un hilo de tweets con las posiciones de los argentinos en el ranking.
    """
    cat_str = tipo.upper()
    argentinos = [p for p in datos if p.get('country', p.get('player_country', '')).lower() in ['argentina', 'arg']]
    
    try:
        argentinos.sort(key=lambda x: int(x.get('place', x.get('player_place', 9999))))
    except Exception:
        pass
        
    if not argentinos:
        return ["--- INICIO TWEET ---\nNo se encontraron jugadores argentinos en el ranking hoy. 🇦🇷\n--- FIN TWEET ---"]

    encabezados = [
        f"🇦🇷 Así arrancan la semana los argentinos en el Ranking {cat_str}:",
        f"🇦🇷 Posiciones de los argentinos en el Ranking {cat_str}:",
        f"🇦🇷 Ranking {cat_str}: Los tenistas nacionales esta semana:"
    ]
    
    header = random.choice(encabezados) + "\n\n"
    tweets = []
    current_text = header
    
    for p in argentinos:
        pos = p.get('place', p.get('player_place'))
        nombre = p.get('player', p.get('player_name'))
        puntos = p.get('points', p.get('player_points'))
        linea = f"• {pos}. {nombre} ({puntos} pts)\n"
        
        if len(current_text) + len(linea) > 250:
            tweets.append(current_text.strip())
            current_text = f"({len(tweets) + 1}/?) Sigue el ranking: 👇\n\n" + linea
        else:
            current_text += linea
            
    tweets.append(current_text.strip())
    
    total_tweets = len(tweets)
    hilo_final = []
    
    for idx, t in enumerate(tweets):
        if total_tweets > 1:
            texto_tweet = t.replace("/?", f"/{total_tweets}")
            if idx == 0 and f"(1/{total_tweets})" not in texto_tweet:
                texto_tweet += f"\n\n(1/{total_tweets}) 🧵"
        else:
            texto_tweet = t
            
        hilo_final.append(f"--- TWEET {idx+1} ---\n{texto_tweet}\n--- FIN TWEET ---")
        
    return hilo_final
