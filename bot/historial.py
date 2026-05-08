import json
import os

CACHE_FILE = "reportados_cache.json"

def cargar_reportados():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def guardar_reportado(event_key):
    reportados = cargar_reportados()
    if event_key not in reportados:
        reportados.append(event_key)
        with open(CACHE_FILE, 'w') as f:
            json.dump(reportados, f)

def limpiar_historial():
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
