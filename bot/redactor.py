import random

def formatear_sets(scores):
    """
    Convierte la lista de scores de la API en un string legible de games por set.
    """
    if not scores or not isinstance(scores, list):
        return ""
    
    sets = []
    for s in scores:
        s1 = s.get('score_first', '0')
        s2 = s.get('score_second', '0')
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

def obtener_hashtag_torneo(nombre_torneo):
    """Mapea nombres de torneos a sus hashtags oficiales o genera uno genérico."""
    nombre = nombre_torneo.lower()
    
    mapping = {
        "roma": "#IBI26",
        "madrid": "#MMOPEN",
        "monte carlo": "#MonteCarloMasters",
        "roland garros": "#RolandGarros",
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
            
    tag_generico = "#" + "".join(nombre_torneo.split())
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
        "¡VAMOS! 🇦🇷🔥", "¡Triunfazo peleado! ✅", "Se sufrió pero se ganó. 💪", 
        "¡Partidazo y victoria! 🎾", "Lo dio vuelta y festejó. 🇦🇷", "Garra y corazón para ganar. ✅"
    ]
    mensajes_victoria_facil = [
        "¡Dio cátedra! 🎾🔥", "Masterclass de tenis. ✅", "¡Paliza! Imparable hoy. 💪",
        "Paso firme y victoria. 🇦🇷", "¡Adentro! Vamos por más. ✅", "Sin despeinarse, a la siguiente. 🎾"
    ]
    mensajes_derrota_ajustada = [
        "Una lástima, se escapó por poco.", "Casi se da, gran esfuerzo.", "Se luchó hasta el final. 🇦🇷",
        "Dolió esta, estuvo ahí. 😕", "Se escapó en el cierre, una pena.", "A levantar cabeza, fue un partidazo."
    ]
    mensajes_derrota_facil = [
        "No pudo ser esta vez. 🎾", "Dura derrota. 🇦🇷", "La tuvo complicada hoy. 😕",
        "Día difícil para el pibe. 🎾", "No encontró el ritmo hoy. 🇦🇷", "A pensar en el próximo torneo. 😕"
    ]
    
    # Caso 1: Jugador 1 es el argentino
    if j1_es_arg:
        if ganador == 1:
            if s2 >= 1: # Ganó 2-1 o similar
                return random.choice(mensajes_victoria_ajustada)
            else: # Ganó 2-0 o similar
                return random.choice(mensajes_victoria_facil)
        elif ganador == 2:
            if s1 >= 1: # Perdió 1-2
                return random.choice(mensajes_derrota_ajustada)
            else: # Perdió 0-2
                return random.choice(mensajes_derrota_facil)
                
    # Caso 2: Jugador 2 es el argentino
    if j2_es_arg:
        if ganador == 2:
            if s1 >= 1: # Ganó 2-1
                return random.choice(mensajes_victoria_ajustada)
            else: # Ganó 2-0
                return random.choice(mensajes_victoria_facil)
        elif ganador == 1:
            if s2 >= 1: # Perdió 1-2
                return random.choice(mensajes_derrota_ajustada)
            else: # Perdió 0-2
                return random.choice(mensajes_derrota_facil)
                
    return ""

def generar_tweet_agenda(torneo, partidos):
    """Genera el texto para un tweet de agenda con categoría y hashtag."""
    cat = extraer_categoria(partidos[0])
    prefijo = f"{cat} " if cat else ""
    tag_torneo = obtener_hashtag_torneo(torneo)
    
    encabezados = [
        f"Hoy en el {prefijo}{torneo} juegan los argentinos: 🇦🇷🎾",
        f"Hoy tenemos acción argentina en el {prefijo}{torneo}: 🇦🇷",
        f"Estos son los argentinos que juegan hoy en {prefijo}{torneo}: 🎾",
        f"Agenda lista para los nuestros en el {prefijo}{torneo}: 🇦🇷",
        f"¡Día de tenis! Argentinos en cancha en el {prefijo}{torneo}: 🎾🇦🇷",
        f"Atenti a la agenda de hoy en el {prefijo}{torneo}: 🇦🇷🎾"
    ]
    
    lineas = [random.choice(encabezados)]
    lineas.append("") 
    
    for p in partidos:
        hora = p.get('event_time', 'S/H')
        j1 = p.get('event_first_player')
        j2 = p.get('event_second_player')
        qualy = " (Qualy)" if p.get('es_qualy') else ""
        lineas.append(f"• {hora} | {j1} vs {j2}{qualy}")
    
    lineas.append("")
    
    cierres = [
        f"Vamos con todo che!! 🇦🇷 {tag_torneo}",
        f"A dejar todo hoy 🇦🇷 {tag_torneo}",
        f"Esperemos que hoy sea un gran día para el tenis argentino 🇦🇷 {tag_torneo}",
        f"Lindo día para ver tenis 🇦🇷 {tag_torneo}",
        f"Día de matienzos y tenis 🧉 {tag_torneo}",
        f"Día movidito para los tenistas argentinos. {tag_torneo}",
        f"Mucha garra hoy! 🇦🇷 {tag_torneo}"
    ]
    lineas.append(random.choice(cierres))
    
    texto = "\n".join(lineas)
    return f"--- INICIO TWEET ---\n{texto}\n--- FIN TWEET ---"

