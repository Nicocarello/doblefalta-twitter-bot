import sys
from bot.api_tennis import TennisAPI
from bot.filtros import filtrar_argentinos, agrupar_por_torneo, es_agenda, es_actualizacion_en_vivo, es_finalizado
from bot.redactor import generar_tweet_agenda, generar_tweet_actualizacion, generar_tweet_finalizado

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

class MockAPI(TennisAPI):
    def obtener_info_jugador(self, player_key):
        arg_keys = ['123', '456', '789', 'CORIA', 'BAGNIS']
        if player_key in arg_keys:
            return {'es_arg': True, 'ranking': 30}
        return {'es_arg': False, 'ranking': 100}

    def obtener_partidos_hoy(self, fecha_iso):
        return [
            # AGENDA
            {
                'tournament_name': 'Roma',
                'event_type_type': 'ATP Men Singles',
                'event_time': '10:00',
                'event_first_player': 'Francisco Cerundolo',
                'first_player_key': '123',
                'event_second_player': 'Novak Djokovic',
                'second_player_key': '999',
                'event_status': '',
                'event_qualification': 'False'
            },
            # VIVO
            {
                'tournament_name': 'Roma',
                'event_type_type': 'ATP Men Singles',
                'event_time': '12:00',
                'event_first_player': 'Sebastian Baez',
                'first_player_key': '456',
                'event_second_player': 'Rafael Nadal',
                'second_player_key': '888',
                'event_status': '2nd Set',
                'scores': [
                    {'score_first': '6', 'score_second': '4', 'score_set': '1'},
                    {'score_first': '2', 'score_second': '1', 'score_set': '2'}
                ],
                'event_qualification': 'False'
            },
            # FINALIZADO - VICTORIA
            {
                'tournament_name': 'Coquimbo',
                'event_type_type': 'Challenger',
                'event_first_player': 'Juan Manuel Cerundolo',
                'first_player_key': '789',
                'event_second_player': 'Qualy Player',
                'second_player_key': '777',
                'event_status': 'Finished',
                'event_final_result': '2 - 1',
                'scores': [
                    {'score_first': '6', 'score_second': '4'},
                    {'score_first': '2', 'score_second': '6'},
                    {'score_first': '7', 'score_second': '5'}
                ],
                'event_qualification': 'True'
            },
            # FINALIZADO - DERROTA AJUSTADA
            {
                'tournament_name': 'Coquimbo',
                'event_type_type': 'Challenger',
                'event_first_player': 'Other Player',
                'first_player_key': 'OP',
                'event_second_player': 'Facundo Bagnis',
                'second_player_key': 'BAGNIS',
                'event_status': 'Finished',
                'event_final_result': '2 - 1',
                'scores': [
                    {'score_first': '7', 'score_second': '6'},
                    {'score_first': '4', 'score_second': '6'},
                    {'score_first': '6', 'score_second': '4'}
                ]
            },
            # FINALIZADO - DERROTA FACIL
            {
                'tournament_name': 'Coquimbo',
                'event_type_type': 'Challenger',
                'event_first_player': 'Federico Coria',
                'first_player_key': 'CORIA',
                'event_second_player': 'Top Player',
                'second_player_key': 'TOP',
                'event_status': 'Finished',
                'event_final_result': '0 - 2',
                'scores': [
                    {'score_first': '1', 'score_second': '6'},
                    {'score_first': '2', 'score_second': '6'}
                ]
            },
            # FINALIZADO - VICTORIA FACIL (PALIZA)
            {
                'tournament_name': 'Coquimbo',
                'event_type_type': 'Challenger',
                'event_first_player': 'Francisco Cerundolo',
                'first_player_key': '123',
                'event_second_player': 'Weak Player',
                'second_player_key': 'WP',
                'event_status': 'Finished',
                'event_final_result': '2 - 0',
                'scores': [
                    {'score_first': '6', 'score_second': '1'},
                    {'score_first': '6', 'score_second': '0'}
                ]
            }
        ]

def test_flow():
    print("🧪 PROBANDO SENTIMIENTOS DE RESULTADOS 🧪")
    api = MockAPI()
    partidos = api.obtener_partidos_hoy("2026-05-07")
    partidos_arg = filtrar_argentinos(partidos, api)
    
    print(f"\n[BLOQUE 1: AGENDA]")
    partidos_agenda = [p for p in partidos_arg if es_agenda(p)]
    agrupados_agenda = agrupar_por_torneo(partidos_agenda)
    for torneo, lista in agrupados_agenda.items():
        print(generar_tweet_agenda(torneo, lista))

    print(f"\n[BLOQUE 2: ACTUALIZACIÓN]")
    partidos_vivo = [p for p in partidos_arg if es_actualizacion_en_vivo(p)]
    agrupados_vivo = agrupar_por_torneo(partidos_vivo)
    for torneo, lista in agrupados_vivo.items():
        print(generar_tweet_actualizacion(torneo, lista))

    print(f"\n[BLOQUE 3: FINALIZADOS]")
    partidos_fin = [p for p in partidos_arg if es_finalizado(p)]
    agrupados_fin = agrupar_por_torneo(partidos_fin)
    for torneo, lista in agrupados_fin.items():
        print(generar_tweet_finalizado(torneo, lista))

if __name__ == "__main__":
    test_flow()
