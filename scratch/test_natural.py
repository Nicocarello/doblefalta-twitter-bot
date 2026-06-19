import random

def test_oracion_agenda():
    partidos = [
        {"hora": "14:00", "j1": "Fran Cerúndolo (27°)", "j2": "Sinner (1°)", "ronda": "4tos", "derbi": False, "arg_es_j1": True},
        {"hora": "S/H", "j1": "Alcaraz (2°)", "j2": "Seba Báez (30°)", "ronda": "Semifinal", "derbi": False, "arg_es_j1": False},
        {"hora": "16:30", "j1": "Fede Coria", "j2": "Díaz Acosta", "ronda": "R1", "derbi": True, "arg_es_j1": True},
    ]

    for p in partidos:
        hora = p['hora']
        ronda = p['ronda']
        j1_str = p['j1']
        j2_str = p['j2']
        
        comienzos = [
            f"A las {hora},",
            f"Desde las {hora},",
            f"A partir de las {hora},",
            f"En el turno de las {hora},"
        ] if hora != 'S/H' else ["En horario a confirmar,", "Sin horario definido todavía,"]
        
        comienzo = random.choice(comienzos)
        verbos = [
            "se medirá ante",
            "jugará contra",
            "se enfrentará a",
            "chocará contra",
            "irá frente a",
            "buscará avanzar ante"
        ]
        verbo = random.choice(verbos)
        
        texto_ronda = f" (por los {ronda})" if ronda and ronda not in ["Qualy", "R1", "R2", "R3", "Ronda"] else ""
        if "Qualy" in ronda: texto_ronda = f" (por la {ronda})"
        elif ronda in ["R1", "R2", "R3", "Ronda"]: texto_ronda = f" (por la {ronda})"
        
        if p['derbi']:
             oracion = f"🎾 {comienzo} tendremos un hermoso DERBI 🇦🇷: {j1_str} {verbo} {j2_str}{texto_ronda}."
        else:
            if p['arg_es_j1']:
                oracion = f"🎾 {comienzo} {j1_str} {verbo} {j2_str}{texto_ronda}."
            else:
                oracion = f"🎾 {comienzo} {j2_str} {verbo} {j1_str}{texto_ronda}."
                
        print(oracion)

def test_oracion_finalizado():
    partidos = [
        {"j1": "Fran Cerúndolo (27°)", "j2": "Sinner (1°)", "ronda": "4tos", "derbi": False, "arg_es_j1": True, "gano": False, "marcador": "6-4 / 6-3"},
        {"j1": "Alcaraz (2°)", "j2": "Seba Báez (30°)", "ronda": "Semifinal", "derbi": False, "arg_es_j1": False, "gano": True, "marcador": "4-6 / 6-3 / 7-6"},
        {"j1": "Fede Coria", "j2": "Díaz Acosta", "ronda": "R1", "derbi": True, "arg_es_j1": True, "gano": None, "marcador": "6-2 / 6-2", "ganador_str": "Fede Coria", "perdedor_str": "Díaz Acosta"},
    ]

    for p in partidos:
        ronda = p['ronda']
        marcador = p['marcador']
        j1_str = p['j1']
        j2_str = p['j2']
        gano = p['gano']
        
        texto_ronda = f" por los {ronda}" if ronda and ronda not in ["Qualy", "Final", "R1", "R2", "R3", "Ronda"] else ""
        if "Qualy" in ronda: texto_ronda = f" en la {ronda}"
        elif ronda == "Final": texto_ronda = f" en la gran Final"
        elif ronda in ["R1", "R2", "R3", "Ronda"]: texto_ronda = f" en la {ronda}"

        if p['derbi']:
             oracion = f"🇦🇷 DERBI: ¡Ganó {p['ganador_str']}! Superó a {p['perdedor_str']} por {marcador}{texto_ronda}."
        else:
            if p['arg_es_j1']:
                arg_str, riv_str = j1_str, j2_str
            else:
                arg_str, riv_str = j2_str, j1_str
                
            if gano:
                verbos_victoria = ["superó a", "venció a", "derrotó a", "le ganó a", "se impuso ante"]
                v = random.choice(verbos_victoria)
                oracion = f"✅ ¡Triunfo argentino! {arg_str} {v} {riv_str} por {marcador}{texto_ronda}."
            else:
                verbos_derrota = ["cayó ante", "no pudo con", "fue derrotado por", "perdió con"]
                v = random.choice(verbos_derrota)
                oracion = f"❌ Fin del camino para {arg_str}. {v.capitalize()} {riv_str} por {marcador}{texto_ronda}."
                
        print(oracion)

print("--- AGENDA ---")
test_oracion_agenda()
print("\n--- FINALIZADOS ---")
test_oracion_finalizado()
