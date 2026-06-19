import random
import re

def obtener_bandera(pais):
    """Devuelve el emoji de la bandera para un país dado."""
    if not pais: return ""
    
    p = pais.lower().strip()
    mapping = {
        "argentina": "🇦🇷",
        "spain": "🇪🇸", "españa": "🇪🇸",
        "usa": "🇺🇸", "united states": "🇺🇸",
        "italy": "🇮🇹", "italia": "🇮🇹",
        "france": "🇫🇷", "francia": "🇫🇷",
        "germany": "🇩🇪", "alemania": "🇩🇪",
        "brazil": "🇧🇷", "brasil": "🇧🇷",
        "chile": "🇨🇱",
        "uruguay": "🇺🇾",
        "colombia": "🇨🇴",
        "peru": "🇵🇪",
        "ecuador": "🇪🇨",
        "mexico": "🇲🇽",
        "great britain": "🇬🇧", "united kingdom": "🇬🇧",
        "australia": "🇦🇺",
        "serbia": "🇷🇸",
        "croatia": "🇭🇷",
        "russia": "🇷🇺",
        "greece": "🇬🇷",
        "poland": "🇵🇱",
        "kazakhstan": "🇰🇿",
        "canada": "🇨🇦",
        "japan": "🇯🇵",
        "china": "🇨🇳",
        "czech republic": "🇨🇿",
        "switzerland": "🇨🇭",
        "austria": "🇦🇹",
        "belgium": "🇧🇪",
        "netherlands": "🇳🇱",
        "norway": "🇳🇴",
        "denmark": "🇩🇰",
        "bulgaria": "🇧🇬",
        "hungary": "🇭🇺",
        "portugal": "🇵🇹",
        "ukraine": "🇺🇦",
        "belarus": "🇧🇾",
        "slovakia": "🇸🇰",
        "slovenia": "🇸🇮",
        "sweden": "🇸🇪",
        "romania": "🇷🇴",
        "neutral": "🏳️",
        "ana": "🏳️",
        "itf": "🏳️"
    }
    return mapping.get(p, "")


def es_derbi_argentino(pais1, pais2):
    """Devuelve True si ambos países son Argentina (derbi argentino)."""
    p1 = (pais1 or '').lower().strip()
    p2 = (pais2 or '').lower().strip()
    return p1 in ("argentina", "arg") and p2 in ("argentina", "arg")


