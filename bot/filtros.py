"""
Módulo de filtros para el bot Doble Falta.
Contiene funciones para filtrar partidos de argentinos,
agrupar por torneo, y clasificar por estado (agenda, en vivo, finalizado).
"""


def es_junior(partido):
    """
    Determina si un partido corresponde a la categoría junior/juvenil.
    """
    if not partido:
        return False
    etype = str(partido.get('event_type_type', '')).lower()
    tname = str(partido.get('tournament_name', '')).lower()
    tround = str(partido.get('tournament_round', '')).lower()
    
    return any(kw in etype or kw in tname or kw in tround 
               for kw in ["girls", "boys", "junior", "juvenil"])


def filtrar_argentinos(partidos, api):
    """
    Filtra la lista de partidos y devuelve solo aquellos donde al menos
    un jugador es argentino. Enriquece cada partido con 'arg_info' y 'es_qualy'.

    Args:
        partidos: Lista de dicts con datos de fixtures de la API.
        api: Instancia de TennisAPI para consultar info de jugadores.
    
    Returns:
        Lista de partidos con presencia argentina, enriquecidos con metadata.
    """
    resultado = []
    for p in partidos:
        p1_key = p.get('first_player_key')
        p2_key = p.get('second_player_key')

        info_j1 = api.obtener_info_jugador(p1_key)
        info_j2 = api.obtener_info_jugador(p2_key)

        if info_j1.get('es_arg') or info_j2.get('es_arg'):
            # Enriquecer el partido con información argentina
            p['arg_info'] = {
                'jugador_1': {
                    'es_arg': info_j1.get('es_arg', False),
                    'ranking': info_j1.get('ranking', 9999),
                    'pais': info_j1.get('pais', '')
                },
                'jugador_2': {
                    'es_arg': info_j2.get('es_arg', False),
                    'ranking': info_j2.get('ranking', 9999),
                    'pais': info_j2.get('pais', '')
                }
            }
            # Marcar si es partido de clasificación (qualy)
            p['es_qualy'] = p.get('event_qualification') == 'True'
            
            # Marcar y renombrar si es junior
            p['es_junior'] = es_junior(p)
            if p['es_junior'] and 'junior' not in p.get('tournament_name', '').lower():
                p['tournament_name'] = f"{p.get('tournament_name')} Junior"

            resultado.append(p)

    return resultado


def agrupar_por_torneo(partidos):
    """
    Agrupa una lista de partidos por nombre de torneo (tournament_name).

    Returns:
        dict: { 'nombre_torneo': [lista_de_partidos], ... }
    """
    grupos = {}
    for p in partidos:
        torneo = p.get('tournament_name', 'Sin Torneo')
        if torneo not in grupos:
            grupos[torneo] = []
        grupos[torneo].append(p)
    return grupos


def es_agenda(partido):
    """
    Determina si un partido aún no comenzó (está en agenda).
    Un partido está en agenda si su event_status está vacío,
    es 'Not Started', o no indica actividad en curso ni finalización.
    """
    status = partido.get('event_status', '').strip().lower()

    # Sin estado = no arrancó
    if not status:
        return True

    # Estados explícitos de "no comenzado"
    if status in ('not started', 'scheduled'):
        return True

    return False


def es_actualizacion_en_vivo(partido):
    """
    Determina si un partido está en curso (en vivo).
    Está en vivo si tiene un event_status que NO sea vacío, 
    'Finished', 'Retired', 'Walkover', 'Postponed', 'Cancelled', 
    'Not Started', ni igual al horario del partido.
    """
    status = partido.get('event_status', '').strip()
    if not status:
        return False

    status_low = status.lower()

    # Estados que NO son "en vivo"
    estados_no_vivo = {
        'finished', 'retired', 'walkover', 'w.o.', 'ret.',
        'postponed', 'cancelled', 'canceled', 'not started',
        'scheduled', 'abandoned', 'awarded'
    }

    # Si el status es uno de los no-vivo, no está en juego
    if status_low in estados_no_vivo:
        return False

    # Si contiene "retired" o "walkover" como substring
    if 'retired' in status_low or 'walkover' in status_low:
        return False

    # Si el status es igual al horario (ej: "10:00"), no está en vivo
    event_time = partido.get('event_time', '')
    if status == event_time:
        return False

    # Cualquier otro estado se considera en vivo
    # (ej: "1st Set", "2nd Set", "Set 1", números, etc.)
    return True


def es_finalizado(partido):
    """
    Determina si un partido ya terminó.
    Está finalizado si su event_status es 'Finished', 'Retired', 
    'Walkover' o variantes.
    """
    status = partido.get('event_status', '').strip().lower()
    if not status:
        return False

    estados_finales = {'finished', 'retired', 'walkover', 'w.o.', 'ret.'}

    if status in estados_finales:
        return True

    # Variantes como "Walkover - Player Name" o "Retired - ..."
    if 'retired' in status or 'walkover' in status:
        return True

    return False
