import requests
from datetime import datetime
import google.generativeai as genai

# ==========================================
# 1. CONFIGURACIÓN DE CREDENCIALES
# ==========================================

# -- API de Tenis --
TENNIS_API_KEY = "604b94cb8b0b40e9f4c0f5916687706a96ee166e893fb5b836e2b30ef232df03"  # Reemplaza con tu clave de api-tennis
TENNIS_BASE_URL = "https://api.api-tennis.com/tennis/"

# -- API de Gemini --
GEMINI_API_KEY = "AIzaSyDPllPhWfT20R2W3w2_cdXZ1J-fOYYsb0I"  # Reemplaza con tu clave de Google Studio
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

cache_jugadores = {}

def info_jugador(player_key):
    if not player_key: return {'es_arg': False, 'ranking': 9999}
    if player_key in cache_jugadores: return cache_jugadores[player_key]
    params = {'method': 'get_players', 'APIkey': TENNIS_API_KEY, 'player_key': player_key}
    info = {'es_arg': False, 'ranking': 9999}
    try:
        response = requests.get(TENNIS_BASE_URL, params=params, timeout=10)
        datos = response.json()
        if datos.get('success') == 1 and datos.get('result'):
            jugador = datos['result'][0]
            pais = jugador.get('player_country')
            ranking = jugador.get('player_ranking', 9999) 
            if pais and pais.lower() == 'argentina': info['es_arg'] = True
            try: info['ranking'] = int(ranking) if ranking else 9999
            except: pass
        cache_jugadores[player_key] = info
        return info
    except: return info

# ==========================================
# 2. LÓGICA DE AGENDA (MAÑANA)
# ==========================================
def obtener_agenda_hoy():
    hoy = datetime.now().strftime('%Y-%m-%d')
    params = {'method': 'get_fixtures', 'APIkey': TENNIS_API_KEY, 'date_start': hoy, 'date_stop': hoy}
    try:
        response = requests.get(TENNIS_BASE_URL, params=params, timeout=20)
        datos = response.json()
        if datos.get('success') != 1: return []
        partidos = []
        for p in datos.get('result', []):
            if info_jugador(p.get('first_player_key'))['es_arg'] or info_jugador(p.get('second_player_key'))['es_arg']:
                p['es_qualy'] = p.get('event_qualification') == 'True'
                partidos.append(p)
        return partidos
    except: return []

def agrupar_agenda(partidos):
    categorias = {"ATP/GS Masculino": [], "WTA/GS Femenino": [], "Challenger Masculino": [], "Challenger Femenino": [], "ITF Masculino": [], "ITF Femenino": []}
    for p in partidos:
        tipo = p.get('event_type_type', '').lower()
        torneo = p.get('tournament_name', '').upper()
        es_femenino = ('women' in tipo or 'wta' in tipo or (('ITF' in tipo.upper() or 'ITF' in torneo) and torneo.startswith('W')))
        if 'atp' in tipo or 'grand slam' in tipo or 'masters' in tipo: cat = "ATP/GS Masculino"
        elif 'wta' in tipo: cat = "WTA/GS Femenino"
        elif 'challenger' in tipo: cat = "Challenger Femenino" if es_femenino else "Challenger Masculino"
        else: cat = "ITF Femenino" if es_femenino else "ITF Masculino"
        categorias[cat].append(p)
    return categorias

def generar_tweet_agenda(categoria, lista_partidos):
    if not lista_partidos: return None
    datos = ""
    hay_qualy = False
    for p in lista_partidos:
        hora = p.get('event_time', 'S/H')
        j1 = p.get('event_first_player')
        j2 = p.get('event_second_player')
        torneo = p.get('tournament_name')
        qualy = " (QUALY)" if p.get('es_qualy') else ""
        if p.get('es_qualy'): hay_qualy = True
        datos += f"- {hora} | {j1} vs {j2} ({torneo}){qualy}\n"

    instr_qualy = "IMPORTANTE: Hay partidos de QUALY. Menciona el 'aguante' o 'remarla'." if hay_qualy else ""
    instr_genero = "OBLIGATORIO: Usa femenino ('las pibas'). NO uses 'los pibes'." if "Femenino" in categoria else "Usa masculino ('los pibes', 'muchachos')."

    # --- PROMPT ACTUALIZADO PARA SALTOS DE LÍNEA ---
    prompt = f"""Eres @DobleFaltaTenis. Redacta UN tweet para la agenda de {categoria}.
    REGLAS DE FORMATO Y CONTENIDO:
    1. Máximo 270 caracteres. NO uses negritas ni asteriscos.
    2. ESTRUCTURA OBLIGATORIA: 
       - Una línea de introducción/saludo.
       - UN SALTO DE LÍNEA (\n) por cada partido listado. Cada partido debe ocupar su propia línea.
       - Una línea de cierre con arenga y hashtags.
    3. {instr_genero}
    4. {instr_qualy}
    5. Menciona SIEMPRE a los argentinos. Tono argento.
    6. Usa emojis (🇦🇷, 🎾, 💪).
    
    Partidos para hoy:
    {datos}
    
    Devuelve ÚNICAMENTE el texto del tweet."""
    
    try: return model.generate_content(prompt).text.strip()
    except: return None