def obtener_nombre_variante(nombre_original):
    """
    Busca si el jugador es un argentino conocido y devuelve una variante aleatoria de su nombre.
    Si no se encuentra en el mapa, devuelve el nombre original.
    """
    if not nombre_original:
        return ""
        
    # Normalización básica para la comparación
    import unicodedata
    def normalizar(t):
        return "".join(
            c for c in unicodedata.normalize('NFD', t.lower())
            if unicodedata.category(c) != 'Mn'
        ).strip()
        
    norm_orig = normalizar(nombre_original)
    
    # Mapa de jugadores argentinos conocidos con sus variantes de nombres/apodos
    variantes_jugadores = {
        # Francisco Cerúndolo
        "francisco cerundolo": [
            "Fran Cerúndolo", "Fran", "Cerúndolo","@FranCerundolo"
        ],
        "f. cerundolo": [
            "Fran Cerúndolo", "Fran", "Cerúndolo","@FranCerundolo"
        ],
        
        # Sebastián Báez
        "sebastian baez": [
            "Seba Báez", "Báez","@sebaabaez7"
        ],
        "s. baez": [
            "Seba Báez", "Báez","@sebaabaez7"
        ],
        
        # Tomás Martín Etcheverry
        "tomas martin etcheverry": [
            "Tomi Etcheverry", "Etcheverry", "Tomi", "El Retu","@tometcheverry"
        ],
        "tomas etcheverry": [
            "Tomi Etcheverry", "Etcheverry", "Tomi", "El Retu","@tometcheverry"
        ],
        "t. m. etcheverry": [
            "Tomi Etcheverry", "Etcheverry", "Tomi","@tometcheverry"
        ],
        
        # Mariano Navone
        "mariano navone": [
            "Mariano Navone", "La Navoneta", "Navone","La Nave","@marianonavone1"
        ],
        "m. navone": [
            "Mariano Navone", "La Navoneta", "Navone","La Nave","@marianonavone1"
        ],
        
        # Facundo Díaz Acosta
        "facundo diaz acosta": [
            "Facu Díaz Acosta", "Díaz Acosta", "Facu","@facudiazacosta"
        ],
        "f. diaz acosta": [
            "Facu Díaz Acosta", "Díaz Acosta", "Facu","@facudiazacosta"
        ],
        
        # Camilo Ugo Carabelli
        "camilo ugo carabelli": [
            "Camilo Ugo", "El Brujo Carabelli", "Carabelli", "Camilo Carabelli", "El Brujo","@camilougo"
        ],
        "c. ugo carabelli": [
            "Camilo Ugo", "El Brujo Carabelli", "Carabelli", "Camilo Carabelli", "El Brujo","@camilougo"
        ],
        
        # Federico Coria
        "federico coria": [
            "Fede Coria", "Coria", "La Mojarra","@fedeecoria"
        ],
        "f. coria": [
            "Fede Coria", "Coria", "La Mojarra","@fedeecoria"
        ],
        
        # Facundo Bagnis
        "facundo bagnis": [
            "Facu Bagnis", "Bagnis","@facubagnis"
        ],
        "f. bagnis": [
            "Facu Bagnis", "Bagnis","@facubagnis"
        ],
        
        # Thiago Agustín Tirante
        "thiago agustin tirante": [
            "Thiago Tirante", "Tirante", "@TiranteThiago"
        ],
        "thiago tirante": [
            "Thiago Tirante", "Tirante", "@TiranteThiago"
        ],
        "t. tirante": [
            "Thiago Tirante", "Tirante", "@TiranteThiago"
        ],
        
        # Juan Manuel Cerúndolo
        "juan manuel cerundolo": [
            "Juanma Cerúndolo", "@jmcerundolo"
        ],
        "j. cerundolo": [
            "Juanma Cerúndolo", "@jmcerundolo"
        ],
        "j. m. cerundolo": [
            "Juanma Cerúndolo", "@jmcerundolo"
        ],
        
        # Nadia Podoroska
        "nadia podoroska": [
            "Nadia Podoroska", "La Rusa Podoroska", "La Rusa", "@nadiapodoroska"
        ],
        "n. podoroska": [
            "Nadia Podoroska", "La Rusa Podoroska", "La Rusa", "@nadiapodoroska"
        ],
        
        # Lourdes Carlé
        "lourdes carle": [
            "Lourdes Carlé", "Carlé", "@LourdesCarle"
        ],
        "l. carle": [
            "Lourdes Carlé", "Carlé", "@LourdesCarle"
        ],
        
        # Julia Riera
        "julia riera": [
            "Juli Riera", "Riera", "@juliriera02"
        ],
        "j. riera": [
            "Juli Riera", "Riera", "@juliriera02"
        ],
        
        # Solana Sierra
        "solana sierra": [
            "Soli Sierra", "Solana", "Solana Sierra"
        ],
        "s. sierra": [
            "Soli Sierra", "Solana", "Solana Sierra"
        ],

        #Mariano Kestelboim
        "mariano kestelboim": [
            "Mariano Kestelboim", "Kestelboim", "@mkestelboim"
        ],
        "m. kestelboim": [
            "Mariano Kestelboim", "Kestelboim", "@mkestelboim"
        ],

        #Jazmin Ortenzi
        "jazmin ortenzi": [
            "Jazmin Ortenzi", "Jaz Ortenzi", "@JazOrtenzi"
        ],
        "j. ortenzi": [
            "Jazmin Ortenzi", "Jaz Ortenzi", "@JazOrtenzi"
        ],

        #Francisco Comesaña
        "francisco comesaña": [
            "Francisco Comesaña", "Comesaña", "Fran Comesaña", "@fran_comesana"
        ],
        "f. comesaña": [
            "Francisco Comesaña", "Comesaña", "Fran Comesaña", "@fran_comesana"
        ],
        "francisco comesana":[
            "Francisco Comesaña", "Comesaña", "Fran Comesaña", "@fran_comesana"
        ],
        "f. comesana":[
            "Francisco Comesaña", "Comesaña", "Fran Comesaña", "@fran_comesana"
        ],

        #Federico Gomez
        "federico gomez": [
            "Federico Gomez", "Gomez", "Fede Gomez"
        ],
        "f. gomez": [
            "Federico Gomez", "Gomez", "Fede Gomez"
        ],
        "f. a. gomez": [
            "Federico Gomez", "Gomez", "Fede Gomez"
        ],

        #Juan Pablo Ficovich
        "juan pablo ficovich": [
            "Juan Ficovich", "Ficovich", "@juampificovich", "Juampi Ficovich"
        ],
        "j. p. ficovich": [
            "Juan Ficovich", "Ficovich", "@juampificovich", "Juampi Ficovich"
        ],

        #Lautaro Midon
        "lautaro midon": [
            "Lautaro Midon", "Midon", "@Lautaromidonn"
        ],
        "l. midon": [
            "Lautaro Midon", "Midon", "@Lautaromidonn"
        ],

        #Alberto Olivieri Genaro
        "alberto olivieri genaro": [
            "Gena Olivieri", "Olivieri", "@GenaOlivieri4"
        ],
        "a. olivieri genaro": [
            "Gena Olivieri", "Olivieri", "@GenaOlivieri4"
        ],
        "a. o. genaro": [
            "Gena Olivieri", "Olivieri", "@GenaOlivieri4"
        ],

        #Bautista Torres Juan
        "bautista torres juan": [
            "Bauti Torres", "Torres", "@_BautiTorres"
        ],
        "b. torres juan": [
            "Bauti Torres", "Torres", "@_BautiTorres"
        ],
        "b. t. juan": [
            "Bauti Torres", "Torres", "@_BautiTorres"
        ],
        "bautista torres j": [
            "Bauti Torres", "Torres", "@_BautiTorres"
        ],
        "b. torres j": [
            "Bauti Torres", "Torres", "@_BautiTorres"
        ],
        "b. t. j": [
            "Bauti Torres", "Torres", "@_BautiTorres"
        ],

        #Manuel La Serna Juan
        "manuel la serna juan": [
            "Manuel La Serna", "La Serna", "@manulaserna3", "Manu La Serna"
        ],
        "m. la serna juan": [
            "Manuel La Serna", "La Serna", "@manulaserna3", "Manu La Serna"
        ],
        "m. l. s. juan": [
            "Manuel La Serna", "La Serna", "@manulaserna3", "Manu La Serna"
        ],
        "manuel la serna j": [
            "Manuel La Serna", "La Serna", "@manulaserna3", "Manu La Serna"
        ],
        "m. la serna j": [
            "Manuel La Serna", "La Serna", "@manulaserna3", "Manu La Serna"
        ],
        "j. m. La Serna": [
            "Manuel La Serna", "La Serna", "@manulaserna3", "Manu La Serna"
        ],

        #Benjamin Chelia
        "benjamin chelia": [
            "Benja Chelia","Benjamin Chelia", "Chelia", "@benja_chelia"
        ],
        "b. chelia": [
            "Benja Chelia","Benjamin Chelia", "Chelia", "@benja_chelia"
        ],

        #Facundo Mena
        "facundo mena": [
            "Facu Mena","Facundo Mena", "Mena", "@menafacundo"
        ],
        "f. mena": [
            "Facu Mena","Facundo Mena", "Mena", "@menafacundo"
        ],

        #Santiago Rodriguez Taverna
        "santiago rodriguez taverna": [
            "Santi Taverna", "Santiago Taverna", "Taverna", "@santyelduke",
        ],
        "s. rodriguez taverna": [
            "Santi Taverna", "Santiago Taverna", "Taverna", "@santyelduke"
        ],
        "s. r. t": [
            "Santi Taverna", "Santiago Taverna", "Taverna", "@santyelduke"
        ],

        #Gonzalo Villanueva
        "gonzalo villanueva": [
            "Gonza Villanueva", "Gon Villanueva", "@gon_villanueva"
        ],
        "g. villanueva": [
            "Gonza Villanueva", "Gon Villanueva", "@gon_villanueva"
        ],
        "g. v": [
            "Gonza Villanueva", "Gon Villanueva", "@gon_villanueva"
        ],

        #Emanuel Ambrogi Luciano
        "emanuel ambrogi luciano": [
            "Lucho Ambrogi", "Luciano Ambrogi", "Ambrogi", "@ambrogi_lucho"
        ],
        "e. ambrogi luciano": [
            "Lucho Ambrogi", "Luciano Ambrogi", "Ambrogi", "@ambrogi_lucho"
        ],
        "e. a. luciano": [
            "Lucho Ambrogi", "Luciano Ambrogi", "Ambrogi", "@ambrogi_lucho"
        ],
        "emanuel ambrogi l": [
            "Lucho Ambrogi", "Luciano Ambrogi", "Ambrogi", "@ambrogi_lucho"
        ],
        "e. ambrogi l": [
            "Lucho Ambrogi", "Luciano Ambrogi", "Ambrogi", "@ambrogi_lucho"
        ],
        "e. a. l": [
            "Lucho Ambrogi", "Luciano Ambrogi", "Ambrogi", "@ambrogi_lucho"
        ],

        #Giovannini Lu

        "L. Giovannini": [
            "L. Giovannini", "Lu Giovannini", "@lulu_giova06",
        ]        
    }
    
    # Intento de coincidencia exacta en el diccionario
    if norm_orig in variantes_jugadores:
        return random.choice(variantes_jugadores[norm_orig])
        
    # Intento de coincidencia por sub-cadena (por si el nombre viene ligeramente diferente de la API)
    for clave, variantes in variantes_jugadores.items():
        if clave in norm_orig or norm_orig in clave:
            return random.choice(variantes)
            
    # Si no es un argentino conocido, devolvemos el original
    return nombre_original


