from bot.redactor import generar_tweet_agenda, obtener_bandera
import json

partido = {
    'event_time': '10:00',
    'event_first_player': 'Sebastian Baez',
    'event_second_player': 'Alexander Bublik',
    'tournament_name': 'ATP Rome',
    'arg_info': {
        'jugador_1': {'es_arg': True, 'ranking': 19, 'pais': 'Argentina'},
        'jugador_2': {'es_arg': False, 'ranking': 18, 'pais': 'Kazakhstan'}
    }
}

print("Prueba de bandera:")
print(f"Argentina: {obtener_bandera('Argentina')}")
print(f"Kazakhstan: {obtener_bandera('Kazakhstan')}")

tweet = generar_tweet_agenda("Rome", [partido])
print("\nTweet generado:")
print(tweet)
