import json
import os
from datetime import datetime, timezone, timedelta

CACHE_FILE = "reportados_cache.json"

# Zona horaria oficial para el bot (Argentina UTC-3, sin horario de verano)
TZ_ARG = timezone(timedelta(hours=-3))

def obtener_fecha_hoy_arg():
    """Devuelve la fecha actual en Argentina en formato YYYY-MM-DD."""
    return datetime.now(TZ_ARG).strftime("%Y-%m-%d")

def obtener_timestamp_arg():
    """Devuelve el timestamp actual en Argentina en formato YYYY-MM-DD HH:MM:SS."""
    return datetime.now(TZ_ARG).strftime("%Y-%m-%d %H:%M:%S")

# Cache en memoria: se carga una sola vez por proceso
_cache = None

def _estructura_vacia():
    return {
        "_version": 2,
        "ultima_actualizacion": obtener_timestamp_arg(),
        "dias": {},
        "legacy_keys": []
    }

def _migrar_formato_legacy(datos_legacy):
    """
    Convierte la lista antigua [12345, 67890] a la nueva estructura estructurada por día.
    """
    fecha_hoy = obtener_fecha_hoy_arg()
    nueva_estructura = _estructura_vacia()
    legacy_keys = []
    partidos_hoy = {}
    
    for k in datos_legacy:
        k_str = str(k)
        legacy_keys.append(k_str)
        partidos_hoy[k_str] = {
            "event_key": k_str,
            "timestamp": obtener_timestamp_arg(),
            "torneo": "Desconocido (Migrado)",
            "jugadores": "Desconocido",
            "resultado": "",
            "tweets": []
        }
    
    nueva_estructura["dias"][fecha_hoy] = partidos_hoy
    nueva_estructura["legacy_keys"] = legacy_keys
    return nueva_estructura

def _cargar_cache():
    """
    Carga el historial desde disco y lo mantiene en memoria.
    Soporta formato legacy (lista) y formato moderno (dict con registro diario).
    """
    global _cache
    if _cache is not None:
        return _cache

    if not os.path.exists(CACHE_FILE):
        _cache = _estructura_vacia()
        return _cache

    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            contenido = json.load(f)
            
            if isinstance(contenido, list):
                # Migración de formato antiguo a nuevo
                _cache = _migrar_formato_legacy(contenido)
                _guardar_cache()
            elif isinstance(contenido, dict):
                _cache = contenido
                if "dias" not in _cache:
                    _cache["dias"] = {}
                if "legacy_keys" not in _cache:
                    _cache["legacy_keys"] = []
            else:
                _cache = _estructura_vacia()
    except Exception as e:
        print(f"⚠️ Error leyendo {CACHE_FILE}: {e}. Se inicializa estructura nueva.")
        _cache = _estructura_vacia()

    return _cache