# ==========================================
# 3. LÓGICA DE ACTUALIZACIÓN (EN VIVO/TARDE)
# ==========================================
def obtener_actualizaciones():
    hoy = datetime.now().strftime('%Y-%m-%d')
    params = {'method': 'get_fixtures', 'APIkey': TENNIS_API_KEY, 'date_start': hoy, 'date_stop': hoy}
    try:
        response = requests.get(TENNIS_BASE_URL, params=params, timeout=20)
        datos = response.json()
        if datos.get('success') != 1: return {'en_juego': [], 'finalizados': []}
        en_juego, finalizados = [], []
        for p in datos.get('result', []):
            i1, i2 = info_jugador(p.get('first_player_key')), info_jugador(p.get('second_player_key'))
            if i1['es_arg'] or i2['es_arg']:
                p['contexto_arg'] = "Jugador 1" if i1['es_arg'] else "Jugador 2"
                p['ranking_j1'], p['ranking_j2'] = i1['ranking'], i2['ranking']
                estado = p.get('event_status', '')
                if estado == 'Finished': finalizados.append(p)
                elif estado not in ['', 'Postponed', 'Cancelled'] and p.get('event_time') != estado: en_juego.append(p)
        return {'en_juego': en_juego, 'finalizados': finalizados}
    except: return {'en_juego': [], 'finalizados': []}

def generar_tweet_actualizacion(tipo, partidos):
    if not partidos: return None
    datos = ""
    for p in partidos:
        datos += f"Partido: {p.get('event_first_player')} (Rank: {p.get('ranking_j1')}) vs {p.get('event_second_player')} (Rank: {p.get('ranking_j2')})\n"
        datos += f"El argentino es el {p.get('contexto_arg')}.\n"
        datos += f"Sets: {p.get('event_final_result', '0-0')} | Estado: {p.get('event_status')} | Game: {p.get('event_game_result', '')}\n\n"

    # --- PROMPT ACTUALIZADO PARA SALTOS DE LÍNEA ---
    prompt = f"""Eres @DobleFaltaTenis. Genera UN tweet sobre los partidos {tipo}.
    REGLAS: 
    1. Máximo 270 caracteres. Sin asteriscos.
    2. ESTRUCTURA: Una línea de intro, UN SALTO DE LÍNEA por cada resultado de partido, una línea de cierre.
    3. NARRATIVA:
       - FINALIZADO: Perdió partido que iba ganando = "se le escapó".
       - FINALIZADO: Empezó perdiendo y ganó = "¡LO DIO VUELTA!".
       - FINALIZADO: Ganó a un mejor ranking = "¡HAZAÑA!", "batacazo".
       - EN JUEGO: Empate en sets = "partido durísimo".
    4. Datos:
    {datos}
    Devuelve ÚNICAMENTE el texto del tweet."""
    
    try: return model.generate_content(prompt).text.strip()
    except: return None

# ==========================================
# 4. MOTOR PRINCIPAL
# ==========================================
if __name__ == "__main__":
    TIPO_DE_REPORTE = "AGENDA" 
    
    print(f"🚀 INICIANDO BOT DOBLE FALTA - MODO: {TIPO_DE_REPORTE} 🚀\n")

    if TIPO_DE_REPORTE == "AGENDA":
        partidos = obtener_agenda_hoy()
        if partidos:
            agrupados = agrupar_agenda(partidos)
            for cat, lista in agrupados.items():
                if lista:
                    tweet = generar_tweet_agenda(cat, lista)
                    print(f"\n--- TWEET {cat} ---\n{tweet}\n{'-'*40}")

    elif TIPO_DE_REPORTE == "ACTUALIZACION":
        data = obtener_actualizaciones()
        if data['en_juego']:
            tweet = generar_tweet_actualizacion("EN JUEGO", data['en_juego'])
            print(f"\n--- TWEET EN JUEGO ---\n{tweet}\n{'-'*40}")
        if data['finalizados']:
            tweet = generar_tweet_actualizacion("FINALIZADOS", data['finalizados'])
            print(f"\n--- TWEET FINALIZADOS ---\n{tweet}\n{'-'*40}")