import sys
import argparse
from datetime import datetime
from bot.api_tennis import TennisAPI
from bot.filtros import filtrar_argentinos, agrupar_por_torneo, es_agenda, es_actualizacion_en_vivo, es_finalizado
from bot.redactor import (
    generar_tweet_agenda,
    generar_tweet_actualizacion,
    generar_tweet_finalizado,
    generar_tweet_ranking,
    generar_hilo_ranking_argentinos,
    generar_tweet_promocional
)
from bot.twitter import publicar_tweet
from bot.config import DRY_RUN, APP_URL
from bot.mailer import enviar_reporte_email
from bot.historial import (
    cargar_reportados,
    ya_fue_reportado,
    guardar_reportados_batch,
    limpiar_historial,
    obtener_fecha_hoy_arg,
    obtener_registro_del_dia,
    debe_publicar_promo,
    registrar_promo_publicada
)

def limpiar_tweet(texto_raw):
    """Elimina los marcadores de formato (--- INICIO TWEET ---, --- FIN TWEET ---)
    del texto generado por el redactor antes de publicarlo o incluirlo en el email."""
    lineas = texto_raw.split('\n')
    # Quita la primera línea si es un marcador
    if lineas and lineas[0].startswith('---') and lineas[0].endswith('---'):
        lineas = lineas[1:]
    # Quita la última línea si es un marcador
    if lineas and lineas[-1].startswith('---') and lineas[-1].endswith('---'):
        lineas = lineas[:-1]
    return '\n'.join(lineas).strip()

def procesar_tweet_promocional(partidos_arg, app_url, reporte_texto, force=False):
    """
    Evalúa y publica el tweet promocional de la app si pasaron al menos 3 días
    desde la última publicación (o si se fuerza explícitamente).
    """
    if not app_url:
        print("💡 APP_URL no configurada en las variables de entorno (.env). Omitiendo promo.")
        return False

    if not force and not debe_publicar_promo(frecuencia_dias=3):
        print("⏳ Promo App: intervalo de 3 días aún no alcanzado.")
        return False

    print("\n📢 PROCESANDO BLOQUE: PROMOCIÓN DE LA APP...")
    tweet_raw = generar_tweet_promocional(app_url, partidos_arg)
    if tweet_raw:
        tweet_limpio = limpiar_tweet(tweet_raw)
        reporte_texto.append(f"[PROMO APP]\n{tweet_limpio}\n\n")
        print("Texto generado para Promo App:")
        print(tweet_limpio)
        if not DRY_RUN:
            publicar_tweet(tweet_limpio)
        registrar_promo_publicada(tweet_limpio)
        print("✅ Tweet promocional publicado y registrado (próximo en 3 días).")
        return True
    return False

