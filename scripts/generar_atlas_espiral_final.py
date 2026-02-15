import os
import json
import pandas as pd

# --- CONFIGURACIÓN ---
DIR_FOTOS = r"F:\fotos"
CSV_ZONAS = r"F:\data\zonas.csv"
JSON_OUT = r"F:\data\puntos_mapa.json"

def limpiar_titulo(n):
    # 'miliciano_herido.webp' -> 'Miliciano herido'
    base = n.replace(".webp","").replace("_", " ").split('(')[0].split('_copy')[0].strip()
    return base.capitalize()

def generar_atlas_espiral_perfecto():
    # 1. Cargamos el JSON actual para no perder tus relatos manuales
    puntos_existentes = {}
    if os.path.exists(JSON_OUT):
        try:
            with open(JSON_OUT, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                puntos_existentes = {p['id']: p for p in datos}
            print(f"📖 Relatos previos cargados.")
        except:
            print("⚠️ No se pudo cargar el JSON previo, se creará uno nuevo.")

    # 2. Cargamos el diccionario de coordenadas
    df_zonas = pd.read_csv(CSV_ZONAS)
    zonas_dict = df_zonas.set_index('zona').to_dict('index')

    puntos_finales = []
    
    # 3. Escaneo de carpetas
    for carpeta in os.listdir(DIR_FOTOS):
        ruta_c = os.path.join(DIR_FOTOS, carpeta)
        if not os.path.isdir(ruta_c) or carpeta == "panos": continue

        # Identificamos Capa y Zona para que coincida con tu getStyle()
        # Identificamos Capa y Zona para que coincida con tu getStyle()
        zona_key = None
        capa_nombre = "Crónica / Etnografía" # Default Rojo

        if carpeta.startswith("pub_"):
            zona_key = carpeta.replace("pub_", "")
            capa_nombre = "Crónica / Etnografía"
        elif carpeta.startswith("fly_"):
            zona_key = carpeta.replace("fly_", "")
            capa_nombre = "Vuelo Aéreo"
        elif carpeta.startswith("nomad_"):
            zona_key = carpeta.replace("nomad_", "")
            capa_nombre = "Bitácora Nómada"
        elif carpeta.startswith("narrativa_"): # 👈 ¡NUEVA CAPA PREPARADA!
            zona_key = carpeta.replace("narrativa_", "")
            capa_nombre = "Narrativa Sonora"

        # EL PORTERO DE LA DISCOTECA: Solo pasa si zona_key está en el CSV
        if zona_key and zona_key in zonas_dict:
            info_gps = zonas_dict[zona_key]
            
            for archivo in os.listdir(ruta_c):
                if archivo.lower().endswith(".webp"):
                    foto_id = archivo
                    
                    # SI YA EXISTE: Mantenemos el relato, pero actualizamos la ruta y GPS
                    if foto_id in puntos_existentes:
                        punto = puntos_existentes[foto_id]
                        punto["lat"] = info_gps['lat']
                        punto["lon"] = info_gps['lon']
                        punto["capa"] = capa_nombre
                        punto["thumb"] = f"fotos/{carpeta}/{archivo}" # 👈 Blindaje
                        punto["full"] = f"fotos/{carpeta}/{archivo}"  # 👈 Blindaje
                        puntos_finales.append(punto)
                    else:
                        # SI ES NUEVO: Creamos el bloque completo
                        puntos_finales.append({
                            "id": foto_id,
                            "lat": info_gps['lat'],
                            "lon": info_gps['lon'],
                            "zona": zona_key,
                            "capa": capa_nombre,
                            "titulo": limpiar_titulo(archivo),
                            "thumb": f"fotos/{carpeta}/{archivo}",
                            "full": f"fotos/{carpeta}/{archivo}",
                            "rating": 5,
                            "descripcion": info_gps['descripcion'],
                            "relato": "Pendiente de relato de Haroldo..."
                        })

    # 4. Guardar resultado
    with open(JSON_OUT, 'w', encoding='utf-8') as f:
        json.dump(puntos_finales, f, indent=2, ensure_ascii=False)
    
    print(f"\n🚀 ¡Misión cumplida! {len(puntos_finales)} puntos listos para el efecto espiral.")

if __name__ == "__main__":
    generar_atlas_espiral_perfecto()