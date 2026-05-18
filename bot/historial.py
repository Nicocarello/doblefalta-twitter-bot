import json
import os

CACHE_FILE = "reportados_cache.json"

# Cache en memoria: se carga una sola vez por proceso
_cache = None

def _cargar_cache():
    """Carga el historial desde disco (solo la primera vez) y lo mantiene en memoria."""
    global _cache
    if _cache is None:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f:
                try:
                    _cache = json.load(f)
                except Exception:
                    _cache = []
        else:
            _cache = []
    return _cache

def _guardar_cache():
    """Persiste el caché en memoria al disco."""
    global _cache
    with open(CACHE_FILE, 'w') as f:
        json.dump(_cache, f)

def cargar_reportados():
    """Devuelve una copia de la lista de event_keys ya reportados."""
    return list(_cargar_cache())

def guardar_reportado(event_key):
    """Guarda un único event_key. Para lotes, usar guardar_reportados_batch()."""
    if not event_key:
        return
    cache = _cargar_cache()
    if event_key not in cache:
        cache.append(event_key)
        _guardar_cache()

def guardar_reportados_batch(event_keys):
    """
    Guarda múltiples event_keys de una sola vez, haciendo un único write a disco.
    Mucho más eficiente que llamar guardar_reportado() en un bucle.
    """
    cache = _cargar_cache()
    changed = False
    for key in event_keys:
        if key and key not in cache:
            cache.append(key)
            changed = True
    if changed:
        _guardar_cache()

def limpiar_historial():
    """Borra el historial en memoria y en disco (para el inicio de un nuevo día)."""
    global _cache
    _cache = []
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
