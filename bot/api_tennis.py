import requests
import json
import os
from bot.config import TENNIS_API_KEY, TENNIS_BASE_URL

CACHE_FILE = "jugadores_cache.json"

class TennisAPI:
    def __init__(self):
        self.cache_jugadores = self._cargar_cache()

    def _cargar_cache(self):
        """Carga el caché desde un archivo JSON local."""
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _guardar_cache(self):
        """Guarda el caché en un archivo JSON local."""
        try:
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.cache_jugadores, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"⚠️ Error guardando caché: {e}")

    def obtener_info_jugador(self, player_key):
        """Consulta info de un jugador con caché persistente."""
        if not player_key:
            return {'es_arg': False, 'ranking': 9999}
        
        player_key_str = str(player_key)
        if player_key_str in self.cache_jugadores:
            cached_info = self.cache_jugadores[player_key_str]
            # Si el caché es viejo o no tiene país, forzamos actualización
            if 'pais' in cached_info and cached_info['pais']:
                return cached_info
        
        params = {
            'method': 'get_players',
            'APIkey': TENNIS_API_KEY,
            'player_key': player_key
        }
        
        info = {'es_arg': False, 'ranking': 9999, 'pais': ''}
        try:
            response = requests.get(TENNIS_BASE_URL, params=params, timeout=10)
            datos = response.json()
            if datos.get('success') == 1 and datos.get('result'):
                jugador = datos['result'][0]
                pais = jugador.get('player_country')
                ranking = jugador.get('player_ranking', 9999)
                
                info['pais'] = pais if pais else ''
                if pais and pais.lower() == 'argentina':
                    info['es_arg'] = True
                
                # Intentar extraer ranking del root o de stats
                ranking_val = jugador.get('player_ranking')
                if not ranking_val:
                    stats = jugador.get('stats', [])
                    # Buscamos el ranking de singles más reciente
                    singles_stats = [s for s in stats if s.get('type') == 'singles']
                    if singles_stats:
                        # Ordenamos por temporada (ej: "2024") descendentemente
                        singles_stats.sort(key=lambda x: x.get('season', '0'), reverse=True)
                        ranking_val = singles_stats[0].get('rank')
                
                try:
                    info['ranking'] = int(ranking_val) if ranking_val else 9999
                except:
                    info['ranking'] = 9999
            
            # Guardar en memoria y persistir
            self.cache_jugadores[player_key_str] = info
            self._guardar_cache()
            return info
        except Exception as e:
            print(f"⚠️ Error consultando jugador {player_key}: {e}")
            return info

    def obtener_partidos_hoy(self, fecha_iso):
        """Consulta todos los fixtures para una fecha específica."""
        params = {
            'method': 'get_fixtures',
            'APIkey': TENNIS_API_KEY,
            'date_start': fecha_iso,
            'date_stop': fecha_iso
        }
        
        try:
            response = requests.get(TENNIS_BASE_URL, params=params, timeout=20)
            datos = response.json()
            if datos.get('success') == 1:
                return datos.get('result', [])
            return []
        except Exception as e:
            print(f"❌ Error consultando la API de Tenis: {e}")
            return []
