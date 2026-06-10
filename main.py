import sys
import argparse
from datetime import datetime
from bot.api_tennis import TennisAPI
from bot.filtros import filtrar_argentinos, agrupar_por_torneo, es_agenda, es_actualizacion_en_vivo, es_finalizado
from bot.redactor import generar_tweet_agenda, generar_tweet_actualizacion, generar_tweet_finalizado, generar_tweet_ranking, generar_hilo_ranking_argentinos
from bot.twitter import publicar_tweet
from bot.config import DRY_RUN
from bot.mailer import enviar_reporte_email
from bot.historial import cargar_reportados, guardar_reportado, guardar_reportados_batch, limpiar_historial

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

# Configuración de salida para consola en Windows (emojis)
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    parser = argparse.ArgumentParser(description="Bot Doble Falta Tenis")
    parser.add_argument("--mode", type=str, default="all", choices=["agenda", "live", "final", "ranking", "all"],
                        help="Modo de ejecución: agenda, live, final o all (por defecto)")
    parser.add_argument("--incremental", action="store_true", 
                        help="Si es True, solo reporta lo nuevo desde la última ejecución")
    args = parser.parse_args()

    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
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
        # Limpiamos el historial del día anterior al inicio de la nueva jornada
        print("🧹 Limpiando historial de reportados del día anterior...")
        limpiar_historial()
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
        
        # Filtro incremental: no repetir partidos ya reportados
        if args.incremental:
            reportados = cargar_reportados()
            partidos_fin = [p for p in partidos_fin if p.get('event_key') not in reportados]
            print(f"Modo incremental activo. Partidos nuevos encontrados: {len(partidos_fin)}")

        if partidos_fin:
            hay_contenido = True
            agrupados = agrupar_por_torneo(partidos_fin)
            for torneo, lista in agrupados.items():
                tweets = generar_tweet_finalizado(torneo, lista)
                reply_id = None
                for t in tweets:
                    t_limpio = limpiar_tweet(t)
                    reporte_texto.append(f"[FINALIZADO - {torneo}]\n{t_limpio}\n\n")
                    print(f"Texto generado para {torneo} (Finalizado)")
                    if not DRY_RUN:
                        reply_id = publicar_tweet(t_limpio, in_reply_to_tweet_id=reply_id)
                
                # Si es incremental, marcar como reportados para la próxima (batch)
                if args.incremental:
                    keys_reportar = [p.get('event_key') for p in lista]
                    guardar_reportados_batch(keys_reportar)
        else:
            print("No hay resultados finales (nuevos) para reportar.")



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