# Configuración de salida para consola en Windows (emojis)
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    parser = argparse.ArgumentParser(description="Bot Doble Falta Tenis")
    parser.add_argument("--mode", type=str, default="all", choices=["agenda", "live", "final", "ranking", "promo", "all"],
                        help="Modo de ejecución: agenda, live, final, ranking, promo o all (por defecto)")
    parser.add_argument("--incremental", action="store_true", 
                        help="Si es True, solo reporta lo nuevo desde la última ejecución (comportamiento por defecto)")
    parser.add_argument("--force", action="store_true",
                        help="Fuerza el reenvío de partidos o promo aunque ya hayan sido reportados")
    args = parser.parse_args()

    fecha_hoy = obtener_fecha_hoy_arg()
    print(f"🚀 INICIANDO BOT DOBLE FALTA - MODO: {args.mode.upper()} - FECHA: {fecha_hoy} 🚀")

    api = TennisAPI()
    
    # 0. Precargar rankings de forma condicional para ahorrar cuota de API
    if args.mode in ["agenda", "ranking"] or not api.cache_jugadores:
        api.precargar_rankings()
    else:
        print("💡 Saltando precarga de rankings de la API (se usará el caché local persistente).")
    
    # 1. Obtener todos los partidos de hoy
    print("🔍 Obteniendo fixtures de la API...")
    partidos = api.obtener_partidos_hoy(fecha_hoy)
    
    if not partidos:
        print("📭 No hay partidos hoy.")
        return

    # 2. Filtrar solo argentinos
    print(f"🇦🇷 Filtrando tenistas argentinos entre {len(partidos)} partidos...")
    partidos_arg = filtrar_argentinos(partidos, api)
    print(f"✅ Se encontraron {len(partidos_arg)} partidos con presencia argentina.")

    if not partidos_arg:
        print("📭 No hay partidos de argentinos hoy.")
        if args.mode != "live": # No mandamos mail si es solo una actualización live vacía
            # enviar_reporte_email(f"Reporte {fecha_hoy}: No se encontraron partidos de tenistas argentinos hoy.")
            pass
        return

    # Lista para recolectar todo el texto generado para el mail
    reporte_texto = [f"REPORTE DOBLE FALTA - {fecha_hoy} ({args.mode.upper()})\n", "="*30 + "\n"]
    hay_contenido = False

    # ---------------------------------------------------------
    # BLOQUE 1: AGENDA
    # ---------------------------------------------------------
    if args.mode in ["agenda", "all"]:
        print("\n📅 PROCESANDO BLOQUE: AGENDA...")
        # Mantenimiento del historial (purga días viejos sin tocar el día de hoy)
        print("🧹 Mantenimiento de historial: purgando registros con más de 7 días...")
        limpiar_historial(dias_retencion=7)
        partidos_agenda = [p for p in partidos_arg if es_agenda(p)]
        if partidos_agenda:
            hay_contenido = True
            agrupados = agrupar_por_torneo(partidos_agenda)
            for torneo, lista in agrupados.items():
                tweets = generar_tweet_agenda(torneo, lista)
                reply_id = None
                for t in tweets:
                    t_limpio = limpiar_tweet(t)
                    reporte_texto.append(f"[AGENDA - {torneo}]\n{t_limpio}\n\n")
                    print(f"Texto generado para {torneo} (Agenda)")
                    if not DRY_RUN:
                        reply_id = publicar_tweet(t_limpio, in_reply_to_tweet_id=reply_id)
        else:
            print("No hay partidos en agenda.")

        # Evaluación periódica de tweet promocional (cada 3 días junto a la agenda matutina)
        if procesar_tweet_promocional(partidos_arg, APP_URL, reporte_texto, force=args.force):
            hay_contenido = True

    # ---------------------------------------------------------
    # BLOQUE 2: EN VIVO
    # ---------------------------------------------------------
    if args.mode in ["live", "all"]:
        print("\n🎾 PROCESANDO BLOQUE: ACTUALIZACIÓN EN VIVO...")
        partidos_vivo = [p for p in partidos_arg if es_actualizacion_en_vivo(p)]
        if partidos_vivo:
            hay_contenido = True
            agrupados = agrupar_por_torneo(partidos_vivo)
            for torneo, lista in agrupados.items():
                tweets = generar_tweet_actualizacion(torneo, lista)
                reply_id = None
                for t in tweets:
                    t_limpio = limpiar_tweet(t)
                    reporte_texto.append(f"[EN VIVO - {torneo}]\n{t_limpio}\n\n")
                    print(f"Texto generado para {torneo} (En Vivo)")
                    if not DRY_RUN:
                        reply_id = publicar_tweet(t_limpio, in_reply_to_tweet_id=reply_id)
        else:
            print("No hay partidos en vivo actualmente.")

    # ---------------------------------------------------------
    # BLOQUE 3: RESULTADOS
    # ---------------------------------------------------------
    if args.mode in ["final", "all"]:
        print("\n🏁 PROCESANDO BLOQUE: RESULTADOS FINALES...")
        partidos_fin = [p for p in partidos_arg if es_finalizado(p)]
        
        # Filtro de duplicados: consultar historial para no repetir partidos ya tuiteados
        reportados = cargar_reportados()
        if not args.force:
            partidos_fin = [p for p in partidos_fin if not ya_fue_reportado(p.get('event_key'), reportados)]
            print(f"Filtro de duplicados activo. Partidos nuevos encontrados: {len(partidos_fin)}")
        else:
            print(f"⚠️ Modo FORCE activo: ignorando filtro de duplicados ({len(partidos_fin)} partidos).")

        if partidos_fin:
            hay_contenido = True
            agrupados = agrupar_por_torneo(partidos_fin)
            for torneo, lista in agrupados.items():
                tweets = generar_tweet_finalizado(torneo, lista)
                reply_id = None
                tweets_publicados = []
                for t in tweets:
                    t_limpio = limpiar_tweet(t)
                    reporte_texto.append(f"[FINALIZADO - {torneo}]\n{t_limpio}\n\n")
                    print(f"Texto generado para {torneo} (Finalizado)")
                    if not DRY_RUN:
                        reply_id = publicar_tweet(t_limpio, in_reply_to_tweet_id=reply_id)
                    tweets_publicados.append(t_limpio)
                
                # Registrar partidos en el historial diario con sus tweets generados (SIEMPRE)
                guardar_reportados_batch(lista, fecha=fecha_hoy, tweets=tweets_publicados)
        else:
            print("No hay resultados finales (nuevos) para reportar.")

        reg_hoy = obtener_registro_del_dia(fecha_hoy)
        print(f"📋 Total de partidos registrados hoy ({fecha_hoy}): {len(reg_hoy)}")



    # ---------------------------------------------------------
    # BLOQUE 4: RANKING (Lunes)
    # ---------------------------------------------------------
    if args.mode in ["ranking", "all"]:
        print("\n📊 PROCESANDO BLOQUE: RANKING TOP 10...")
        for cat in ["atp", "wta"]:
            datos_ranking = api.obtener_rankings(cat)
            if datos_ranking:
                hay_contenido = True
                texto_tweet = limpiar_tweet(generar_tweet_ranking(datos_ranking, cat))
                reporte_texto.append(f"[RANKING {cat.upper()}]\n{texto_tweet}\n\n")
                print(f"Texto generado para Ranking {cat.upper()}")
                reply_id = None
                if not DRY_RUN:
                    reply_id = publicar_tweet(texto_tweet)
                # Hilo de Argentinos (Nuevo!)
                if cat == "atp":
                    print(f"Generando hilo de argentinos para {cat.upper()}...")
                    hilo_arg = generar_hilo_ranking_argentinos(datos_ranking, cat)
                    for i, tweet_hilo in enumerate(hilo_arg):
                        tweet_hilo_limpio = limpiar_tweet(tweet_hilo)
                        reporte_texto.append(f"[HILO RANKING ARGENTINOS {cat.upper()} - Parte {i+1}]\n{tweet_hilo_limpio}\n\n")
                        if not DRY_RUN:
                            reply_id = publicar_tweet(tweet_hilo_limpio, in_reply_to_tweet_id=reply_id)
            else:
                print(f"No se pudo obtener el ranking {cat.upper()}.")

    # ---------------------------------------------------------
    # BLOQUE 5: PROMO APP (Modo manual o forzado)
    # ---------------------------------------------------------
    if args.mode == "promo":
        if procesar_tweet_promocional(partidos_arg, APP_URL, reporte_texto, force=True):
            hay_contenido = True

    # ---------------------------------------------------------
    # ENVÍO DE EMAIL
    # ---------------------------------------------------------
    if hay_contenido:
        print("\n📧 Generando reporte por email...")
        cuerpo_completo = "".join(reporte_texto)
        # enviar_reporte_email(cuerpo_completo)
        pass
    else:
        print("\n📭 No hay contenido relevante para enviar en este modo.")

    print("\n✨ PROCESO FINALIZADO ✨")

if __name__ == "__main__":
    main()
