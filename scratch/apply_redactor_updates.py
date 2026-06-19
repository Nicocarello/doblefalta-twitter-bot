import os

file_path = r"c:\Users\nico_\OneDrive\Desktop\PROYECTOS\BOT TWITTER TENIS\bot\redactor.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# REPLACE 1: generar_tweet_agenda
old_agenda_str = """        ronda = traducir_ronda(p.get('tournament_round', ''))
        prefijo_partido = f"• [{ronda}] " if ronda else "• "
        
        qualy = " (Qualy)" if (p.get('es_qualy') and not todos_qualy) else ""
        
        j1_str = _formatear_jugador_completo(j1, flag1, r1_str)
        j2_str = _formatear_jugador_completo(j2, flag2, r2_str)
        
        # Si es un derbi argentino, anotarlo claramente
        if es_derbi_argentino(pais1, pais2):
            line = f"{prefijo_partido}{hora} | {j1_str} vs {j2_str}{qualy}  — DERBI 🇦🇷🇦🇷"
        else:
            line = f"{prefijo_partido}{hora} | {j1_str} vs {j2_str}{qualy}"
        lineas_partidos.append(line)"""

new_agenda_str = """        ronda = traducir_ronda(p.get('tournament_round', ''))
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
                
        lineas_partidos.append(line)"""

# REPLACE 2: generar_tweet_finalizado
old_final_str = """        ronda = traducir_ronda(p.get('tournament_round', ''))
        prefijo_partido = f"• [{ronda}] " if ronda else "• "
        
        scores_api = p.get('scores', [])
        sets_formateados = formatear_sets(scores_api)
        
        marcador = sets_formateados if sets_formateados else p.get('event_final_result', '0-0')
        j1_str = _formatear_jugador_completo(j1, flag1, r1_str)
        j2_str = _formatear_jugador_completo(j2, flag2, r2_str)
        
        es_qualy = p.get('es_qualy', False)
        es_gs = any(gs in torneo.lower() for gs in ["roland garros", "wimbledon", "us open", "australian open"])
        prefijo_torneo = torneo if es_gs else f"{cat} {torneo}".strip()

        # Si es un derbi argentino, no lo contamos en el balance nacional, solo lo anotamos
        if es_derbi_argentino(pais1, pais2):
            try:
                s1, s2 = map(int, p.get('event_final_result', '0 - 0').split(' - '))
            except:
                s1, s2 = 0, 0
                
            status_low = p.get('event_status', '').lower()
            es_retiro = status_low in ['retired', 'walkover', 'w.o.', 'ret.'] or 'retired' in status_low or 'walkover' in status_low
            tipo_retiro = "retiro" if ("ret" in status_low or "retired" in status_low) else "W.O."
            
            if es_retiro:
                if s1 > s2:
                    msg_result = f"DERBI ARGENTINO: ganó {j1} por {tipo_retiro} de {j2} 🇦🇷"
                elif s2 > s1:
                    msg_result = f"DERBI ARGENTINO: ganó {j2} por {tipo_retiro} de {j1} 🇦🇷"
                else:
                    msg_result = f"DERBI ARGENTINO: ganó por {tipo_retiro} 🇦🇷"
            else:
                if s1 > s2:
                    msg_result = f"DERBI ARGENTINO: ganó {j1} 🇦🇷"
                elif s2 > s1:
                    msg_result = f"DERBI ARGENTINO: ganó {j2} 🇦🇷"
                else:
                    msg_result = "DERBI ARGENTINO"
            gano = None
            line = f"{prefijo_partido}{j1_str} vs {j2_str}: {marcador} {msg_result}"
        elif es_qualy:
            msg_result, gano = analizar_resultado_argentino(p)
            if gano is True: total_victorias += 1
            elif gano is False: total_derrotas += 1
            
            j1_es_arg = info.get('jugador_1', {}).get('es_arg', False)
            if j1_es_arg:
                arg_str = j1_str
                riv_str = j2_str
            else:
                arg_str = j2_str
                riv_str = j1_str
                
            if ronda == "Final":
                if gano:
                    line = f"{prefijo_partido}{arg_str} ganó {marcador} a {riv_str} y entró al cuadro principal de {prefijo_torneo} 🇦🇷"
                else:
                    line = f"{prefijo_partido}{arg_str} cayó {marcador} ante {riv_str} y no pudo entrar al cuadro principal de {prefijo_torneo} 😢"
            else:
                if gano:
                    line = f"{prefijo_partido}{arg_str} ganó {marcador} a {riv_str} y avanza en la qualy de {prefijo_torneo} 💪"
                else:
                    line = f"{prefijo_partido}{arg_str} cayó {marcador} ante {riv_str} y quedó eliminado en la qualy de {prefijo_torneo} 😢"
        else:
            msg_result, gano = analizar_resultado_argentino(p)
            if gano is True: total_victorias += 1
            elif gano is False: total_derrotas += 1
            line = f"{prefijo_partido}{j1_str} vs {j2_str}: {marcador} {msg_result}"

        lineas_partidos.append(line)"""

new_final_str = """        ronda = traducir_ronda(p.get('tournament_round', ''))
        
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

        lineas_partidos.append(line)"""

if old_agenda_str in content:
    content = content.replace(old_agenda_str, new_agenda_str)
    print("Agenda replaced successfully")
else:
    print("Agenda string not found")

if old_final_str in content:
    content = content.replace(old_final_str, new_final_str)
    print("Final replaced successfully")
else:
    print("Final string not found")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
