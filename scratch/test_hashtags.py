import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from bot.redactor import obtener_hashtag_torneo

# Casos de prueba
casos = [
    # Grand Slams (No deben cambiar, tienen su hashtag propio en mapping o son especiales)
    ("Roland Garros", "WTA", "#RolandGarros"),
    ("Wimbledon", "ATP", "#Wimbledon"),
    ("US Open", "WTA", "#USOpen"),
    ("Australian Open", "ATP", "#AusOpen"),
    
    # Torneos en mapping oficial (No deben cambiar)
    ("Rome", "ATP", "#IBI26"),
    ("Buenos Aires", "ATP", "#IEBMasArgOpen"),
    
    # Genéricos (Deben incluir la categoría)
    ("Coquimbo", "Challenger", "#ChallengerCoquimbo"),
    ("ITF W35 Boca Raton", "ITF", "#ITFW35BocaRaton"),
    ("WTA Rabat", "WTA", "#WTARabat"),
    ("ATP Lyon", "ATP", "#ATPLyon"),
]

print("🧪 PROBANDO GENERACIÓN DE HASHTAGS DE TORNEOS 🧪")
print(f"{'Torneo':<25} | {'Categoría':<10} | {'Esperado':<20} | {'Obtenido':<20} | {'Estado'}")
print("-" * 90)

exito = True
for torneo, cat, esperado in casos:
    obtenido = obtener_hashtag_torneo(torneo, cat)
    status = "✅ OK" if obtenido == esperado else "❌ ERROR"
    if obtenido != esperado:
        exito = False
    print(f"{torneo:<25} | {cat:<10} | {esperado:<20} | {obtenido:<20} | {status}")

if exito:
    print("\n🎉 ¡Todas las pruebas de hashtag pasaron exitosamente!")
else:
    print("\n❌ Algunas pruebas fallaron.")
