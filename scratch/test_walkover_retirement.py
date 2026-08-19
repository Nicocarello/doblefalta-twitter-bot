import sys
import os

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bot.redactor import generar_tweet_finalizado, determinar_ganador_partido, detectar_tipo_finalizacion, analizar_resultado_argentino
from bot.filtros import es_finalizado, es_actualizacion_en_vivo

def run_tests():
    print("=" * 60)
    print("🧪 INICIANDO PRUEBAS DE WALKOVER Y RETIRO")
    print("=" * 60)

    # 1. Caso Midón vs Marcondes (Challenger Kingston)
    p_midon_wo = {
        'tournament_name': 'Challenger Kingston',
        'event_type_type': 'Challenger',
        'tournament_round': '1/8-finals',
        'event_first_player': 'Lautaro Midon',
        'first_player_key': '101',
        'event_second_player': 'I. Marcondes',
        'second_player_key': '102',
        'event_status': 'Walkover',
        'event_winner': 'First Player',
        'event_final_result': '1 - 1',
        'scores': [
            {'score_first': '7', 'score_second': '6'},
            {'score_first': '3', 'score_second': '6'}
        ],
        'arg_info': {
            'jugador_1': {'es_arg': True, 'ranking': 193, 'pais': 'Argentina'},
            'jugador_2': {'es_arg': False, 'ranking': 316, 'pais': 'Brazil'}
        }
    }

    print("\n--- 1. Caso Midón vs Marcondes (7-6 / 3-6 con Walkover en API) ---")
    g = determinar_ganador_partido(p_midon_wo)
    tf = detectar_tipo_finalizacion(p_midon_wo)
    msg, gano = analizar_resultado_argentino(p_midon_wo)
    print(f"Ganador: {g} (Esperado: 1)")
    print(f"Tipo finalización: {tf} (Esperado: retiro)")
    print(f"Gano argentino: {gano} (Esperado: True)")
    print(f"Es finalizado: {es_finalizado(p_midon_wo)} (Esperado: True)")
    print(f"Es en vivo: {es_actualizacion_en_vivo(p_midon_wo)} (Esperado: False)")
    tweet1 = generar_tweet_finalizado("Challenger Kingston", [p_midon_wo])
    print(f"Tweet generado:\n{tweet1[0]}")
    assert g == 1, f"Fallo: ganador debió ser 1, fue {g}"
    assert gano is True, f"Fallo: gano debió ser True, fue {gano}"
    assert "Triunfo argentino" in tweet1[0] or "avanzó" in tweet1[0]
    assert "Cayó ante" not in tweet1[0]
    assert "Fin del camino" not in tweet1[0]

    # 2. Walkover puro sin juego (0-0)
    p_wo_puro = {
        'tournament_name': 'Challenger Kingston',
        'event_type_type': 'Challenger',
        'tournament_round': '1/8-finals',
        'event_first_player': 'Lautaro Midon',
        'first_player_key': '101',
        'event_second_player': 'I. Marcondes',
        'second_player_key': '102',
        'event_status': 'Walkover',
        'event_winner': 'First Player',
        'event_final_result': '0 - 0',
        'scores': [],
        'arg_info': {
            'jugador_1': {'es_arg': True, 'ranking': 193, 'pais': 'Argentina'},
            'jugador_2': {'es_arg': False, 'ranking': 316, 'pais': 'Brazil'}
        }
    }

    print("\n--- 2. Walkover puro sin juego (W.O.) ---")
    g = determinar_ganador_partido(p_wo_puro)
    tf = detectar_tipo_finalizacion(p_wo_puro)
    msg, gano = analizar_resultado_argentino(p_wo_puro)
    print(f"Ganador: {g} (Esperado: 1)")
    print(f"Tipo finalización: {tf} (Esperado: walkover)")
    print(f"Gano argentino: {gano} (Esperado: True)")
    tweet2 = generar_tweet_finalizado("Challenger Kingston", [p_wo_puro])
    print(f"Tweet generado:\n{tweet2[0]}")
    assert g == 1
    assert tf == 'walkover'
    assert gano is True
    assert "Walkover" in tweet2[0] or "W.O." in tweet2[0]
    assert "0-0" not in tweet2[0]

    # 3. Argentino se retira por lesión
    p_arg_retira = {
        'tournament_name': 'ATP Rome',
        'event_type_type': 'ATP',
        'tournament_round': 'Rome - Quarter-finals',
        'event_first_player': 'Francisco Cerundolo',
        'first_player_key': '201',
        'event_second_player': 'Jannik Sinner',
        'second_player_key': '202',
        'event_status': 'Retired',
        'event_winner': 'Second Player',
        'event_final_result': '0 - 1',
        'scores': [
            {'score_first': '4', 'score_second': '6'},
            {'score_first': '1', 'score_second': '2'}
        ],
        'arg_info': {
            'jugador_1': {'es_arg': True, 'ranking': 27, 'pais': 'Argentina'},
            'jugador_2': {'es_arg': False, 'ranking': 1, 'pais': 'Italy'}
        }
    }

    print("\n--- 3. Argentino se retira por lesión ---")
    g = determinar_ganador_partido(p_arg_retira)
    tf = detectar_tipo_finalizacion(p_arg_retira)
    msg, gano = analizar_resultado_argentino(p_arg_retira)
    print(f"Ganador: {g} (Esperado: 2)")
    print(f"Tipo finalización: {tf} (Esperado: retiro)")
    print(f"Gano argentino: {gano} (Esperado: False)")
    tweet3 = generar_tweet_finalizado("ATP Rome", [p_arg_retira])
    print(f"Tweet generado:\n{tweet3[0]}")
    assert g == 2
    assert tf == 'retiro'
    assert gano is False
    assert "retir" in tweet3[0].lower()

    # 4. Derbi Argentino con retiro
    p_derbi_ret = {
        'tournament_name': 'ATP Buenos Aires',
        'event_type_type': 'ATP',
        'tournament_round': 'Buenos Aires - Semi-finals',
        'event_first_player': 'Francisco Cerundolo',
        'first_player_key': '201',
        'event_second_player': 'Sebastian Baez',
        'second_player_key': '203',
        'event_status': 'Retired',
        'event_winner': 'First Player',
        'event_final_result': '1 - 0',
        'scores': [
            {'score_first': '6', 'score_second': '3'},
            {'score_first': '2', 'score_second': '1'}
        ],
        'arg_info': {
            'jugador_1': {'es_arg': True, 'ranking': 27, 'pais': 'Argentina'},
            'jugador_2': {'es_arg': True, 'ranking': 30, 'pais': 'Argentina'}
        }
    }

    print("\n--- 4. Derbi Argentino con retiro ---")
    g = determinar_ganador_partido(p_derbi_ret)
    tf = detectar_tipo_finalizacion(p_derbi_ret)
    print(f"Ganador: {g} (Esperado: 1)")
    print(f"Tipo finalización: {tf} (Esperado: retiro)")
    tweet4 = generar_tweet_finalizado("ATP Buenos Aires", [p_derbi_ret])
    print(f"Tweet generado:\n{tweet4[0]}")
    assert g == 1
    assert "DERBI" in tweet4[0]
    assert "retiro" in tweet4[0].lower()

    # 5. Derbi Argentino con Walkover
    p_derbi_wo = {
        'tournament_name': 'ATP Buenos Aires',
        'event_type_type': 'ATP',
        'tournament_round': 'Buenos Aires - Semi-finals',
        'event_first_player': 'Francisco Cerundolo',
        'first_player_key': '201',
        'event_second_player': 'Sebastian Baez',
        'second_player_key': '203',
        'event_status': 'Walkover',
        'event_winner': 'Second Player',
        'event_final_result': '0 - 0',
        'scores': [],
        'arg_info': {
            'jugador_1': {'es_arg': True, 'ranking': 27, 'pais': 'Argentina'},
            'jugador_2': {'es_arg': True, 'ranking': 30, 'pais': 'Argentina'}
        }
    }

    print("\n--- 5. Derbi Argentino con Walkover ---")
    g = determinar_ganador_partido(p_derbi_wo)
    tf = detectar_tipo_finalizacion(p_derbi_wo)
    print(f"Ganador: {g} (Esperado: 2)")
    print(f"Tipo finalización: {tf} (Esperado: walkover)")
    tweet5 = generar_tweet_finalizado("ATP Buenos Aires", [p_derbi_wo])
    print(f"Tweet generado:\n{tweet5[0]}")
    assert g == 2
    assert "DERBI" in tweet5[0]
    assert "Walkover" in tweet5[0] or "W.O." in tweet5[0]

    # 6. Victoria y Derrota normales
    p_win_norm = {
        'tournament_name': 'Rome',
        'event_type_type': 'ATP',
        'tournament_round': 'Rome - Final',
        'event_first_player': 'Francisco Cerundolo',
        'first_player_key': '201',
        'event_second_player': 'Novak Djokovic',
        'second_player_key': '999',
        'event_status': 'Finished',
        'event_winner': 'First Player',
        'event_final_result': '2 - 0',
        'scores': [
            {'score_first': '6', 'score_second': '4'},
            {'score_first': '6', 'score_second': '3'}
        ],
        'arg_info': {
            'jugador_1': {'es_arg': True, 'ranking': 27, 'pais': 'Argentina'},
            'jugador_2': {'es_arg': False, 'ranking': 1, 'pais': 'Serbia'}
        }
    }

    print("\n--- 6. Victoria Normal ---")
    g = determinar_ganador_partido(p_win_norm)
    tf = detectar_tipo_finalizacion(p_win_norm)
    msg, gano = analizar_resultado_argentino(p_win_norm)
    print(f"Ganador: {g} (Esperado: 1)")
    print(f"Tipo finalización: {tf} (Esperado: normal)")
    print(f"Gano argentino: {gano} (Esperado: True)")
    tweet6 = generar_tweet_finalizado("Rome", [p_win_norm])
    print(f"Tweet generado:\n{tweet6[0]}")
    assert g == 1
    assert tf == 'normal'
    assert gano is True
    assert "6-4 / 6-3" in tweet6[0]

    print("\n" + "=" * 60)
    print("✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
    print("=" * 60)

if __name__ == '__main__':
    run_tests()