def traducir_estado_en_vivo(estado_api):
    """Traduce el estado del partido en vivo al español para hacerlo más amigable."""
    if not estado_api: return ""
    est = str(estado_api).lower().strip()
    
    if "1st set" in est: return "1er Set"
    if "2nd set" in est: return "2do Set"
    if "3rd set" in est: return "3er Set"
    if "4th set" in est: return "4to Set"
    if "5th set" in est: return "5to Set"
    if "delayed" in est: return "Demorado"
    if "suspended" in est: return "Suspendido"
    if "interrupted" in est: return "Interrumpido"
    if "medical" in est or "med" in est: return "Médico"
    
    return estado_api


def _formatear_jugador_completo(nombre, bandera, ranking_str):
    """
    Formatea el nombre del jugador junto con su bandera y ranking,
    evitando espacios consecutivos si alguno de estos datos es nulo o vacío.
    """
    # Primero buscamos si tiene una variante/apodo dinámico
    nombre_apodo = obtener_nombre_variante(nombre)
    
    partes = [nombre_apodo.strip()]
    if bandera and bandera.strip():
        partes.append(bandera.strip())
    if ranking_str and ranking_str.strip():
        partes.append(ranking_str.strip())
    return " ".join(partes)

def formatear_sets(scores):
    """
    Convierte la lista de scores de la API en un string legible de games por set.
    Maneja el caso de tiebreaks donde la API devuelve decimales (ej: 7.9 -> 7).
    """
    if not scores or not isinstance(scores, list):
        return ""
    
    sets = []
    for s in scores:
        # Tomamos solo la parte entera antes del punto decimal si existe
        s1 = str(s.get('score_first', '0')).split('.')[0]
        s2 = str(s.get('score_second', '0')).split('.')[0]
        
        # Evitar agregar sets vacíos (0-0) si ya tenemos sets cargados
        if s1 == '0' and s2 == '0' and len(sets) > 0:
            continue
            
        sets.append(f"{s1}-{s2}")
    
    return " / ".join(sets)

def extraer_categoria(partido):
    """Extrae la categoría del torneo (ATP, WTA, Challenger, ITF) buscando en los nombres."""
    name = partido.get('tournament_name', '').upper()
    etype = partido.get('event_type_type', '').upper()
    full = f"{name} {etype}"
    
    if "ATP" in full: return "ATP"
    if "WTA" in full: return "WTA"
    if "CHALLENGER" in full: return "Challenger"
    if "ITF" in full: return "ITF"
    return ""

def traducir_ronda(ronda_api):
    """Traduce la ronda del torneo proveniente de la API al español."""
    if not ronda_api: return ""
    r = str(ronda_api).lower()
    
    if "final" in r and "quarter" not in r and "semi" not in r and "1/" not in r: return "Final"
    if "semi" in r: return "Semifinal"
    if "quarter" in r: return "4tos"
    if "1/8" in r: return "8vos"
    if "1/16" in r: return "16avos"
    if "1/32" in r: return "32avos"
    if "1/64" in r: return "64avos"
    
    # Qualy: detecta el número de ronda si está presente (ej: "Qualifying Round 2" → "R2 Qualy")
    if "qualif" in r or "qualy" in r:
        match = re.search(r'\d+', r)
        if match:
            return f"R{match.group()} Qualy"
        return "Qualy"
    
    # Si contiene round pero ninguna de las anteriores (ej: "Round 1")
    if "round" in r:
        return "Ronda"
        
    return ""

def traducir_nombre_torneo(nombre):
    """Traduce nombres de torneos de inglés a español para el público argentino."""
    nombre_low = nombre.lower()
    
    # Preservar si era Junior
    tiene_junior = "junior" in nombre_low
    
    # Mapeo específico de ATP 1000 y otros comunes
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
    """Mapea nombres de torneos a sus hashtags oficiales o genera uno genérico incluyendo la categoría."""
    nombre = nombre_torneo.lower()
    
    # Mapeo de torneos importantes (estos tienen prioridad)
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
            
    # Tomar solo la primera parte si hay una coma (ej: "Boca Raton, FL 3" -> "Boca Raton")
    nombre_base = nombre_torneo.split(',')[0]
    
    # Limpieza de prefijos para el hashtag (ej: "ITF W35 Boca Raton" -> "BocaRaton")
    # Removemos ITF, ATP, WTA, Challenger y categorías como M15, W35, etc.
    nombre_sin_prefijo = re.sub(r'^(ITF|ATP|WTA|Challenger|M\d+|W\d+)\s+', '', nombre_base, flags=re.IGNORECASE).strip()
    
    # Si al limpiar queda vacío (ej: solo decía "Challenger"), volvemos al base
    if not nombre_sin_prefijo:
        nombre_sin_prefijo = nombre_base
        
    # Generar hashtag genérico quitando espacios y caracteres especiales
    nombre_final = "".join(char for char in nombre_sin_prefijo if char.isalnum())
    
    # Agregar la categoría al inicio si está presente (ej: ATP, Challenger, ITF, WTA)
    if categoria:
        cat_clean = str(categoria).strip()
        if not nombre_final.lower().startswith(cat_clean.lower()):
            nombre_final = cat_clean + nombre_final
            
    return "#" + nombre_final

