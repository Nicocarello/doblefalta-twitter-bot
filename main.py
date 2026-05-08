import sys
import argparse
from datetime import datetime
from bot.api_tennis import TennisAPI
from bot.filtros import filtrar_argentinos, agrupar_por_torneo, es_agenda, es_actualizacion_en_vivo, es_finalizado
from bot.redactor import generar_tweet_agenda, generar_tweet_actualizacion, generar_tweet_finalizado
# from bot.twitter import publicar_tweet  # Omitimos por ahora
from bot.mailer import enviar_reporte_email

# Configuración de salida para consola en Windows (emojis)
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    parser = argparse.ArgumentParser(description="Bot Doble Falta Tenis")
    parser.add_argument("--mode", type=str, default="all", choices=["agenda", "live", "final", "all"],
                        help="Modo de ejecución: agenda, live, final o all (por defecto)")
    args = parser.parse_args()

    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    print(f"🚀 INICIANDO BOT DOBLE FALTA - MODO: {args.mode.upper()} - FECHA: {fecha_hoy} 🚀")

    api = TennisAPI()
    
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
            enviar_reporte_email(f"Reporte {fecha_hoy}: No se encontraron partidos de tenistas argentinos hoy.")
        return

    # Lista para recolectar todo el texto generado para el mail
    reporte_texto = [f"REPORTE DOBLE FALTA - {fecha_hoy} ({args.mode.upper()})\n", "="*30 + "\n"]
    hay_contenido = False

    # ---------------------------------------------------------
    # BLOQUE 1: AGENDA
    # ---------------------------------------------------------
    if args.mode in ["agenda", "all"]:
        print("\n📅 PROCESANDO BLOQUE: AGENDA...")
        partidos_agenda = [p for p in partidos_arg if es_agenda(p)]
        if partidos_agenda:
            hay_contenido = True
            agrupados = agrupar_por_torneo(partidos_agenda)
            for torneo, lista in agrupados.items():
                texto_tweet = generar_tweet_agenda(torneo, lista)
                reporte_texto.append(f"[AGENDA - {torneo}]\n{texto_tweet}\n\n")
                print(f"Texto generado para {torneo} (Agenda)")
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
                texto_tweet = generar_tweet_actualizacion(torneo, lista)
                reporte_texto.append(f"[EN VIVO - {torneo}]\n{texto_tweet}\n\n")
                print(f"Texto generated para {torneo} (En Vivo)")
        else:
            print("No hay partidos en vivo actualmente.")

    # ---------------------------------------------------------
    # BLOQUE 3: RESULTADOS
    # ---------------------------------------------------------
    if args.mode in ["final", "all"]:
        print("\n🏁 PROCESANDO BLOQUE: RESULTADOS FINALES...")
        partidos_fin = [p for p in partidos_arg if es_finalizado(p)]
        if partidos_fin:
            hay_contenido = True
            agrupados = agrupar_por_torneo(partidos_fin)
            for torneo, lista in agrupados.items():
                texto_tweet = generar_tweet_finalizado(torneo, lista)
                reporte_texto.append(f"[FINALIZADO - {torneo}]\n{texto_tweet}\n\n")
                print(f"Texto generado para {torneo} (Finalizado)")
        else:
            print("No hay resultados finales para reportar.")

    # ---------------------------------------------------------
    # ENVÍO DE EMAIL
    # ---------------------------------------------------------
    if hay_contenido:
        print("\n📧 Generando reporte por email...")
        cuerpo_completo = "".join(reporte_texto)
        enviar_reporte_email(cuerpo_completo)
    else:
        print("\n📭 No hay contenido relevante para enviar en este modo.")

    print("\n✨ PROCESO FINALIZADO ✨")

if __name__ == "__main__":
    main()
