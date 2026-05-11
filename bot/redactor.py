import random

def obtener_bandera(pais):
    """Devuelve el emoji de la bandera para un país dado."""
    if not pais: return "🎾"
    
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
    }
    return mapping.get(p, "🎾")

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

def traducir_nombre_torneo(nombre):
    """Traduce nombres de torneos de inglés a español para el público argentino."""
    nombre_low = nombre.lower()
    
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
    
    for en, es in traducciones.items():
        if en in nombre_low:
            return es
            
    # Si no hay traducción específica, devolver el original (capitalizado)
    return nombre

def obtener_hashtag_torneo(nombre_torneo, categoria=""):
    """Mapea nombres de torneos a sus hashtags oficiales o genera uno genérico incluyendo la categoría."""
    nombre = nombre_torneo.lower()
    
    # Mapeo de torneos importantes (estos tienen prioridad)
    mapping = {
        "roma": "#IBI26",
        "rome": "#IBI26",
        "madrid": "#MMOPEN",
        "monte-carlo": "#MonteCarloMasters",
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
    
    # Combinar categoría y nombre para el hashtag genérico (ej: "Challenger" + "Santos" -> "#ChallengerSantos")
    # Evitamos repetir si la categoría ya está en el nombre (ej: "ITF W35" -> no poner ITFtwice)
    prefijo = categoria if categoria and categoria.upper() not in nombre_base.upper() else ""
    full_name = f"{prefijo}{nombre_base}"
    
    # Generar hashtag genérico quitando espacios y caracteres especiales
    nombre_limpio = "".join(char for char in full_name if char.isalnum())
    tag_generico = "#" + nombre_limpio
    return tag_generico

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
    
    # Mensajes
    mensajes_victoria_ajustada = [
        "¡VAMOS! 🇦🇷", "¡Triunfazo peleado!", "Se sufrió pero se ganó. 💪", 
        "¡Partidazo y victoria! 🎾", "Lo dio vuelta y festejó. 🇦🇷", "Garra y corazón para ganar."
    ]
    mensajes_victoria_facil = [
        "Cátedra de tenis! 🎾", "Masterclass de tenis.", "¡Paliza! Imparable hoy. 💪",
        "Paso firme y victoria. 🇦🇷", "¡Adentro! Vamos por más.", "Sin despeinarse, a la siguiente. 🎾"
    ]
    mensajes_derrota_ajustada = [
        "Una lástima, se escapó por poco.", "Casi se da, gran esfuerzo.", "Se luchó hasta el final. 🇦🇷",
        "Dolió esta, estuvo ahí. 😕", "Se escapó en el cierre, una pena.", "A levantar cabeza, fue un partidazo."
    ]
    mensajes_derrota_facil = [
        "No pudo ser esta vez. 🎾", "Dura derrota. 🇦🇷", "La tuvo complicada hoy. 😕",
        "No encontró el ritmo hoy. 🇦🇷", "A pensar en el próximo torneo. 😕"
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
    margen_hilo = 20
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

def generar_tweet_agenda(torneo_original, partidos):
    """Genera el texto para un tweet de agenda con categoría y hashtag."""
    torneo = traducir_nombre_torneo(torneo_original)
    cat = extraer_categoria(partidos[0])
    prefijo = f"{cat} " if cat else ""
    tag_torneo = obtener_hashtag_torneo(torneo, cat)
    
    encabezados = [
        f"Hoy en el {prefijo}{torneo} juegan los argentinos: 🇦🇷🎾",
        f"Hoy tenemos acción argentina en el {prefijo}{torneo}: 🇦🇷",
        f"Estos son los argentinos que juegan hoy en {prefijo}{torneo}: 🎾",
        f"Agenda lista para los nuestros en el {prefijo}{torneo}: 🇦🇷",
        f"¡Día de tenis! Argentinos en cancha en el {prefijo}{torneo}: 🎾🇦🇷",
        f"Atenti a la agenda de hoy en el {prefijo}{torneo}: 🇦🇷🎾"
    ]
    
    encabezado = random.choice(encabezados)
    lineas_partidos = []
    
    for p in partidos:
        hora = p.get('event_time', 'S/H')
        j1 = p.get('event_first_player')
        j2 = p.get('event_second_player')
        
        info = p.get('arg_info', {})
        rank1 = info.get('jugador_1', {}).get('ranking', 9999)
        rank2 = info.get('jugador_2', {}).get('ranking', 9999)
        pais1 = info.get('jugador_1', {}).get('pais', '')
        pais2 = info.get('jugador_2', {}).get('pais', '')
        
        flag1 = obtener_bandera(pais1)
        flag2 = obtener_bandera(pais2)
        
        r1_str = f"({rank1}°)" if rank1 < 2500 else ""
        r2_str = f"({rank2}°)" if rank2 < 2500 else ""
        
        qualy = " (Qualy)" if p.get('es_qualy') else ""
        lineas_partidos.append(f"• {hora} | {j1} {flag1} {r1_str} vs {j2} {flag2} {r2_str}{qualy}")
    
    cierres = [
        f"Vamos con todo che!! 🇦🇷 {tag_torneo}",
        f"A dejar todo hoy 🇦🇷 {tag_torneo}",
        f"Esperemos que hoy sea un gran día para el tenis argentino 🇦🇷 {tag_torneo}",
        f"Lindo día para ver tenis 🇦🇷 {tag_torneo}",
        f"Día de matienzos y tenis 🧉 {tag_torneo}",
        f"Día movidito para los tenistas argentinos. {tag_torneo}",
        f"Mucha garra hoy! 🇦🇷 {tag_torneo}"
    ]
    
    return _formatear_en_hilo(encabezado, lineas_partidos, cierres)

def generar_tweet_actualizacion(torneo_original, partidos):
    """Genera el texto para un tweet en vivo simplificado con hashtag."""
    torneo = traducir_nombre_torneo(torneo_original)
    cat = extraer_categoria(partidos[0])
    prefijo = f"{cat} " if cat else ""
    tag_torneo = obtener_hashtag_torneo(torneo, cat)
    
    encabezados = [
        f"En el {prefijo}{torneo} están jugando: 🎾🇦🇷",
        f"Acción en vivo desde el {prefijo}{torneo}: 🇦🇷",
        f"Actualizamos los partidos en el {prefijo}{torneo}: 🎾",
        f"Así vienen los pibes en el {prefijo}{torneo}: 🇦🇷💪",
        f"Resultados parciales en el {prefijo}{torneo}: 🎾🇦🇷"
    ]
    
    encabezado = random.choice(encabezados)
    lineas_partidos = []
    
    for p in partidos:
        j1 = p.get('event_first_player')
        j2 = p.get('event_second_player')
        
        info = p.get('arg_info', {})
        rank1 = info.get('jugador_1', {}).get('ranking', 9999)
        rank2 = info.get('jugador_2', {}).get('ranking', 9999)
        pais1 = info.get('jugador_1', {}).get('pais', '')
        pais2 = info.get('jugador_2', {}).get('pais', '')
        
        flag1 = obtener_bandera(pais1)
        flag2 = obtener_bandera(pais2)
        
        r1_str = f"({rank1}°)" if rank1 < 2500 else ""
        r2_str = f"({rank2}°)" if rank2 < 2500 else ""
        
        scores_api = p.get('scores', [])
        sets_formateados = formatear_sets(scores_api)
        info_marcador = sets_formateados if sets_formateados else "0-0"
            
        lineas_partidos.append(f"• {j1} {flag1} {r1_str} vs {j2} {flag2} {r2_str}: {info_marcador}")
    
    cierres = [
        f"¡Vamos que se puede loko! 🇦🇷💪 {tag_torneo}",
        f"Seguilo minuto a minuto! 🇦🇷 {tag_torneo}",
        f"Seguimos punto a punto. 🇦🇷 {tag_torneo}",
        f"¡Hay que poner huevo! 🇦🇷 {tag_torneo}",
    ]
    
    return _formatear_en_hilo(encabezado, lineas_partidos, cierres)

def generar_tweet_finalizado(torneo_original, partidos):
    """Genera el texto para resultados finales con análisis de victoria/derrota."""
    torneo = traducir_nombre_torneo(torneo_original)
    cat = extraer_categoria(partidos[0])
    prefijo = f"{cat} " if cat else ""
    tag_torneo = obtener_hashtag_torneo(torneo, cat)
    
    encabezados = [
        f"Resultados finales para los argentinos en el {prefijo}{torneo}: 🇦🇷",
        f"Terminó la jornada en el {prefijo}{torneo}: ",
        f"Balance final del {prefijo}{torneo} para los argentinos: 🇦🇷",
        f"Marcadores finales en el {prefijo}{torneo}:🇦🇷",
        f"Resumen de los argentinos hoy en el {prefijo}{torneo}: 🎾"
    ]
    
    encabezado = random.choice(encabezados)
    lineas_partidos = []
    
    total_victorias = 0
    total_derrotas = 0
    
    for p in partidos:
        j1 = p.get('event_first_player')
        j2 = p.get('event_second_player')
        
        info = p.get('arg_info', {})
        rank1 = info.get('jugador_1', {}).get('ranking', 9999)
        rank2 = info.get('jugador_2', {}).get('ranking', 9999)
        pais1 = info.get('jugador_1', {}).get('pais', '')
        pais2 = info.get('jugador_2', {}).get('pais', '')
        
        flag1 = obtener_bandera(pais1)
        flag2 = obtener_bandera(pais2)
        
        r1_str = f"({rank1}°)" if rank1 < 2500 else ""
        r2_str = f"({rank2}°)" if rank2 < 2500 else ""
        
        scores_api = p.get('scores', [])
        sets_formateados = formatear_sets(scores_api)
        
        marcador = sets_formateados if sets_formateados else p.get('event_final_result', '0-0')
        msg_result, gano = analizar_resultado_argentino(p)
        
        if gano is True: total_victorias += 1
        elif gano is False: total_derrotas += 1
        
        lineas_partidos.append(f"• {j1} {flag1} {r1_str} vs {j2} {flag2} {r2_str}: {marcador} {msg_result}")
    
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
            f"Día difícil, pero siempre bancando a los nuestros 🇦🇷 {tag_torneo}",
            f"A recargar pilas para el próximo torneo 💪 {tag_torneo}",
            f"No se dio hoy, pero el esfuerzo no se negocia 🎾 {tag_torneo}",
            f"A seguir laburando que los resultados van a llegar 🇦🇷 {tag_torneo}",
            f"Un día para aprender y seguir adelante 🇦🇷 {tag_torneo}",
            f"No fue el mejor día para nuestro tenis 🇦🇷 {tag_torneo}"
        ]
    else:
        cierres = [
            f"Así quedó la jornada 🇦🇷 {tag_torneo}",
            f"Balance del día para los argentinos 🇦🇷 {tag_torneo}",
            f"Terminó la acción por hoy 🎾 {tag_torneo}",
            f"Cerramos un día intenso 🇦🇷 {tag_torneo}",
            f"Con una de cal y una de arena hoy 🇦🇷 {tag_torneo}"
        ]
        
    return _formatear_en_hilo(encabezado, lineas_partidos, cierres)

def generar_tweet_ranking(datos, tipo="atp"):
    """Genera un tweet con el Top 10 del ranking."""
    top_10 = datos[:10]
    emoji_cat = "💪" if tipo.lower() == "atp" else "🎾"
    
    encabezados = [
        f"Top 10 Ranking {tipo.upper()} 🎾:",
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
        f"Ranking {tipo.upper()}: Las posiciones de los nuestros players 🇦🇷",
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
