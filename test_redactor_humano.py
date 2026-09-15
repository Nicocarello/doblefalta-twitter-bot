import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from bot.redactor import (
    generar_tweet_agenda,
    generar_tweet_actualizacion,
    generar_tweet_finalizado,
    generar_tweet_ranking,
    generar_hilo_ranking_argentinos
)

def verificar_longitud(tweets, nombre_caso):
    for i, t in enumerate(tweets):
        # Limpiar marcadores de inicio/fin
        lineas = [l for l in t.split('\n') if not l.startswith('---')]
        limpio = "\n".join(lineas).strip()
        largo = len(limpio)
        print(f"[{nombre_caso} - Tweet {i+1}] ({largo} caracteres)")
        print(limpio)
        print("-" * 50)
        assert largo <= 280, f"Error: Tweet excede 280 caracteres ({largo}):\n{limpio}"

def main():
    print("=" * 60)
    print("🎾 PRUEBA INTEGRAL DE REDACCIÓN DE TWEETS HUMANIZADOS 🎾")
    print("=" * 60)

    # 1. Partido Único - Agenda
    p_agenda_single = [{
        'tournament_name': 'Rome',
        'event_type_type': 'ATP',
        'event_time': '11:00',
        'event_first_player': 'Francisco Cerundolo',
        'event_second_player': 'Alexander Zverev',
        'tournament_round': 'Rome - Quarter-finals',
        'arg_info': {
            'jugador_1': {'es_arg': True, 'ranking': 30, 'pais': 'Argentina'},
            'jugador_2': {'es_arg': False, 'ranking': 4, 'pais': 'Germany'}
        }
    }]
    t_agenda_single = generar_tweet_agenda("Rome", p_agenda_single)
    verificar_longitud(t_agenda_single, "1. Agenda Partido Único")

    # 2. Duelo Argentino - Agenda
    p_agenda_derbi = [{
        'tournament_name': 'Buenos Aires',
        'event_type_type': 'ATP',
        'event_time': '16:00',
        'event_first_player': 'Francisco Cerundolo',
        'event_second_player': 'Sebastian Baez',
        'tournament_round': 'Buenos Aires - Semi-finals',
        'arg_info': {
            'jugador_1': {'es_arg': True, 'ranking': 30, 'pais': 'Argentina'},
            'jugador_2': {'es_arg': True, 'ranking': 25, 'pais': 'Argentina'}
        }
    }]
    t_agenda_derbi = generar_tweet_agenda("Buenos Aires", p_agenda_derbi)
    verificar_longitud(t_agenda_derbi, "2. Agenda Duelo Argentino")

    # 3. Agenda Múltiple
    p_agenda_multi = [
        {
            'tournament_name': 'Roland Garros',
            'event_type_type': 'ATP',
            'event_time': '09:00',
            'event_first_player': 'Tomas Martin Etcheverry',
            'event_second_player': 'Casper Ruud',
            'tournament_round': 'Roland Garros - Round 2',
            'arg_info': {
                'jugador_1': {'es_arg': True, 'ranking': 32, 'pais': 'Argentina'},
                'jugador_2': {'es_arg': False, 'ranking': 8, 'pais': 'Norway'}
            }
        },
        {
            'tournament_name': 'Roland Garros',
            'event_type_type': 'WTA',
            'event_time': '12:30',
            'event_first_player': 'Lourdes Carle',
            'event_second_player': 'Aryna Sabalenka',
            'tournament_round': 'Roland Garros - Round 2',
            'arg_info': {
                'jugador_1': {'es_arg': True, 'ranking': 75, 'pais': 'Argentina'},
                'jugador_2': {'es_arg': False, 'ranking': 2, 'pais': 'Belarus'}
            }
        },
        {
            'tournament_name': 'Roland Garros',
            'event_type_type': 'ATP',
            'event_time': '15:00',
            'event_first_player': 'Mariano Navone',
            'event_second_player': 'Taylor Fritz',
            'tournament_round': 'Roland Garros - Round 2',
            'arg_info': {
                'jugador_1': {'es_arg': True, 'ranking': 35, 'pais': 'Argentina'},
                'jugador_2': {'es_arg': False, 'ranking': 12, 'pais': 'USA'}
            }
        }
    ]
    t_agenda_multi = generar_tweet_agenda("Roland Garros", p_agenda_multi)
    verificar_longitud(t_agenda_multi, "3. Agenda Múltiple")

    # 4. Partido Único - Victoria Narrativa
    p_fin_single_win = [{
        'tournament_name': 'Rome',
        'event_type_type': 'ATP',
        'event_first_player': 'Francisco Cerundolo',
        'first_player_key': '1',
        'event_second_player': 'Alexander Zverev',
        'second_player_key': '2',
        'event_status': 'Finished',
        'event_winner': 'First Player',
        'event_final_result': '2 - 1',
        'tournament_round': 'Rome - Quarter-finals',
        'scores': [
            {'score_first': '6', 'score_second': '4'},
            {'score_first': '3', 'score_second': '6'},
            {'score_first': '7.4', 'score_second': '6'}
        ],
        'arg_info': {
            'jugador_1': {'es_arg': True, 'ranking': 30, 'pais': 'Argentina'},
            'jugador_2': {'es_arg': False, 'ranking': 4, 'pais': 'Germany'}
        }
    }]
    t_fin_single_win = generar_tweet_finalizado("Rome", p_fin_single_win)
    verificar_longitud(t_fin_single_win, "4. Finalizado Partido Único (Victoria)")

    # 5. Partido Único - Derrota Ajustada
    p_fin_single_loss = [{
        'tournament_name': 'Rome',
        'event_type_type': 'ATP',
        'event_first_player': 'Sebastian Baez',
        'first_player_key': '1',
        'event_second_player': 'Rafael Nadal',
        'second_player_key': '2',
        'event_status': 'Finished',
        'event_winner': 'Second Player',
        'event_final_result': '1 - 2',
        'tournament_round': 'Rome - Quarter-finals',
        'scores': [
            {'score_first': '7.5', 'score_second': '6'},
            {'score_first': '4', 'score_second': '6'},
            {'score_first': '4', 'score_second': '6'}
        ],
        'arg_info': {
            'jugador_1': {'es_arg': True, 'ranking': 25, 'pais': 'Argentina'},
            'jugador_2': {'es_arg': False, 'ranking': 100, 'pais': 'Spain'}
        }
    }]
    t_fin_single_loss = generar_tweet_finalizado("Rome", p_fin_single_loss)
    verificar_longitud(t_fin_single_loss, "5. Finalizado Partido Único (Derrota)")

    # 6. Duelo Argentino - Finalizado
    p_fin_derbi = [{
        'tournament_name': 'Buenos Aires',
        'event_type_type': 'ATP',
        'event_first_player': 'Francisco Cerundolo',
        'first_player_key': '1',
        'event_second_player': 'Sebastian Baez',
        'second_player_key': '2',
        'event_status': 'Finished',
        'event_winner': 'First Player',
        'event_final_result': '2 - 0',
        'tournament_round': 'Buenos Aires - Semi-finals',
        'scores': [
            {'score_first': '6', 'score_second': '4'},
            {'score_first': '6', 'score_second': '3'}
        ],
        'arg_info': {
            'jugador_1': {'es_arg': True, 'ranking': 30, 'pais': 'Argentina'},
            'jugador_2': {'es_arg': True, 'ranking': 25, 'pais': 'Argentina'}
        }
    }]
    t_fin_derbi = generar_tweet_finalizado("Buenos Aires", p_fin_derbi)
    verificar_longitud(t_fin_derbi, "6. Finalizado Duelo Argentino")

    # 7. Múltiples Partidos - Finalizados (Resumen)
    p_fin_multi = [
        {
            'tournament_name': 'Challenger Coquimbo',
            'event_type_type': 'Challenger',
            'event_first_player': 'Juan Manuel Cerundolo',
            'first_player_key': '1',
            'event_second_player': 'H. Dellien',
            'second_player_key': '2',
            'event_status': 'Finished',
            'event_winner': 'First Player',
            'event_final_result': '2 - 0',
            'tournament_round': '1/4-finals',
            'scores': [
                {'score_first': '6', 'score_second': '3'},
                {'score_first': '6', 'score_second': '2'}
            ],
            'arg_info': {
                'jugador_1': {'es_arg': True, 'ranking': 120, 'pais': 'Argentina'},
                'jugador_2': {'es_arg': False, 'ranking': 110, 'pais': 'Bolivia'}
            }
        },
        {
            'tournament_name': 'Challenger Coquimbo',
            'event_type_type': 'Challenger',
            'event_first_player': 'Facundo Bagnis',
            'first_player_key': '3',
            'event_second_player': 'P. Sakamoto',
            'second_player_key': '4',
            'event_status': 'Finished',
            'event_winner': 'Second Player',
            'event_final_result': '1 - 2',
            'tournament_round': '1/4-finals',
            'scores': [
                {'score_first': '6', 'score_second': '4'},
                {'score_first': '4', 'score_second': '6'},
                {'score_first': '3', 'score_second': '6'}
            ],
            'arg_info': {
                'jugador_1': {'es_arg': True, 'ranking': 150, 'pais': 'Argentina'},
                'jugador_2': {'es_arg': False, 'ranking': 220, 'pais': 'Brazil'}
            }
        }
    ]
    t_fin_multi = generar_tweet_finalizado("Challenger Coquimbo", p_fin_multi)
    verificar_longitud(t_fin_multi, "7. Resumen de Múltiples Partidos")

    # 8. Rankings
    mock_ranking = [
        {'place': '1', 'player': 'Jannik Sinner', 'country': 'Italy', 'points': '10330'},
        {'place': '2', 'player': 'Carlos Alcaraz', 'country': 'Spain', 'points': '7500'},
        {'place': '3', 'player': 'Alexander Zverev', 'country': 'Germany', 'points': '7000'},
        {'place': '25', 'player': 'Sebastian Baez', 'country': 'Argentina', 'points': '1800'},
        {'place': '30', 'player': 'Francisco Cerundolo', 'country': 'Argentina', 'points': '1500'},
        {'place': '35', 'player': 'Tomas Martin Etcheverry', 'country': 'Argentina', 'points': '1350'},
    ]
    t_ranking = generar_tweet_ranking(mock_ranking, "atp")
    verificar_longitud([t_ranking], "8. Top 10 Ranking ATP")

    t_hilo_arg = generar_hilo_ranking_argentinos(mock_ranking, "atp")
    verificar_longitud(t_hilo_arg, "9. Hilo Argentinos Ranking ATP")

    print("\n🎉 ¡TODAS LAS PRUEBAS DE FORMATO Y LONGITUD PASARON EXITOSAMENTE!")

if __name__ == '__main__':
    main()