def analizar_resultado_argentino(partido):
    """
    Analiza si el argentino ganó o perdió y con qué intensidad.
    Devuelve un mensaje corto.
    """
    arg_info = partido.get('arg_info', {})
    j1_es_arg = arg_info.get('jugador_1', {}).get('es_arg', False)
    j2_es_arg = arg_info.get('jugador_2', {}).get('es_arg', False)
    
    # Marcador de sets (ej: "2 - 1")
    final_res = partido.get('event_final_result', "0 - 0")
    try:
        s1, s2 = map(int, final_res.split(" - "))
    except:
        s1, s2 = 0, 0
        
    # Ganador 1 o 2
    ganador = 1 if s1 > s2 else (2 if s2 > s1 else 0)
    
    status = partido.get('event_status', '').lower()
    nombre_j1 = partido.get('event_first_player', 'Rival')
    nombre_j2 = partido.get('event_second_player', 'Rival')
    
    # Detección de Retiros y Walkovers
    es_retiro = status in ['retired', 'walkover', 'w.o.', 'ret.'] or 'retired' in status or 'walkover' in status
    tipo_retiro = "retiro" if ("ret" in status or "retired" in status) else "W.O."
    
    if es_retiro:
        if j1_es_arg:
            if ganador == 1:
                return f"Victoria por {tipo_retiro} de {nombre_j2}", True
            else:
                return f"Derrota por {tipo_retiro} de {nombre_j1}", False
        if j2_es_arg:
            if ganador == 2:
                return f"Victoria por {tipo_retiro} de {nombre_j1}", True
            else:
                return f"Derrota por {tipo_retiro} de {nombre_j2}", False
    
    ronda = traducir_ronda(partido.get('tournament_round', ''))
    es_qualy = partido.get('es_qualy', False)
    es_final = (ronda == "Final" and not es_qualy)

    if es_final:
        mensajes_victoria_ajustada = [
            "¡CAMPEÓN! 🏆🇦🇷", "¡Se consagró campeón tras un partidazo! 🏆", 
            "¡El título es argentino! 🏆🇦🇷", "¡Levanta el trofeo y grita campeón! 🏆🇦🇷"
        ]
        mensajes_victoria_facil = [
            "¡CAMPEÓN INDISCUTIDO! 🏆🇦🇷", "¡Masterclass y título a casa! 🏆", 
            "¡Dominio total en la final para gritar campeón! 🏆🇦🇷","Cátedra de tenis"
        ]
        mensajes_derrota_ajustada = [
            "Se escapó la final por muy poco 🇦🇷", "Gran torneo, lástima el final.", 
            "No pudo consagrarse 🇦🇷", "Cierra una gran semana como finalista 🇦🇷"
        ]
        mensajes_derrota_facil = [
            "No encontró el ritmo en el partido 😕", 
            "Dura derrota, no pudo consagrarse campeón hoy 🇦🇷", "A levantar cabeza, gran semana llegando a la final 🇦🇷"
        ]
    else:
        # Mensajes regulares
        mensajes_victoria_ajustada = [
            "¡VAMOS! 🇦🇷", "¡Triunfazo peleado!", "Se sufrió pero se ganó. 💪", 
            "¡Partidazo y victoria! ", "¡Lo dio vuelta y festejó! 🇦🇷", "¡Qué huevo!"
        ]
        mensajes_victoria_facil = [
            "¡Cátedra de tenis! ", "¡Masterclass en la cancha!", "¡Paliza! Imparable hoy. 💪",
            "¡Paso firme y a la siguiente ronda! 🇦🇷", "¡Adentro! Vamos por más.", "Sin despeinarse. "
        ]
        mensajes_derrota_ajustada = [
            "Una lástima, se escapó por poco.", "Casi se da, gran esfuerzo.", "Se luchó hasta el final 🇦🇷",
            "Mala suerte en esta.", "Se escapó en el cierre, una pena.", "A levantar cabeza, fue un partidazo."
        ]
        mensajes_derrota_facil = [
            "No pudo ser esta vez", "Dura derrota 🇦🇷", "La tuvo complicada hoy 😕",
            "No encontró el ritmo hoy 🇦🇷", "A pensar en el próximo torneo 😕"
        ]
    
    # Caso 1: Jugador 1 es el argentino
    if j1_es_arg:
        if ganador == 1:
            if s2 >= 1: # Ganó 2-1 o similar
                return random.choice(mensajes_victoria_ajustada), True
            else: # Ganó 2-0 o similar
                return random.choice(mensajes_victoria_facil), True
        elif ganador == 2:
            if s1 >= 1: # Perdió 1-2
                return random.choice(mensajes_derrota_ajustada), False
            else: # Perdió 0-2
                return random.choice(mensajes_derrota_facil), False
                
    # Caso 2: Jugador 2 es el argentino
    if j2_es_arg:
        if ganador == 2:
            if s1 >= 1: # Ganó 2-1
                return random.choice(mensajes_victoria_ajustada), True
            else: # Ganó 2-0
                return random.choice(mensajes_victoria_facil), True
        elif ganador == 1:
            if s2 >= 1: # Perdió 1-2
                return random.choice(mensajes_derrota_ajustada), False
            else: # Perdió 0-2
                return random.choice(mensajes_derrota_facil), False
                
    return "", None

def _formatear_en_hilo(encabezado, lineas_items, cierres, max_chars=280):
    """
    Toma un encabezado, una lista de líneas (partidos) y una lista de posibles cierres.
    Divide el contenido en múltiples bloques (tweets) si excede el límite de caracteres.
    Retorna una lista de strings con el formato --- INICIO TWEET --- ... --- FIN TWEET ---.
    """
    cierre = random.choice(cierres)
    margen_hilo = 10
    limite = max_chars - margen_hilo
    
    tweets_raw = []
    current_text = encabezado + "\n\n"
    
    for linea in lineas_items:
        if len(current_text) + len(linea) + 1 > limite:
            tweets_raw.append(current_text.strip())
            current_text = "Sigue la lista: 👇\n\n" + linea + "\n"
        else:
            current_text += linea + "\n"
            
    if len(current_text) + len(cierre) + 2 > limite:
        tweets_raw.append(current_text.strip())
        current_text = cierre
    else:
        current_text += "\n" + cierre
        
    tweets_raw.append(current_text.strip())
    
    total_tweets = len(tweets_raw)
    hilo_final = []
    for idx, t in enumerate(tweets_raw):
        texto_final = t
        if total_tweets > 1:
            texto_final += f"\n\n({idx+1}/{total_tweets}) 🧵"
        hilo_final.append(f"--- INICIO TWEET ---\n{texto_final}\n--- FIN TWEET ---")
        
    return hilo_final

