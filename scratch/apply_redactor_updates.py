import re

file_path = "bot/redactor.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Definir helper functions y generar_tweet_resultado_unico
helpers_and_single = """def obtener_nombre_balance(nombre_completo):
    \"\"\"Devuelve el apellido o nombre corto para la lista del balance diario.\"\"\"
    if not nombre_completo:
        return ""
    norm = nombre_completo.lower().strip()
    mapeo = {
        "francisco cerundolo": "F. Cerúndolo",
        "f. cerundolo": "F. Cerúndolo",
        "juan manuel cerundolo": "J.M. Cerúndolo",
        "j. cerundolo": "J.M. Cerúndolo",
        "j. m. cerundolo": "J.M. Cerúndolo",
        "sebastian baez": "Báez",
        "s. baez": "Báez",
        "tomas martin etcheverry": "Etcheverry",
        "tomas etcheverry": "Etcheverry",
        "t. etcheverry": "Etcheverry",
        "t. m. etcheverry": "Etcheverry",
        "mariano navone": "Navone",
        "m. navone": "Navone",
        "facundo diaz acosta": "Díaz Acosta",
        "f. diaz acosta": "Díaz Acosta",
        "camilo ugo carabelli": "Ugo Carabelli",
        "c. ugo carabelli": "Ugo Carabelli",
        "federico coria": "Coria",
        "f. coria": "Coria",
        "facundo bagnis": "Bagnis",
        "f. bagnis": "Bagnis",
        "thiago agustin tirante": "Tirante",
        "thiago tirante": "Tirante",
        "t. tirante": "Tirante",
        "nadia podoroska": "Podoroska",
        "n. podoroska": "Podoroska",
        "lourdes carle": "Carlé",
        "l. carle": "Carlé",
        "julia riera": "Riera",
        "j. riera": "Riera",
        "solana sierra": "Sierra",
        "s. sierra": "Sierra",
        "francisco comesaña": "Comesaña",
        "f. comesaña": "Comesaña",
        "francisco comesana": "Comesaña",
        "f. comesana": "Comesaña",
        "federico gomez": "F. Gómez",
        "f. gomez": "F. Gómez",
        "juan pablo ficovich": "Ficovich",
        "j. p. ficovich": "Ficovich",
        "lautaro midon": "Midón",
        "l. midon": "Midón",
        "alberto olivieri genaro": "Olivieri",
        "a. olivieri genaro": "Olivieri",
        "bautista torres juan": "Torres",
        "b. torres juan": "Torres",
        "manuel la serna juan": "La Serna",
        "m. la serna juan": "La Serna",
        "benjamin chelia": "Chelia",
        "b. chelia": "Chelia",
        "facundo mena": "Mena",
        "f. mena": "Mena",
        "santiago rodriguez taverna": "Taverna",
        "s. rodriguez taverna": "Taverna",
        "gonzalo villanueva": "Villanueva",
        "g. villanueva": "Villanueva",
        "emanuel ambrogi luciano": "Ambrogi",
        "e. ambrogi luciano": "Ambrogi",
        "jazmin ortenzi": "Ortenzi",
        "j. ortenzi": "Ortenzi"
    }
    if norm in mapeo:
        return mapeo[norm]
        
    partes = nombre_completo.split()
    if len(partes) > 1:
        return partes[-1].title()
    return nombre_completo.title()

def formatear_lista_con_y(lista):
    \"\"\"Junta una lista de nombres con comas y una 'y' para el último elemento.\"\"\"
    if not lista:
        return ""
    if len(lista) == 1:
        return lista[0]
    return ", ".join(lista[:-1]) + " y " + lista[-1]

def generar_tweet_resultado_unico(partido, torneo_original):
    \"\"\"
    Genera el texto de resultado final para un único partido (Modo Single).
    Usa el formato narrativo sumamente conversacional.
    \"\"\"
    torneo = traducir_nombre_torneo(torneo_original)
    cat = extraer_categoria(partido)
    
    # Emojis de país del torneo
    bandera_torneo = obtener_bandera(torneo)
    if not bandera_torneo:
        bandera_torneo = "🎾"
        
    # Cabecera del torneo (ej: "Ch75 🇮🇹 Vicenza 🇮🇹")
    prefijo_torneo = f"{cat} {torneo}" if cat else torneo
    cabecera = f"{prefijo_torneo} {bandera_torneo}"
    
    j1 = partido.get('event_first_player')
    j2 = partido.get('event_second_player')
    
    info = partido.get('arg_info', {})
    pais1 = info.get('jugador_1', {}).get('pais', '')
    pais2 = info.get('jugador_2', {}).get('pais', '')
    
    j1_es_arg = info.get('jugador_1', {}).get('es_arg', False)
    j2_es_arg = info.get('jugador_2', {}).get('es_arg', False)
    
    # Determinar ganador
    final_res = partido.get('event_final_result', "0 - 0")
    try:
        s1, s2 = map(int, final_res.split(" - "))
    except:
        s1, s2 = 0, 0
    ganador = 1 if s1 > s2 else (2 if s2 > s1 else 0)
    
    # Formatear sets
    scores_api = partido.get('scores', [])
    sets_formateados = formatear_sets_single(scores_api, ganador)
    if not sets_formateados:
        sets_formateados = final_res.replace(" - ", " ")
        
    ronda_actual = partido.get('tournament_round', '')
    ronda_siguiente = obtener_siguiente_ronda_texto(ronda_actual)
    
    status = partido.get('event_status', '').lower()
    es_retiro = status in ['retired', 'walkover', 'w.o.', 'ret.'] or 'retired' in status or 'walkover' in status
    tipo_retiro = "retiro" if ("ret" in status or "retired" in status) else "W.O."
    
    # Si es un Derbi Argentino
    if es_derbi_argentino(pais1, pais2):
        if ganador == 1:
            nom_ganador = obtener_nombre_variante(j1)
            nom_perdedor = obtener_nombre_variante(j2)
        else:
            nom_ganador = obtener_nombre_variante(j2)
            nom_perdedor = obtener_nombre_variante(j1)
            
        if es_retiro:
            cuerpo = f"¡Victoria de {nom_ganador}! 🎉\\nCon un {sets_formateados} le ganó a {nom_perdedor} por {tipo_retiro}, ¡está seguro en {ronda_siguiente}! 🚀"
        else:
            cuerpo = f"¡Victoria de {nom_ganador}! 🎉\\nCon un sólido {sets_formateados} se quedó con el derbi ante {nom_perdedor}, ¡está seguro en {ronda_siguiente}! 🚀"
            
        texto = f"{cabecera}\\n\\ncuerpo\\n\\n¡Partidazo de ambos! 🇦🇷"
        # Reemplazar la palabra 'cuerpo' literal por la variable en la ejecucion real
        texto = texto.replace("cuerpo", cuerpo)
        return [f"--- INICIO TWEET ---\\n{texto}\\n--- FIN TWEET ---"]

    # Caso en que gane o pierda el argentino contra un extranjero
    if j1_es_arg:
        arg_completo = j1
        arg_apodo = obtener_nombre_variante(j1)
        riv_nombre = j2
        riv_pais_code = obtener_codigo_pais(pais2)
        arg_ganó = (ganador == 1)
    else:
        arg_completo = j2
        arg_apodo = obtener_nombre_variante(j2)
        riv_nombre = j1
        riv_pais_code = obtener_codigo_pais(pais1)
        arg_ganó = (ganador == 2)
        
    # Obtener frase de aliento basada en el apodo
    nombre_aliento = arg_apodo.replace("@", "") if arg_apodo.startswith("@") else arg_apodo
    nombre_aliento = nombre_aliento.split()[0]
    
    frase_aliento = f"Dale {nombre_aliento}!!"
    
    if arg_ganó:
        # Victoria
        if es_retiro:
            cuerpo = f"¡Bien {arg_apodo}! 🎉\\nPor {tipo_retiro} de {riv_nombre} ({riv_pais_code}) con marcador {sets_formateados}, ¡está seguro en {ronda_siguiente}! 🚀"
        else:
            adjetivos = ["sólido", "batallado", "partidazo", "gran triunfo"]
            adj = random.choice(adjetivos)
            cuerpo = f"¡Bien {arg_apodo}!! 🎉\\nCon un {adj} {sets_formateados} le ganó a {riv_nombre} ({riv_pais_code}), ¡está seguro en {ronda_siguiente}! 🚀"
            
        texto = f"{cabecera}\\n\\n{cuerpo}\\n\\n{frase_aliento} 🇦🇷"
    else:
        # Derrota
        if es_retiro:
            cuerpo = f"No pudo ser para {arg_apodo} 😢\\nDebió retirarse por {tipo_retiro} con marcador {sets_formateados} ante {riv_nombre} ({riv_pais_code}) y se despide de {torneo}."
        else:
            cuerpo = f"No pudo ser para {arg_apodo} 😢\\nCayó por {sets_formateados} ante {riv_nombre} ({riv_pais_code}) y se despide de {torneo}."
            
        texto = f"{cabecera}\\n\\n{cuerpo}\\n\\n¡A levantar cabeza y pensar en lo que viene, {nombre_aliento}! 💪"
        
    return [f"--- INICIO TWEET ---\\n{texto}\\n--- FIN TWEET ---"]
"""