def generar_tweet_actualizacion(torneo, partidos):
    """Genera el texto para un tweet en vivo simplificado con hashtag."""
    cat = extraer_categoria(partidos[0])
    prefijo = f"{cat} " if cat else ""
    tag_torneo = obtener_hashtag_torneo(torneo)
    
    encabezados = [
        f"En el {prefijo}{torneo} están jugando: 🎾🇦🇷",
        f"Acción en vivo desde el {prefijo}{torneo}: 🇦🇷",
        f"Actualizamos los partidos en el {prefijo}{torneo}: 🎾",
        f"Así vienen los pibes en el {prefijo}{torneo}: 🇦🇷💪",
        f"Resultados parciales en el {prefijo}{torneo}: 🎾🇦🇷"
    ]
    
    lineas = [random.choice(encabezados)]
    lineas.append("") 
    
    for p in partidos:
        j1 = p.get('event_first_player')
        j2 = p.get('event_second_player')
        
        scores_api = p.get('scores', [])
        sets_formateados = formatear_sets(scores_api)
        info_marcador = sets_formateados if sets_formateados else "0-0"
            
        lineas.append(f"• {j1} vs {j2}: {info_marcador}")
    
    lineas.append("")
    
    cierres = [
        f"¡Vamos que se puede loko! 🇦🇷💪 {tag_torneo}",
        f"Seguilo minuto a minuto! 🇦🇷 {tag_torneo}",
        f"¡Qué momento para estar vivos! Aguante el tenis. 🇦🇷 {tag_torneo}",
        f"Cada punto vale oro. ¡Vamos carajo! 💪 {tag_torneo}",
        f"La garra argentina en su máxima expresión. 🇦🇷 {tag_torneo}",
        f"¿Sale remontada épica? Yo confío. 🇦🇷 {tag_torneo}",
    ]
    lineas.append(random.choice(cierres))
    
    texto = "\n".join(lineas)
    return f"--- INICIO TWEET ---\n{texto}\n--- FIN TWEET ---"

def generar_tweet_finalizado(torneo, partidos):
    """Genera el texto para resultados finales con análisis de victoria/derrota."""
    cat = extraer_categoria(partidos[0])
    prefijo = f"{cat} " if cat else ""
    tag_torneo = obtener_hashtag_torneo(torneo)
    
    encabezados = [
        f"Resultados finales para los argentinos en el {prefijo}{torneo}: 🇦🇷",
        f"Terminó la jornada en el {prefijo}{torneo}. Así les fue a los nuestros: 🎾",
        f"Balance final del {prefijo}{torneo} para la legión: 🇦🇷",
        f"Marcadores finales en el {prefijo}{torneo}: ✅🇦🇷",
        f"Resumen de los argentinos hoy en el {prefijo}{torneo}: 🎾"
    ]
    
    lineas = [random.choice(encabezados)]
    lineas.append("") 
    
    for p in partidos:
        j1 = p.get('event_first_player')
        j2 = p.get('event_second_player')
        
        scores_api = p.get('scores', [])
        sets_formateados = formatear_sets(scores_api)
        
        marcador = sets_formateados if sets_formateados else p.get('event_final_result', '0-0')
        msg_result = analizar_resultado_argentino(p)
        
        lineas.append(f"• {j1} vs {j2}: {marcador} {msg_result}")
    
    lineas.append("")
    
    cierres = [
        f"¡VAMOS ARGENTINA! 🇦🇷 #Tenis {tag_torneo}",
        f"Gran jornada para el tenis nacional. 🇦🇷 {tag_torneo}",
        f"Seguimos sumando. ¡Orgullo por los nuestros! 💪 {tag_torneo}",
        f"Así quedó la jornada. ¡Mañana por más! 🇦🇷 {tag_torneo}",
        f"Balance del día para los nuestros. 🇦🇷 {tag_torneo}",
        f"¡Argentina pisando fuerte en el circuito! {tag_torneo}",
        f"Terminó la acción por hoy 🎾 {tag_torneo}",
        f"Cerramos un día intenso. ¡Gracias por el aguante! 🇦🇷 {tag_torneo}"
    ]
    lineas.append(random.choice(cierres))
    
    texto = "\n".join(lineas)
    return f"--- INICIO TWEET ---\n{texto}\n--- FIN TWEET ---"
