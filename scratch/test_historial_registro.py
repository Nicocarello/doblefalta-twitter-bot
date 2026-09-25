import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.')

import os
import json
import shutil
from datetime import datetime, timezone, timedelta

# Importar funciones a testear
from bot.historial import (
    _cargar_cache,
    _guardar_cache,
    cargar_reportados,
    ya_fue_reportado,
    guardar_reportado,
    guardar_reportados_batch,
    limpiar_historial,
    obtener_registro_del_dia,
    obtener_fecha_hoy_arg,
    CACHE_FILE
)

def run_tests():
    print("=" * 60)
    print("🧪 INICIANDO TEST DEL REGISTRO DIARIO Y DEDUPLICACIÓN 🧪")
    print("=" * 60)

    # 1. Verificar migración del cache actual
    print("\n1. Verificando carga y migración de reportados_cache.json actual...")
    cache = _cargar_cache()
    assert isinstance(cache, dict), "El caché debe ser un diccionario"
    assert "dias" in cache, "El caché debe contener la clave 'dias'"
    assert "legacy_keys" in cache, "El caché debe contener la clave 'legacy_keys'"
    print("✅ Estructura del caché migrada correctamente.")

    # 2. Verificar que los IDs del archivo actual (incluyendo Cerúndolo: 12165862) están reconocidos
    print("\n2. Verificando detección de claves existentes (int y str)...")
    cerundolo_key = 12165862
    assert ya_fue_reportado(cerundolo_key), f"El ID {cerundolo_key} (int) debió ser detectado como ya reportado"
    assert ya_fue_reportado(str(cerundolo_key)), f"El ID {cerundolo_key} (str) debió ser detectado como ya reportado"
    
    reportados = cargar_reportados()
    assert cerundolo_key in reportados, "El ID numérico debe estar en el set de reportados"
    assert str(cerundolo_key) in reportados, "El ID string debe estar en el set de reportados"
    print(f"✅ Cerúndolo ({cerundolo_key}) correctamente reconocido como YA REPORTADO.")

    # 3. Guardar partido con datos enriquecidos
    print("\n3. Probando guardado de partido enriquecido con tweet...")
    fecha_hoy = obtener_fecha_hoy_arg()
    partido_mock = {
        'event_key': 99990001,
        'event_first_player': 'Francisco Cerúndolo',
        'event_second_player': 'Casper Ruud',
        'tournament_name': 'ATP Laver Cup',
        'event_final_result': '6-7(4), 6-4, 10-8',
        'event_status': 'Finished',
        'tournament_round': 'Round Robin'
    }
    tweet_mock = "BATALLÓ PERO NO ALCANZÓ 🇦🇷\n\nFran Cerúndolo cayó ante C. Ruud..."
    
    guardar_reportados_batch([partido_mock], fecha=fecha_hoy, tweets=[tweet_mock])
    
    assert ya_fue_reportado(99990001), "El nuevo partido debe estar reportado"
    assert ya_fue_reportado("99990001"), "El nuevo partido debe estar reportado como string"
    
    registro_hoy = obtener_registro_del_dia(fecha_hoy)
    assert "99990001" in registro_hoy, "El partido debe figurar en el registro de hoy"
    entry = registro_hoy["99990001"]
    assert entry["jugadores"] == "Francisco Cerúndolo vs Casper Ruud"
    assert entry["torneo"] == "ATP Laver Cup"
    assert entry["resultado"] == "6-7(4), 6-4, 10-8"
    assert tweet_mock in entry["tweets"]
    print("✅ Registro de partido y tweet guardado con éxito en el día actual.")

    # 4. Probar que limpiar_historial NO borra el archivo ni el día de hoy
    print("\n4. Verificando que limpiar_historial() NO borra los partidos de hoy...")
    limpiar_historial(dias_retencion=7)
    assert os.path.exists(CACHE_FILE), "El archivo reportados_cache.json NUNCA debe ser eliminado"
    assert ya_fue_reportado(99990001), "El partido de hoy debe seguir existiendo tras limpiar_historial"
    assert ya_fue_reportado(cerundolo_key), "Cerúndolo debe seguir existiendo tras limpiar_historial"
    print("✅ limpiar_historial preservó todos los partidos de hoy y recientes.")

    # 5. Probar purga de fecha antigua (> 7 días)
    print("\n5. Probando purga selectiva de fechas de más de 7 días...")
    fecha_vieja = "2026-09-01"
    cache["dias"][fecha_vieja] = {
        "88880001": {
            "event_key": "88880001",
            "jugadores": "Test vs Test",
            "torneo": "Old Tournament"
        }
    }
    _guardar_cache()
    assert fecha_vieja in _cargar_cache()["dias"], "La fecha vieja debe haberse guardado"
    
    limpiar_historial(dias_retencion=7)
    assert fecha_vieja not in _cargar_cache()["dias"], "La fecha vieja debe haber sido purgada"
    assert fecha_hoy in _cargar_cache()["dias"], "La fecha de hoy debe conservarse"
    print("✅ Purga selectiva funcionó correctamente sin tocar hoy ni días recientes.")

    # 6. Simular filtro en main: verificar que un partido repetido es ignorado
    print("\n6. Simulando lógica de filtrado de main.py...")
    partidos_api_simulados = [
        partido_mock, # ya reportado
        {
            'event_key': 99990002,
            'event_first_player': 'Sebastián Báez',
            'event_second_player': 'Taylor Fritz',
            'tournament_name': 'ATP Tokyo',
            'event_status': 'Finished'
        } # nuevo
    ]
    
    rep_set = cargar_reportados()
    nuevos = [p for p in partidos_api_simulados if not ya_fue_reportado(p.get('event_key'), rep_set)]
    assert len(nuevos) == 1, f"Debió encontrar exactamente 1 partido nuevo, encontró: {len(nuevos)}"
    assert nuevos[0]['event_key'] == 99990002, "El partido nuevo debe ser Báez"
    print("✅ Filtro de duplicados excluyó correctamente el partido ya reportado y dejó solo el nuevo.")

    print("\n" + "=" * 60)
    print("🎉 ¡TODOS LOS TESTS PASARON EXITOSAMENTE! 🎉")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