def _guardar_cache():
    """Persiste el caché en memoria al disco con formato legible e indentado."""
    global _cache
    if _cache is None:
        return
    _cache["ultima_actualizacion"] = obtener_timestamp_arg()
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(_cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ Error guardando caché en {CACHE_FILE}: {e}")

def cargar_reportados(dias_atras=7):
    """
    Devuelve un conjunto (set) con todos los event_keys reportados en los últimos
    `dias_atras` días y claves legacy.
    
    Para evitar problemas de tipos, incluye cada clave como string y como entero
    (si es convertible a entero). Así `p.get('event_key') in reportados` funciona
    siempre, sea int o str.
    """
    cache = _cargar_cache()
    keys_set = set()

    # Agregar claves legacy
    for k in cache.get("legacy_keys", []):
        k_str = str(k)
        keys_set.add(k_str)
        if k_str.isdigit():
            keys_set.add(int(k_str))

    # Filtrar fechas recientes
    hoy = datetime.now(TZ_ARG).date()
    fecha_limite = hoy - timedelta(days=dias_atras)

    dias_dict = cache.get("dias", {})
    for fecha_str, partidos in dias_dict.items():
        try:
            fecha_d = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            if fecha_d >= fecha_limite:
                for k in partidos.keys():
                    k_str = str(k)
                    keys_set.add(k_str)
                    if k_str.isdigit():
                        keys_set.add(int(k_str))
        except ValueError:
            # Si el string no es fecha válida, incluir por seguridad
            for k in partidos.keys():
                k_str = str(k)
                keys_set.add(k_str)
                if k_str.isdigit():
                    keys_set.add(int(k_str))

    return keys_set

def ya_fue_reportado(event_key, reportados_set=None):
    """
    Determina si un event_key ya fue reportado previamente.
    Si se pasa un `reportados_set`, se consulta ese conjunto; de lo contrario,
    se consulta directamente el caché.
    """
    if event_key is None or event_key == "":
        return False

    if reportados_set is not None:
        return (event_key in reportados_set) or (str(event_key) in reportados_set)

    rep = cargar_reportados()
    return (event_key in rep) or (str(event_key) in rep)

def _extraer_datos_partido(item, tweets=None):
    """
    Normaliza un item (que puede ser dict de partido o un event_key plano)
    a la estructura completa de registro.
    """
    if isinstance(item, dict):
        key = str(item.get('event_key', ''))
        j1 = item.get('event_first_player', '')
        j2 = item.get('event_second_player', '')
        jugadores = f"{j1} vs {j2}".strip() if (j1 or j2) else "Desconocido"
        torneo = item.get('tournament_name', 'Sin Torneo')
        resultado = item.get('event_final_result', '')
        estado = item.get('event_status', '')
        ronda = item.get('tournament_round', '')
    else:
        key = str(item)
        jugadores = "Desconocido"
        torneo = "Sin Torneo"
        resultado = ""
        estado = ""
        ronda = ""

    lista_tweets = []
    if tweets:
        if isinstance(tweets, list):
            lista_tweets = tweets
        elif isinstance(tweets, str):
            lista_tweets = [tweets]

    return key, {
        "event_key": key,
        "timestamp": obtener_timestamp_arg(),
        "torneo": torneo,
        "ronda": ronda,
        "jugadores": jugadores,
        "resultado": resultado,
        "estado": estado,
        "tweets": lista_tweets
    }

def guardar_reportado(item, tweet=None, fecha=None):
    """
    Guarda un único partido o event_key en el registro del día.
    `item` puede ser un diccionario de partido o un ID (int/str).
    """
    if not item:
        return
    guardar_reportados_batch([item], fecha=fecha, tweets=[tweet] if tweet else None)

def guardar_reportados_batch(items, fecha=None, tweets=None):
    """
    Guarda múltiples partidos o event_keys en el registro del día de una sola vez.
    `items` puede ser una lista de dicts de partidos o una lista de IDs.
    `tweets` puede ser una lista de tweets generados para estos partidos.
    """
    if not items:
        return

    if not fecha:
        fecha = obtener_fecha_hoy_arg()

    cache = _cargar_cache()
    if "dias" not in cache:
        cache["dias"] = {}
    if fecha not in cache["dias"]:
        cache["dias"][fecha] = {}

    changed = False
    for item in items:
        key, datos = _extraer_datos_partido(item, tweets)
        if not key:
            continue
        
        # Si ya existía, enriquecemos o actualizamos tweets sin pisar lo anterior
        if key in cache["dias"][fecha]:
            existente = cache["dias"][fecha][key]
            if datos["tweets"]:
                existente_tweets = existente.get("tweets", [])
                for t in datos["tweets"]:
                    if t not in existente_tweets:
                        existente_tweets.append(t)
                existente["tweets"] = existente_tweets
            if datos["resultado"] and not existente.get("resultado"):
                existente["resultado"] = datos["resultado"]
            if datos["jugadores"] != "Desconocido" and existente.get("jugadores") == "Desconocido":
                existente["jugadores"] = datos["jugadores"]
            if datos["torneo"] != "Sin Torneo" and existente.get("torneo") == "Sin Torneo":
                existente["torneo"] = datos["torneo"]
            changed = True
        else:
            cache["dias"][fecha][key] = datos
            changed = True

    if changed:
        _guardar_cache()

def obtener_registro_del_dia(fecha=None):
    """
    Devuelve un diccionario con todos los partidos tuiteados en la fecha solicitada
    (por defecto la fecha actual en Argentina).
    Formato: { event_key: { detalles... } }
    """
    if not fecha:
        fecha = obtener_fecha_hoy_arg()
    cache = _cargar_cache()
    return dict(cache.get("dias", {}).get(fecha, {}))

def limpiar_historial(dias_retencion=7):
    """
    Mantenimiento periódico del historial: purga fechas antiguas que tengan
    más de `dias_retencion` días.
    
    IMPORTANTE:
    NUNCA borra el archivo ni elimina los partidos del día actual o recientes.
    Esto previene que una ejecución de agenda (incluso con retraso) vuelva
    a tuitear partidos ya finalizados de la jornada.
    """
    cache = _cargar_cache()
    hoy = datetime.now(TZ_ARG).date()
    fecha_limite = hoy - timedelta(days=dias_retencion)

    dias_dict = cache.get("dias", {})
    fechas_a_eliminar = []

    for fecha_str in list(dias_dict.keys()):
        try:
            fecha_d = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            if fecha_d < fecha_limite:
                fechas_a_eliminar.append(fecha_str)
        except ValueError:
            pass

    if fechas_a_eliminar:
        print(f"🧹 Purgando historial antiguo ({len(fechas_a_eliminar)} días anteriores a {fecha_limite})...")
        for f in fechas_a_eliminar:
            del dias_dict[f]
        _guardar_cache()
    else:
        print(f"🧹 Historial al día: no hay registros con más de {dias_retencion} días para purgar.")

def debe_publicar_promo(frecuencia_dias=3, fecha_hoy=None):
    """
    Verifica si corresponde publicar un tweet promocional de la app.
    Devuelve True si pasaron al menos `frecuencia_dias` días desde la última promo
    o si nunca se publicó una.
    """
    if not fecha_hoy:
        fecha_hoy = obtener_fecha_hoy_arg()
    
    cache = _cargar_cache()
    ultima_promo = cache.get("ultima_promo_app")
    
    if not ultima_promo:
        return True
    
    try:
        f_hoy = datetime.strptime(fecha_hoy, "%Y-%m-%d").date()
        f_ult = datetime.strptime(ultima_promo, "%Y-%m-%d").date()
        dias_pasados = (f_hoy - f_ult).days
        return dias_pasados >= frecuencia_dias
    except Exception:
        return True

def registrar_promo_publicada(tweet_texto, fecha_hoy=None):
    """
    Registra que se publicó un tweet promocional para el control de frecuencia.
    """
    if not fecha_hoy:
        fecha_hoy = obtener_fecha_hoy_arg()

    cache = _cargar_cache()
    cache["ultima_promo_app"] = fecha_hoy
    
    if "historial_promos" not in cache:
        cache["historial_promos"] = []
        
    cache["historial_promos"].append({
        "fecha": fecha_hoy,
        "timestamp": obtener_timestamp_arg(),
        "tweet": tweet_texto
    })
    # Mantener como máximo los últimos 15 registros de promos
    cache["historial_promos"] = cache["historial_promos"][-15:]
    _guardar_cache()