def obtener_frases_torneo(torneo_original, partidos):
    """
    Retorna preposiciones y nombres pulidos para el torneo,
    manejando correctamente Grand Slams (sin ATP/WTA) y la Qualy.
    """
    torneo = traducir_nombre_torneo(torneo_original)
    cat = extraer_categoria(partidos[0])
    
    es_gs = any(gs in torneo.lower() for gs in ["roland garros", "wimbledon", "us open", "australian open"])
    todos_qualy = all(p.get('es_qualy') for p in partidos)
    
    frases = {}
    
    if es_gs:
        # Grand Slams
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
                frases["nombre"] = torneo
            else:
                # Roland Garros, Wimbledon
                frases["en"] = f"en {torneo}"
                frases["del"] = f"de {torneo}"
                frases["al"] = f"a {torneo}"
                frases["nombre"] = torneo
    else:
        # ATP, WTA, Challenger, ITF, etc.
        prefijo = f"{cat} " if cat else ""
        if todos_qualy:
            conector = "del " if cat else "de "
            frases["en"] = f"en la Qualy {conector}{prefijo}{torneo}"
            frases["del"] = f"de la Qualy {conector}{prefijo}{torneo}"
            frases["al"] = f"a la Qualy {conector}{prefijo}{torneo}"
            frases["nombre"] = f"la Qualy {conector}{prefijo}{torneo}"
        else:
            frases["en"] = f"en el {prefijo}{torneo}"
            frases["del"] = f"del {prefijo}{torneo}"
            frases["al"] = f"al {prefijo}{torneo}"
            frases["nombre"] = f"{prefijo}{torneo}"
            
    return frases

def generar_tweet_agenda(torneo_original, partidos):
    """Genera el texto para un tweet de agenda con categoría y hashtag."""
    torneo = traducir_nombre_torneo(torneo_original)
    cat = extraer_categoria(partidos[0])
    tag_torneo = obtener_hashtag_torneo(torneo, cat)
    frases = obtener_frases_torneo(torneo_original, partidos)
    
    rondas_presentes = set()
    for p in partidos:
        r = traducir_ronda(p.get('tournament_round', ''))
        if r:
            rondas_presentes.add(r)
            
    # ¿Son todos los partidos de qualy?
    todos_qualy = all(p.get('es_qualy') for p in partidos)
            
    if "Final" in rondas_presentes:
        encabezados = [
            f"🏆 ¡Día de FINAL {frases['en']}! 🇦🇷",
            f"Se juega la gran final {frases['del']}: 🇦🇷🏆",
            f"¡Llegó el día! Hoy es la final {frases['del']}: 🇦🇷",
            f"Día de coronación {frases['en']}. Juegan: 🇦🇷"
        ]
    elif "Semifinal" in rondas_presentes:
        encabezados = [
            f"Estos son los horarios de las semifinales {frases['en']}: 🇦🇷",
            f"¡Día de Semis {frases['en']}! Juegan los nuestros: 🇦🇷",
            f"Buscando el pase a la final hoy {frases['en']}: 🇦🇷"
        ]
    elif "4tos" in rondas_presentes:
        encabezados = [
            f"Día de 4tos {frases['en']}: 🇦🇷",
            f"¡4tos a la vista {frases['en']}! Juegan: 🇦🇷",
            f"Por un lugar en semis {frases['del']}: 🇦🇷"
        ]
    elif "8vos" in rondas_presentes:
        encabezados = [
            f"Día de 8vos {frases['en']}: 🇦🇷",
            f"Buscando meterse entre los 8 mejores {frases['del']}: 🇦🇷"
        ]
    elif todos_qualy or "Qualy" in rondas_presentes or any("qualy" in r.lower() for r in rondas_presentes):
        if todos_qualy:
            encabezados = [
                f"🎾 ¡Comienza la Qualy de {torneo}! Estos son los argentinos que juegan: 🇦🇷",
                f"Día de clasificación en la Qualy de {torneo}: 🇦🇷",
                f"Agenda de la Qualy de {torneo}: 🇦🇷",
                f"¡Empieza la batalla por entrar al cuadro principal de {torneo}! Juegan los argentinos: 🇦🇷"
            ]
        else:
            encabezados = [
                f"🎾 ¡Comienza la Qualy {frases['en']}! Estos son los argentinos que juegan: 🇦🇷",
                f"Día de clasificación {frases['en']}: 🇦🇷",
                f"Agenda de la Qualy {frases['en']}: 🇦🇷",
                f"¡Empieza la batalla por entrar {frases['al']}! Juegan los argentinos: 🇦🇷"
            ]
    else:
        encabezados = [
            f"Hoy {frases['en']} juegan los argentinos: 🇦🇷",
            f"Hoy tenemos acción argentina {frases['en']}: 🇦🇷",
            f"Estos son los argentinos que juegan hoy {frases['en']}: ",
            f"Agenda 🇦🇷 lista {frases['del']}:",
            f"¡Día de tenis argentino {frases['en']}! 🇦🇷",
            f"Atenti a la agenda de hoy {frases['en']}: 🇦🇷"
        ]
    
    encabezado = random.choice(encabezados)
    lineas_partidos = []
    
    for p in partidos:
        hora = p.get('event_time', 'S/H')
        j1 = p.get('event_first_player')
        j2 = p.get('event_second_player')
        
        info = p.get('arg_info', {})
        try:
            rank1 = int(info.get('jugador_1', {}).get('ranking', 9999))
        except (ValueError, TypeError):
            rank1 = 9999
        try:
            rank2 = int(info.get('jugador_2', {}).get('ranking', 9999))
        except (ValueError, TypeError):
            rank2 = 9999
        pais1 = info.get('jugador_1', {}).get('pais', '')
        pais2 = info.get('jugador_2', {}).get('pais', '')
        
        flag1 = obtener_bandera(pais1)
        flag2 = obtener_bandera(pais2)
        
        r1_str = f"({rank1}°)" if rank1 < 2500 else ""
        r2_str = f"({rank2}°)" if rank2 < 2500 else ""
        
        ronda = traducir_ronda(p.get('tournament_round', ''))
        qualy = " (Qualy)" if (p.get('es_qualy') and not todos_qualy) else ""
        
        j1_str = _formatear_jugador_completo(j1, flag1, r1_str)
        j2_str = _formatear_jugador_completo(j2, flag2, r2_str)
        
        comienzos = [
            f"A las {hora},", f"Desde las {hora},",
            f"A partir de las {hora},", f"En el turno de las {hora},"
        ] if hora != 'S/H' else ["En horario a confirmar,", "Sin horario definido todavía,"]
        comienzo = random.choice(comienzos)
        
        verbos = [
            "se medirá ante", "jugará contra", "se enfrentará a",
            "chocará contra", "irá frente a", "buscará avanzar ante", "se cruzará con"
        ]
        verbo = random.choice(verbos)
        
        texto_ronda = f" (por los {ronda})" if ronda and ronda not in ["Qualy", "R1", "R2", "R3", "Ronda", "Final"] else ""
        if "Qualy" in ronda: texto_ronda = f" (por la {ronda})"
        elif ronda in ["R1", "R2", "R3", "Ronda"]: texto_ronda = f" (por la {ronda})"
        elif ronda == "Final": texto_ronda = " en la gran final"
        if qualy: texto_ronda += qualy
        
        j1_es_arg = info.get('jugador_1', {}).get('es_arg', False)
        
        if es_derbi_argentino(pais1, pais2):
             line = f"🎾 {comienzo} tendremos un hermoso DERBI 🇦🇷: {j1_str} {verbo} {j2_str}{texto_ronda}."
        else:
            if j1_es_arg:
                line = f"🎾 {comienzo} {j1_str} {verbo} {j2_str}{texto_ronda}."
            else:
                line = f"🎾 {comienzo} {j2_str} {verbo} {j1_str}{texto_ronda}."
                
        lineas_partidos.append(line)
    
    cierres = [
        f"Vamos con todo che!! 🇦🇷 {tag_torneo}",
        f"A dejar todo hoy 🇦🇷 {tag_torneo}",
        f"Esperemos que hoy sea un gran día para el tenis argentino 🇦🇷 {tag_torneo}",
        f"Lindo día para ver tenis 🇦🇷 {tag_torneo}",
        f"Día de matienzos y tenis 🧉 {tag_torneo}",
        f"Día movidito hoy. {tag_torneo}",
        f"Mucha garra hoy! 🇦🇷 {tag_torneo}"
    ]
    
    return _formatear_en_hilo(encabezado, lineas_partidos, cierres)

