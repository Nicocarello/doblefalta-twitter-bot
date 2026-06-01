import sys
import os

# Añadir el directorio raíz al path para importar bot
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from bot.filtros import filtrar_argentinos, agrupar_por_torneo
from bot.redactor import generar_tweet_agenda, generar_tweet_actualizacion, generar_tweet_finalizado

class MockAPI:
    def obtener_info_jugador(self, key):
        if key == 'arg_junior':
            return {'es_arg': True, 'ranking': 1498, 'pais': 'Argentina'}
        if key == 'fr_junior':
            return {'es_arg': False, 'ranking': 615, 'pais': 'France'}
        if key == 'arg_pro':
            return {'es_arg': True, 'ranking': 30, 'pais': 'Argentina'}
        if key == 'pro_rival':
            return {'es_arg': False, 'ranking': 1, 'pais': 'Serbia'}
        return {'es_arg': False, 'ranking': 9999, 'pais': 'Unknown'}

def main():
    api = MockAPI()
    
    # 1. Un partido Junior y otro Pro
    partidos = [
        {
            'event_key': 1,
            'event_first_player': 'E. Inisan',
            'first_player_key': 'fr_junior',
            'event_second_player': 'S. A. Larraya Guidi',
            'second_player_key': 'arg_junior',
            'event_final_result': '0 - 2',
            'event_status': 'Finished',
            'event_type_type': 'Girls Singles',
            'tournament_name': 'French Open',
            'tournament_round': 'Girls French Open - 1/16-finals',
            'scores': [
                {'score_first': '4', 'score_second': '6'},
                {'score_first': '0', 'score_second': '6'}
            ],
            'event_qualification': 'False'
        },
        {
            'event_key': 2,
            'event_first_player': 'Novak Djokovic',
            'first_player_key': 'pro_rival',
            'event_second_player': 'Francisco Cerundolo',
            'second_player_key': 'arg_pro',
            'event_final_result': '3 - 2',
            'event_status': 'Finished',
            'event_type_type': 'Singles',
            'tournament_name': 'French Open',
            'tournament_round': 'French Open - 4tos',
            'scores': [
                {'score_first': '6', 'score_second': '4'},
                {'score_first': '3', 'score_second': '6'},
                {'score_first': '6', 'score_second': '7'},
                {'score_first': '6', 'score_second': '3'},
                {'score_first': '6', 'score_second': '4'}
            ],
            'event_qualification': 'False'
        }
    ]
    
    print("--- 1. Filtrando partidos ---")
    partidos_arg = filtrar_argentinos(partidos, api)
    print(f"Partidos filtrados ({len(partidos_arg)}):")
    for p in partidos_arg:
        print(f"  - {p['event_first_player']} vs {p['event_second_player']} | Torneo: {p['tournament_name']} (Junior: {p.get('es_junior')})")
        
    print("\n--- 2. Agrupando por torneo ---")
    agrupados = agrupar_por_torneo(partidos_arg)
    for torneo, lista in agrupados.items():
        print(f"Torneo: {torneo}")
        for p in lista:
            print(f"  - {p['event_first_player']} vs {p['event_second_player']}")
            
    print("\n--- 3. Generando tweets finalizados ---")
    for torneo, lista in agrupados.items():
        tweets = generar_tweet_finalizado(torneo, lista)
        print(f"\nTorneo: {torneo}")
        for t in tweets:
            print(t)

if __name__ == "__main__":
    main()
