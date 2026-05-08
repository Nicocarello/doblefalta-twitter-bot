def filtrar_argentinos(partidos, api_client):
    """Filtra partidos donde al menos uno de los jugadores es argentino."""
    partidos_arg = []
    total = len(partidos)
    print(f"Total de partidos a procesar: {total}")
    for i, p in enumerate(partidos, 1):
        if i % 10 == 0:
            print(f"Procesando {i}/{total}...")
        p1_key = p.get('first_player_key')
        p2_key = p.get('second_player_key')
        
        info1 = api_client.obtener_info_jugador(p1_key)
        info2 = api_client.obtener_info_jugador(p2_key)
        
        if info1['es_arg'] or info2['es_arg']:
            # Guardamos contexto útil
            p['es_qualy'] = p.get('event_qualification') == 'True'
            p['arg_info'] = {
                'jugador_1': info1,
                'jugador_2': info2
            }
            partidos_arg.append(p)
    return partidos_arg

def agrupar_por_torneo(partidos):
    """Agrupa una lista de partidos por el nombre del torneo."""
    agrupados = {}
    for p in partidos:
        torneo = p.get('tournament_name', 'Otros Torneos').strip()
        if torneo not in agrupados:
            agrupados[torneo] = []
        agrupados[torneo].append(p)
    return agrupados

def es_agenda(partido):
    """Determina si un partido aún no ha comenzado."""
    status = partido.get('event_status', '').lower()
    # En api-tennis, si no empezó, status suele estar vacío, ser igual a la hora, o 'Not Started'
    if not status or status == 'not started' or status == partido.get('event_time'):
        return True
    return False

def contar_games_totales(partido):
    """Suma todos los games jugados en el partido hasta el momento."""
    scores = partido.get('scores', [])
    if not scores or not isinstance(scores, list):
        return 0
    total = 0
    for s in scores:
        try:
            total += int(s.get('score_first', 0))
            total += int(s.get('score_second', 0))
        except (ValueError, TypeError):
            continue
    return total

def es_actualizacion_en_vivo(partido):
    """Determina si un partido está en juego (LIVE) y tiene suficiente avance (mínimo 4 games)."""
    status = partido.get('event_status', '').lower()
    # Ignoramos finalizados, cancelados, pospuestos y vacíos
    ignorar = ['finished', 'cancelled', 'postponed', '', 'not started']
    
    # Si el status es algo como '1st Set', '2nd Set', o un marcador, está en juego
    esta_en_juego = status not in ignorar and status != partido.get('event_time')
    
    if esta_en_juego:
        # Filtro solicitado: al menos 4 games para evitar reportar 0-0 o 1-0
        return contar_games_totales(partido) >= 4
        
    return False

def es_finalizado(partido):
    """Determina si un partido ya terminó."""
    return partido.get('event_status', '').lower() == 'finished'