# 2. Reemplazo de generar_tweet_finalizado completo
new_generar_tweet_finalizado = """def generar_tweet_finalizado(torneo_original, partidos):
    \"\"\"Genera el texto para resultados finales con análisis de victoria/derrota.\"\"\"
    if not partidos:
        return []
        
    # Modo Single si es solo un partido
    if len(partidos) == 1:
        return generar_tweet_resultado_unico(partidos[0], torneo_original)
        
    # Modo Balance Diario si son múltiples partidos
    torneo = traducir_nombre_torneo(torneo_original)
    cat = extraer_categoria(partidos[0])
    tag_torneo = obtener_hashtag_torneo(torneo, cat)
    
    ronda_api = partidos[0].get('tournament_round', '')
    ronda = traducir_ronda(ronda_api).upper()
    if not ronda:
        ronda = "JORNADA"
        
    es_gs = any(gs in torneo.lower() for gs in ["roland garros", "wimbledon", "us open", "australian open"])
    prefijo_torneo = torneo if es_gs else f"{cat} {torneo}".strip()
    
    ganadores = []
    perdedores = []
    
    for p in partidos:
        j1 = p.get('event_first_player')
        j2 = p.get('event_second_player')
        
        info = p.get('arg_info', {})
        pais1 = info.get('jugador_1', {}).get('pais', '')
        pais2 = info.get('jugador_2', {}).get('pais', '')
        
        j1_es_arg = info.get('jugador_1', {}).get('es_arg', False)
        j2_es_arg = info.get('jugador_2', {}).get('es_arg', False)
        
        final_res = p.get('event_final_result', "0 - 0")
        try:
            s1, s2 = map(int, final_res.split(" - "))
        except:
            s1, s2 = 0, 0
        ganador = 1 if s1 > s2 else (2 if s2 > s1 else 0)
        
        if es_derbi_argentino(pais1, pais2):
            if ganador == 1:
                ganadores.append(obtener_nombre_balance(j1))
                perdedores.append(obtener_nombre_balance(j2))
            else:
                ganadores.append(obtener_nombre_balance(j2))
                perdedores.append(obtener_nombre_balance(j1))
        else:
            _, gano = analizar_resultado_argentino(p)
            if j1_es_arg:
                nombre_arg = obtener_nombre_balance(j1)
            else:
                nombre_arg = obtener_nombre_balance(j2)
                
            if gano is True:
                ganadores.append(nombre_arg)
            elif gano is False:
                perdedores.append(nombre_arg)
                
    total_v = len(ganadores)
    total_d = len(perdedores)
    
    # Armar el tweet de balance
    lineas = [f"EL BALANCE DE LOS ARGENTINOS EN LA {ronda} DE {prefijo_torneo.upper()}."]
    lineas.append("")
    lineas.append(f"🇦🇷 ARGENTINA: {total_v}-{total_d}")
    
    if ganadores:
        lineas.append(f"✅ {formatear_lista_con_y(ganadores)}")
    if perdedores:
        lineas.append(f"❌ {formatear_lista_con_y(perdedores)}")
        
    lineas.append("")
    lineas.append(tag_torneo)
    
    texto = "\\n".join(lineas)
    return [f"--- INICIO TWEET ---\\n{texto}\\n--- FIN TWEET ---"]"""

# Encontrar el inicio de generar_tweet_finalizado y reemplazarlo
func_start = content.find("def generar_tweet_finalizado(torneo_original, partidos):")
if func_start == -1:
    raise Exception("No se encontró def generar_tweet_finalizado")

# Encontrar el inicio de la siguiente función (generar_tweet_ranking)
next_func = content.find("def generar_tweet_ranking(datos, tipo=\"atp\"):")
if next_func == -1:
    raise Exception("No se encontró def generar_tweet_ranking")

# Reemplazar toda esa sección
modified_content = content[:func_start] + helpers_and_single + "\n" + new_generar_tweet_finalizado + "\n" + content[next_func:]

with open(file_path, "w", encoding="utf-8") as f:
    f.write(modified_content)

print("Modificaciones aplicadas con éxito a bot/redactor.py!")