def generar_tweet_actualizacion(torneo_original, partidos):
    """Genera el texto para un tweet en vivo simplificado con hashtag."""
    torneo = traducir_nombre_torneo(torneo_original)
    cat = extraer_categoria(partidos[0])
    tag_torneo = obtener_hashtag_torneo(torneo, cat)
    frases = obtener_frases_torneo(torneo_original, partidos)
    
    rondas_presentes = set()
    for p in partidos:
        r = traducir_ronda(p.get('tournament_round', ''))
        if r:
            rondas_presentes.add(r)
            
    if "Final" in rondas_presentes:
        encabezados = [
            f"🏆 ¡Se está jugando la FINAL {frases['en']}! 🇦🇷",
            f"Acción en vivo desde la final {frases['del']}: 🇦🇷🏆",
            f"Así va la gran final {frases['del']}: 🇦🇷"
        ]
    elif "Semifinal" in rondas_presentes:
        encabezados = [
            f"¡Están en juego las semifinales {frases['del']}! 🇦🇷",
            f"Actualizamos las Semis {frases['en']}: 🇦🇷",
            f"Buscando el pase a la final en vivo {frases['en']}: 🇦🇷"
        ]
    elif "4tos" in rondas_presentes:
        encabezados = [
            f"Acción en vivo de los 4tos {frases['en']}: 🇦🇷",
            f"Actualizamos los 4tos {frases['en']}: 🇦🇷",
            f"Peleando por llegar a semis {frases['en']}: 🇦🇷"
        ]
    elif "8vos" in rondas_presentes:
        encabezados = [
            f"Actualizamos los 8vos {frases['en']}: 🇦🇷",
            f"Acción de 8vos en vivo desde {frases['nombre']}: 🇦🇷"
        ]
    else:
        encabezados = [
            f"{frases['en'].capitalize()} están jugando: 🇦🇷",
            f"Acción en vivo {frases['en']}: 🇦🇷",
            f"Actualizamos los partidos {frases['en']}: ",
            f"Así estamos {frases['en']}: 🇦🇷💪",
            f"Resultados parciales {frases['en']}: 🇦🇷"
        ]
    
    encabezado = random.choice(encabezados)
    lineas_partidos = []
    
    for p in partidos:
        j1 = p.get('event_first_player')
        j2 = p.get('event_second_player')
        
        info = p.get('arg_info', {})
        try:
            rank1 = int(info.get('jugador_1', {}).get('ranking', 9999))
        except (ValueError, TypeError):
            rank1 = 9999
        try:
            rank2 = int(info.get('jugador_2', {}).get('ranking', 9999))
        except (ValueError, TypeError):
            rank2 = 9999
        pais1 = info.get('jugador_1', {}).get('pais', '')
        pais2 = info.get('jugador_2', {}).get('pais', '')
        
        flag1 = obtener_bandera(pais1)
        flag2 = obtener_bandera(pais2)
        
        r1_str = f"({rank1}°)" if rank1 < 2500 else ""
        r2_str = f"({rank2}°)" if rank2 < 2500 else ""
        
        ronda = traducir_ronda(p.get('tournament_round', ''))
        prefijo_partido = f"• [{ronda}] " if ronda else "• "
        
        scores_api = p.get('scores', [])
        sets_formateados = formatear_sets(scores_api)
        
        # Obtener y traducir estado en vivo
        estado_api = p.get('event_status', '')
        estado_traducido = traducir_estado_en_vivo(estado_api)
        estado_str = f" ({estado_traducido})" if estado_traducido else ""
        
        info_marcador = sets_formateados if sets_formateados else "0-0"
        marcador_completo = f"{info_marcador}{estado_str}"
        
        j1_str = _formatear_jugador_completo(j1, flag1, r1_str)
        j2_str = _formatear_jugador_completo(j2, flag2, r2_str)
        
        # Marcar derbi argentino en actualizaciones en vivo
        if es_derbi_argentino(pais1, pais2):
            lineas_partidos.append(f"{prefijo_partido}{j1_str} vs {j2_str}: {marcador_completo}  — DERBI 🇦🇷🇦🇷")
        else:
            lineas_partidos.append(f"{prefijo_partido}{j1_str} vs {j2_str}: {marcador_completo}")
    
    cierres = [
        f"¡Vamos que se puede loko! 🇦🇷💪 {tag_torneo}",
        f"Seguilo minuto a minuto! 🇦🇷 {tag_torneo}",
        f"Seguimos punto a punto. 🇦🇷 {tag_torneo}",
        f"¡Dale que se puede! 🇦🇷 {tag_torneo}",
        f"A seguir metiendo 🇦🇷 {tag_torneo}"
    ]
    
    return _formatear_en_hilo(encabezado, lineas_partidos, cierres)

