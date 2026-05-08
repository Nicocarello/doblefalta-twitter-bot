import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
TENNIS_API_KEY = os.getenv("TENNIS_API_KEY")
TENNIS_BASE_URL = "https://api.api-tennis.com/tennis/"

def search_player(name):
    params = {
        'method': 'get_players',
        'APIkey': TENNIS_API_KEY,
        'search': name
    }
    response = requests.get(TENNIS_BASE_URL, params=params)
    data = response.json()
    if data.get('success') == 1:
        for p in data.get('result', []):
            print(f"ID: {p['player_key']}, Name: {p['player_name']}, Country: {p['player_country']}")

print("Searching for Baez...")
search_player("Baez")
