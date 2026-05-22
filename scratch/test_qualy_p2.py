import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from bot.redactor import generar_tweet_finalizado

partido_p2_ganador = {
    'tournament_name': 'Roland Garros',
    'event_type_type': 'WTA',
    'event_first_player': 'A. Holmgren',
    'first_player_key': '999',
    'event_second_player': 'Diaz Acosta',
    'second_player_key': '123',
    'event_status': 'Finished',
    'event_final_result': '1 - 2',
    'tournament_round': 'Roland Garros - Final',
    'scores': [
        {'score_first': '7', 'score_second': '6'},
        {'score_first': '4', 'score_second': '6'},
        {'score_first': '2', 'score_second': '6'}
    ],
    'event_qualification': 'True',
    'es_qualy': True,
    'arg_info': {
        'jugador_1': {'es_arg': False, 'ranking': 155, 'pais': 'Denmark'},
        'jugador_2': {'es_arg': True, 'ranking': 150, 'pais': 'Argentina'}
    }
}

partido_p2_perdedor = {
    'tournament_name': 'Roland Garros',
    'event_type_type': 'WTA',
    'event_first_player': 'A. Korneeva',
    'first_player_key': '888',
    'event_second_player': 'Juli Riera',
    'second_player_key': '456',
    'event_status': 'Finished',
    'event_final_result': '2 - 0',
    'tournament_round': 'Roland Garros - Final',
    'scores': [
        {'score_first': '6', 'score_second': '3'},
        {'score_first': '6', 'score_second': '2'}
    ],
    'event_qualification': 'True',
    'es_qualy': True,
    'arg_info': {
        'jugador_1': {'es_arg': False, 'ranking': 100, 'pais': 'Neutral'},
        'jugador_2': {'es_arg': True, 'ranking': 180, 'pais': 'Argentina'}
    }
}

print("🧪 PROBANDO ARGENTINO COMO JUGADOR 2 EN FINALES DE QUALY 🧪")
tweets = generar_tweet_finalizado("Roland Garros", [partido_p2_ganador, partido_p2_perdedor])
for t in tweets:
    print(t)