def generar_tweet_finalizado(torneo_original, partidos):
    """Genera el texto para resultados finales con análisis de victoria/derrota."""
    torneo = traducir_nombre_torneo(torneo_original)
    cat = extraer_categoria(partidos[0])
    tag_torneo = obtener_hashtag_torneo(torneo, cat)
    frases = obtener_frases_torneo(torneo_original, partidos)
    
    rondas_presentes = set()
    for p in partidos:
        r = traducir_ronda(p.get('tournament_round', ''))
        if r:
            rondas_presentes.add(r)
            
    if "Final" in rondas_presentes:
        encabezados = [
            f"🏆 ¡Resultados de la FINAL {frases['en']}! 🇦🇷",
            f"Terminó el torneo para los nuestros {frases['en']}: 🇦🇷🏆",
            f"Así nos fue en la gran final {frases['del']}: 🇦🇷"
        ]
    elif "Semifinal" in rondas_presentes:
        encabezados = [
            f"Resultados de las semifinales {frases['en']}: 🇦🇷",
            f"Terminaron las Semis {frases['en']}: 🇦🇷",
            f"¿Quién pasó a la final? Resumen {frases['en']}: 🇦🇷"
        ]
    elif "4tos" in rondas_presentes:
        encabezados = [
            f"Resultados de los 4tos {frases['en']}: 🇦🇷",
            f"Terminaron los 4tos {frases['en']}: 🇦🇷",
            f"Balance de los 4tos {frases['en']}: 🇦🇷"
        ]
    elif "8vos" in rondas_presentes:
        encabezados = [
            f"Resultados de los 8vos {frases['en']}: 🇦🇷",
            f"Terminaron los 8vos {frases['en']}: 🇦🇷"
        ]
    else:
        encabezados = [
            f"Resultados finales para los argentinos {frases['en']}: 🇦🇷",
            f"Terminó la jornada {frases['en']}: ",
            f"Balance final {frases['del']} para los argentinos: 🇦🇷",
            f"Resultados finales {frases['en']}: 🇦🇷",
            f"Resumen de los argentinos hoy {frases['en']}: "
        ]
    
    encabezado = random.choice(encabezados)
    lineas_partidos = []
    
    total_victorias = 0
    total_derrotas = 0
    
    for p in partidos:
        j1 = p.get('event_first_player')
        j2 = p.get('event_second_player')
        
        info = p.get('arg_info', {})
        try:
            rank1 = int(info.get('jugador_1', {}).get('ranking', 9999))
        except (ValueError, TypeError):
            rank1 = 9999
        try:
            rank2 = int(info.get('jugador_2', {}).get('ranking', 9999))
        except (ValueError, TypeError):
            rank2 = 9999
        pais1 = info.get('jugador_1', {}).get('pais', '')
        pais2 = info.get('jugador_2', {}).get('pais', '')
        
        flag1 = obtener_bandera(pais1)
        flag2 = obtener_bandera(pais2)
        
        r1_str = f"({rank1}°)" if rank1 < 2500 else ""
        r2_str = f"({rank2}°)" if rank2 < 2500 else ""
        
        ronda = traducir_ronda(p.get('tournament_round', ''))
        
        scores_api = p.get('scores', [])
        sets_formateados = formatear_sets(scores_api)
        marcador = sets_formateados if sets_formateados else p.get('event_final_result', '0-0')
        j1_str = _formatear_jugador_completo(j1, flag1, r1_str)
        j2_str = _formatear_jugador_completo(j2, flag2, r2_str)
        
        es_qualy = p.get('es_qualy', False)
        es_gs = any(gs in torneo.lower() for gs in ["roland garros", "wimbledon", "us open", "australian open"])
        prefijo_torneo = torneo if es_gs else f"{cat} {torneo}".strip()
        
        texto_ronda = f" por los {ronda}" if ronda and ronda not in ["Qualy", "Final", "R1", "R2", "R3", "Ronda"] else ""
        if "Qualy" in ronda: texto_ronda = f" en la {ronda}"
        elif ronda == "Final": texto_ronda = f" en la gran final"
        elif ronda in ["R1", "R2", "R3", "Ronda"]: texto_ronda = f" en la {ronda}"
        
        if es_qualy: texto_ronda += f" de {prefijo_torneo}"
        
        msg_result, gano = analizar_resultado_argentino(p)
        if gano is True: total_victorias += 1
        elif gano is False: total_derrotas += 1

        if es_derbi_argentino(pais1, pais2):
            try:
                s1, s2 = map(int, p.get('event_final_result', '0 - 0').split(' - '))
            except:
                s1, s2 = 0, 0
                
            status_low = p.get('event_status', '').lower()
            es_retiro = status_low in ['retired', 'walkover', 'w.o.', 'ret.'] or 'retired' in status_low or 'walkover' in status_low
            tipo_retiro = "retiro" if ("ret" in status_low or "retired" in status_low) else "W.O."
            
            if es_retiro:
                if s1 > s2: line = f"🇦🇷 DERBI: {j1_str} avanza por {tipo_retiro} de {j2_str}."
                elif s2 > s1: line = f"🇦🇷 DERBI: {j2_str} avanza por {tipo_retiro} de {j1_str}."
                else: line = f"🇦🇷 DERBI: Partido definido por {tipo_retiro}."
            else:
                if s1 > s2: line = f"🇦🇷 DERBI: ¡Triunfo para {j1_str}! Superó a {j2_str} por {marcador}{texto_ronda}."
                elif s2 > s1: line = f"🇦🇷 DERBI: ¡Triunfo para {j2_str}! Superó a {j1_str} por {marcador}{texto_ronda}."
                else: line = f"🇦🇷 DERBI: Partido terminado entre {j1_str} y {j2_str}."
        else:
            j1_es_arg = info.get('jugador_1', {}).get('es_arg', False)
            if j1_es_arg:
                arg_str, riv_str = j1_str, j2_str
            else:
                arg_str, riv_str = j2_str, j1_str
                
            if gano:
                verbos_victoria = ["superó a", "venció a", "derrotó a", "le ganó a", "se impuso ante"]
                v = random.choice(verbos_victoria)
                line = f"✅ ¡Triunfo argentino! {arg_str} {v} {riv_str} por {marcador}{texto_ronda}."
            else:
                verbos_derrota = ["cayó ante", "no pudo con", "fue derrotado por", "perdió con"]
                v = random.choice(verbos_derrota)
                line = f"❌ Fin del camino para {arg_str}. {v.capitalize()} {riv_str} por {marcador}{texto_ronda}."

        lineas_partidos.append(line)
    
    # Selección de cierres según balance de la jornada
    if total_victorias > 0 and total_derrotas == 0:
        cierres = [
            f"¡VAMOS ARGENTINA! 🇦🇷 #Tenis {tag_torneo}",
            f"Gran jornada para el tenis nacional. 🇦🇷 {tag_torneo}",
            f"Seguimos sumando 💪 {tag_torneo}",
            f"¡Argentina pisando fuerte en el circuito! {tag_torneo}",
            f"Paso firme los argentinos hoy. 🇦🇷 {tag_torneo}",
            f"Buen día para el tenis argentino 🇦🇷 {tag_torneo}"
        ]
    elif total_victorias == 0 and total_derrotas > 0:
        cierres = [
            f"Día difícil, pero siempre bancando 🇦🇷 {tag_torneo}",
            f"A recargar pilas para el próximo torneo 💪 {tag_torneo}",
            f"No se dio hoy 🇦🇷 {tag_torneo}",
            f"A seguir adelante 🇦🇷 {tag_torneo}",
            f"No fue el mejor día 🇦🇷 {tag_torneo}"
        ]
    else:
        cierres = [
            f"Así quedó la jornada 🇦🇷 {tag_torneo}",
            f"Balance del día para los argentinos 🇦🇷 {tag_torneo}",
            f"Terminó la acción por hoy  {tag_torneo}",
            f"Cerramos un día intenso 🇦🇷 {tag_torneo}",
            f"Con una de cal y una de arena hoy 🇦🇷 {tag_torneo}"
        ]
        
    return _formatear_en_hilo(encabezado, lineas_partidos, cierres)

