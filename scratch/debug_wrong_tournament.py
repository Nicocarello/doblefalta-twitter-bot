import sys
import os
from datetime import datetime

# Añadir el directorio raíz al path para importar bot
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bot.api_tennis import TennisAPI

def main():
    api = TennisAPI()
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    print(f"Buscando partidos para la fecha: {fecha_hoy}")
    
    partidos = api.obtener_partidos_hoy(fecha_hoy)
    print(f"Total partidos hoy: {len(partidos)}")
    
    encontrados = []
    for p in partidos:
        p1 = p.get('event_first_player', '')
        p2 = p.get('event_second_player', '')
        if "Inisan" in p1 or "Inisan" in p2 or "Larraya" in p1 or "Larraya" in p2:
            encontrados.append(p)
            
    if encontrados:
        for idx, p in enumerate(encontrados):
            print(f"\n--- Partido {idx + 1} ---")
            for k, v in p.items():
                print(f"{k}: {v}")
    else:
        print("No se encontraron partidos de Inisan o Larraya en la fecha actual.")

if __name__ == "__main__":
    main()
