from datetime import datetime, timedelta
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

    def precargar_rankings(self):
        """
        Descarga los rankings actuales (ATP, WTA, ITF) y actualiza el caché masivamente.
        Esto evita cientos de llamadas individuales y asegura rankings globales correctos.
        """
        print("📊 Precargando rankings globales para optimizar el caché...")
        for cat in ["atp", "wta", "itf"]:
            standings = self.obtener_rankings(cat)
            if not standings:
                continue
            
            count = 0
            for item in standings:
                p_key = str(item.get('player_key'))
                if not p_key: continue
                
                ranking = 9999
                try:
                    ranking = int(item.get('player_place', item.get('place', 9999)))
                except: pass
                
                pais = item.get('country', item.get('player_country', ''))
                
                # Actualizar o crear entrada en el caché
                info = self.cache_jugadores.get(p_key, {'es_arg': False})
                info['ranking'] = ranking
                if pais:
                    info['pais'] = pais
                    info['es_arg'] = (pais.lower() == 'argentina')
                
                info['last_update'] = datetime.now().strftime("%Y-%m-%d")
                self.cache_jugadores[p_key] = info
                count += 1
            print(f"✅ Se actualizaron {count} jugadores desde el ranking {cat.upper()}.")
        
        self._guardar_cache()

    def obtener_info_jugador(self, player_key):
        """Consulta info de un jugador con caché persistente y refresco periódico."""
        if not player_key:
            return {'es_arg': False, 'ranking': 9999}
        
        player_key_str = str(player_key)
        hoy = datetime.now()
        
        if player_key_str in self.cache_jugadores:
            cached_info = self.cache_jugadores[player_key_str]
            last_upd_str = cached_info.get('last_update')
            
            # Si tenemos info completa y es reciente (< 7 días), la usamos
            if last_upd_str and 'pais' in cached_info and cached_info['pais']:
                try:
                    last_upd = datetime.strptime(last_upd_str, "%Y-%m-%d")
                    # Si el ranking es 9999, reintentamos cada 3 días, si no, cada 7
                    dias_expiracion = 3 if cached_info.get('ranking') == 9999 else 7
                    if (hoy - last_upd).days < dias_expiracion:
                        return cached_info
                except:
                    pass # Si hay error en fecha, procedemos a actualizar
        
        # Si no está en caché o expiró, consultamos la API
        params = {
            'method': 'get_players',
            'APIkey': TENNIS_API_KEY,
            'player_key': player_key
        }
        
        info = {'es_arg': False, 'ranking': 9999, 'pais': '', 'last_update': hoy.strftime("%Y-%m-%d")}
        try:
            response = requests.get(TENNIS_BASE_URL, params=params, timeout=10)
            datos = response.json()
            if datos.get('success') == 1 and datos.get('result'):
                jugador = datos['result'][0]
                pais = jugador.get('player_country')
                
                info['pais'] = pais if pais else ''
                if pais and pais.lower() == 'argentina':
                    info['es_arg'] = True
                
                # Intentar extraer ranking del root o de stats
                ranking_val = jugador.get('player_ranking')
                if not ranking_val:
                    stats = jugador.get('stats', [])
                    singles_stats = [s for s in stats if s.get('type') == 'singles']
                    if singles_stats:
                        singles_stats.sort(key=lambda x: x.get('season', '0'), reverse=True)
                        ranking_val = singles_stats[0].get('rank')
                
                try:
                    info['ranking'] = int(ranking_val) if ranking_val else 9999
                except:
                    info['ranking'] = 9999
            
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

    def obtener_rankings(self, tipo="atp"):
        """Consulta el ranking (standings) para ATP o WTA."""
        params = {
            'method': 'get_standings',
            'APIkey': TENNIS_API_KEY,
            'event_type': tipo.upper()
        }
        try:
            response = requests.get(TENNIS_BASE_URL, params=params, timeout=20)
            datos = response.json()
            if datos.get('success') == 1:
                return datos.get('result', [])
            return []
        except Exception as e:
            print(f"❌ Error consultando rankings {tipo}: {e}")
            return []