def generar_tweet_ranking(datos, tipo="atp"):
    """Genera un tweet con el Top 10 del ranking."""
    top_10 = datos[:10]
    emoji_cat = "💪" if tipo.lower() == "atp" else ""
    
    encabezados = [
        f"Top 10 Ranking {tipo.upper()} :",
        f"Así quedó el Top 10 {tipo.upper()} esta semana:",
        f"El nuevo Top 10 del mundo ({tipo.upper()}):"
    ]
    
    lineas = [random.choice(encabezados)]
    
    for p in top_10:
        pos = p.get('place', p.get('player_place'))
        nombre_completo = p.get('player', p.get('player_name', ''))
        
        # Usar solo el apellido (o el resto del nombre sin el primero)
        # "Jannik Sinner" -> "Sinner", "Alex De Minaur" -> "De Minaur"
        partes = nombre_completo.split()
        nombre_corto = " ".join(partes[1:]) if len(partes) > 1 else nombre_completo
        
        pais = p.get('country', p.get('player_country'))
        flag = obtener_bandera(pais)
        puntos = p.get('points', p.get('player_points'))
        
        lineas.append(f"{pos}. {nombre_corto} {flag} {puntos}")
    
    lineas.append("")
    
    cierres = [
        f"#{tipo.upper()}Ranking",
        f"#Ranking{tipo.upper()}"
    ]
    lineas.append(random.choice(cierres))
    
    texto = "\n".join(lineas)
    return f"--- INICIO TWEET ---\n{texto}\n--- FIN TWEET ---"

def generar_hilo_ranking_argentinos(datos, tipo="atp"):
    """
    Genera un hilo de tweets con las posiciones de todos los argentinos en el ranking.
    Divide el contenido automáticamente si supera los 280 caracteres.
    """
    argentinos = [p for p in datos if p.get('country', p.get('player_country', '')).lower() in ['argentina', 'arg']]
    
    # Asegurar orden por ranking
    try:
        argentinos.sort(key=lambda x: int(x.get('place', x.get('player_place', 9999))))
    except:
        pass
        
    if not argentinos:
        return ["--- INICIO TWEET ---\nNo se encontraron jugadores argentinos en el ranking hoy. 🇦🇷\n--- FIN TWEET ---"]

    encabezados = [
        f"🇦🇷 Así están los argentinos en el ranking {tipo.upper()} esta semana:",
        f"Ranking {tipo.upper()}: 🇦🇷",
        f"¿Cómo están rankeados los argentinos? 🇦🇷"
    ]
    
    header = random.choice(encabezados) + "\n\n"
    
    tweets = []
    current_text = header
    
    for p in argentinos:
        pos = p.get('place', p.get('player_place'))
        nombre = p.get('player', p.get('player_name'))
        puntos = p.get('points', p.get('player_points'))
        linea = f"• {pos}. {nombre} 🇦🇷 ({puntos} pts)\n"
        
        # Si la línea excede el límite (con margen para el pie de hilo), guardamos y empezamos nuevo tweet
        if len(current_text) + len(linea) > 250:
            tweets.append(current_text.strip())
            # El siguiente tweet empieza con la numeración
            current_text = f"({len(tweets) + 1}/?) Sigue el ranking: 👇\n\n" + linea
        else:
            current_text += linea
            
    # Añadir el último acumulado
    tweets.append(current_text.strip())
    
    # Post-procesamiento para enumerar hilos correctamente (1/X, 2/X, etc)
    total_tweets = len(tweets)
    hilo_final = []
    
    for idx, t in enumerate(tweets):
        if total_tweets > 1:
            texto_tweet = t.replace("/?", f"/{total_tweets}")
            # Si es el primero y no tiene el (1/X), se lo agregamos al final
            if idx == 0 and f"(1/{total_tweets})" not in texto_tweet:
                texto_tweet += f"\n\n(1/{total_tweets}) 🧵"
        else:
            texto_tweet = t
            
        hilo_final.append(f"--- TWEET {idx+1} ---\n{texto_tweet}\n--- FIN TWEET ---")
        
    return hilo_final
