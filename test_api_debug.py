import requests
import os
from dotenv import load_dotenv

load_dotenv()
TENNIS_API_KEY = os.getenv("TENNIS_API_KEY")
TENNIS_BASE_URL = "https://api.api-tennis.com/tennis/"

def test_player(player_key):
    params = {
        'method': 'get_players',
        'APIkey': TENNIS_API_KEY,
        'player_key': player_key
    }
    response = requests.get(TENNIS_BASE_URL, params=params)
    print(f"Status: {response.status_code}")
    print(f"Body: {response.text}")

# Probemos con Sebastian Baez si sabemos su ID, o busquemos por nombre
# En el reporte del usuario aparece Baez vs Bublik.
# Vamos a ver qué IDs tienen en el cache si puedo.

test_player("949") # Un ID al azar del cache que es argentino (linea 79 del view anterior)
