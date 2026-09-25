import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.')

from bot.redactor import detectar_torneo_destacado, generar_tweet_promocional
from bot.historial import debe_publicar_promo, registrar_promo_publicada, _cargar_cache, _guardar_cache
from datetime import datetime, timezone, timedelta

def main():
    print("=" * 60)
    print("🧪 TEST DE TWEETS PROMOCIONALES DE LA APP 🧪")
    print("=" * 60)

    # 1. Probar detección de torneo masivo: Roland Garros
    p_rg = [{'tournament_name': 'Roland Garros - Men Singles', 'event_type_type': 'Grand Slam'}]
    nombre, tag, es_masivo = detectar_torneo_destacado(p_rg)
    print(f"\n1. Torneo detectado: {nombre} | Tag: {tag} | Masivo: {es_masivo}")
    assert es_masivo is True
    assert tag == "#RolandGarros"

    # 2. Probar detección de Copa Davis
    p_davis = [{'tournament_name': 'Davis Cup World Group', 'event_type_type': 'Davis Cup'}]
    nombre_d, tag_d, es_masivo_d = detectar_torneo_destacado(p_davis)
    print(f"2. Torneo detectado: {nombre_d} | Tag: {tag_d} | Masivo: {es_masivo_d}")
    assert es_masivo_d is True
    assert tag_d == "#CopaDavis"

    # 3. Probar generación de tweet promocional masivo
    url_test = "https://doblefalta.com/app"
    tweet_promo_masivo = generar_tweet_promocional(url_test, p_rg)
    assert tweet_promo_masivo is not None
    # Limpiar marcadores
    limpio_masivo = "\n".join([l for l in tweet_promo_masivo.split('\n') if not l.startswith('---')]).strip()
    print(f"\n3. Tweet Promo Masivo ({len(limpio_masivo)} caracteres):")
    print(limpio_masivo)
    assert len(limpio_masivo) <= 280, f"Excede 280 caracteres: {len(limpio_masivo)}"
    assert url_test in limpio_masivo
    assert "#RolandGarros" in limpio_masivo

    # 4. Probar generación de tweet promocional regular (sin torneo masivo)
    p_challenger = [{'tournament_name': 'Challenger Villa Maria', 'event_type_type': 'Challenger'}]
    tweet_promo_reg = generar_tweet_promocional(url_test, p_challenger)
    limpio_reg = "\n".join([l for l in tweet_promo_reg.split('\n') if not l.startswith('---')]).strip()
    print(f"\n4. Tweet Promo Regular ({len(limpio_reg)} caracteres):")
    print(limpio_reg)
    assert len(limpio_reg) <= 280, f"Excede 280 caracteres: {len(limpio_reg)}"
    assert url_test in limpio_reg

    # 5. Probar control de frecuencia (cada 3 días)
    cache = _cargar_cache()
    promo_anterior = cache.get("ultima_promo_app")
    
    # Simular que nunca se publicó promo
    cache["ultima_promo_app"] = None
    _guardar_cache()
    assert debe_publicar_promo(frecuencia_dias=3) is True, "Debe publicar si nunca hubo promo"

    # Simular que se publicó hoy
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    registrar_promo_publicada(limpio_reg, fecha_hoy=fecha_hoy)
    assert debe_publicar_promo(frecuencia_dias=3, fecha_hoy=fecha_hoy) is False, "No debe publicar si ya se publicó hoy"

    # Simular que pasaron 2 días (no debe publicar)
    fecha_hace_2 = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
    cache["ultima_promo_app"] = fecha_hace_2
    _guardar_cache()
    assert debe_publicar_promo(frecuencia_dias=3, fecha_hoy=fecha_hoy) is False, "No debe publicar con solo 2 días"

    # Simular que pasaron 3 días (debe publicar)
    fecha_hace_3 = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
    cache["ultima_promo_app"] = fecha_hace_3
    _guardar_cache()
    assert debe_publicar_promo(frecuencia_dias=3, fecha_hoy=fecha_hoy) is True, "Debe publicar si pasaron 3 días"

    # Restaurar valor previo
    cache["ultima_promo_app"] = promo_anterior
    _guardar_cache()
    print("\n5. Control de frecuencia (3 días): comprobado con éxito.")

    print("\n" + "=" * 60)
    print("🎉 ¡TODOS LOS TESTS DE PROMO PASARON EXITOSAMENTE! 🎉")
    print("=" * 60)

if __name__ == "__main__":
    main()
