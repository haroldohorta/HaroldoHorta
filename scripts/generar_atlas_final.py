import os
import json
import pandas as pd
import random

# --- RUTAS ---
DIR_FOTOS = r"F:\fotos"
CSV_ZONAS = r"F:\data\zonas.csv"
JSON_OUT = r"F:\data\puntos_mapa.json"

def limpiar_titulo(n):
    return n.replace(".webp","").replace("_", " ").split('(')[0].split('_copy')[0].strip().capitalize()

def generar_atlas_ordenado():
    print("🧹 Limpiando y reconstruyendo Atlas (Omitiendo 'panos')...")
    
    # 1. Cargar Zonas
    df = pd.read_csv(CSV_ZONAS)
    zonas = df.set_index('zona').to_dict('index')

    puntos = []
    # Solo procesamos estos prefijos
    prefijos_validos = ("pub_", "fly_", "nomad_")

    for carpeta in os.listdir(DIR_FOTOS):
        ruta_c = os.path.join(DIR_FOTOS, carpeta)
        
        # OMITIR si no es carpeta o si es la de panos
        if not os.path.isdir(ruta_c) or carpeta == "panos":
            continue
            
        if carpeta.startswith(prefijos_validos):
            # Extraer zona: pub_nicaragua -> nicaragua
            zona_key = carpeta.split('_', 1)[-1]
            
            if zona_key in zonas:
                info = zonas[zona_key]
                
                # Capas según prefijo
                if carpeta.startswith("pub_"): capa = "Crónica & Etnografía"
                elif carpeta.startswith("fly_"): capa = "Vuelo Aéreo"
                else: capa = "Expedición Nómade"

                for f in os.listdir(ruta_c):
                    if f.lower().endswith(".webp"):
                        # JITTER: Dispersión de ~500 metros para que no se tapen
                        lat = info['lat'] + random.uniform(-0.006, 0.006)
                        lon = info['lon'] + random.uniform(-0.006, 0.006)

                        puntos.append({
                            "id": f,
                            "lat": round(lat, 6),
                            "lon": round(lon, 6),
                            "zona": zona_key,
                            "capa": capa,
                            "titulo": limpiar_titulo(f),
                            "thumb": f"fotos/{carpeta}/{f}",
                            "full": f"fotos/{carpeta}/{f}",
                            "descripcion": info['descripcion'],
                            "relato": "Pendiente de relato de Haroldo..."
                        })
                print(f"✅ Carpeta procesada: {carpeta}")
            else:
                print(f"⚠️ Zona '{zona_key}' no existe en zonas.csv. Saltando...")

    # Guardar desde cero (adiós fantasmas)
    with open(JSON_OUT, 'w', encoding='utf-8') as f:
        json.dump(puntos, f, indent=2, ensure_ascii=False)
    
    print(f"\n🚀 ¡LISTO! El Atlas tiene {len(puntos)} puntos perfectamente ubicados.")

if __name__ == "__main__":
    generar_atlas_ordenado()