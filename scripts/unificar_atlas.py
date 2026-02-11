import os
import pandas as pd
import json

# ================= CONFIGURACIÓN =================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_FOTOS = os.path.join(BASE_DIR, "fotos")
RUTA_CSV = os.path.join(BASE_DIR, "data", "zonas.csv")
ARCHIVO_SALIDA = os.path.join(BASE_DIR, "data", "puntos_mapa.json")

CATEGORIAS = {
    "pub_": "Crónica & Etnografía",
    "nomad_": "Bitácora Nómada",
    "fly_": "Registro Aéreo",
    "nav_": "Registro Naval"
}

# Extensiones permitidas
EXTS = ('.jpg', '.jpeg', '.png', '.webp', '.gif')

def escanear_todo():
    print("🚀 Iniciando Escaneo Profundo del Atlas...")

    if not os.path.exists(RUTA_CSV):
        print("❌ Faltan datos maestros (zonas.csv)")
        return

    df_zonas = pd.read_csv(RUTA_CSV)
    df_zonas['zona'] = df_zonas['zona'].astype(str).str.strip().str.lower()
    
    # Convertimos el DF a un diccionario para búsqueda rápida
    info_zonas = {}
    for _, row in df_zonas.iterrows():
        info_zonas[row['zona']] = {
            'lat': float(row['lat']), 
            'lon': float(row['lon']), 
            'desc': row['descripcion']
        }

    todos_los_puntos = []

    # Recorrer TODAS las carpetas y subcarpetas
    for root, dirs, files in os.walk(RUTA_FOTOS):
        # Detectar zona basada en el nombre de la carpeta actual
        nombre_carpeta = os.path.basename(root).lower()
        
        # Limpieza de prefijos para hallar la zona
        zona_detectada = nombre_carpeta
        categoria_detectada = "Archivo General"
        
        for pre, cat in CATEGORIAS.items():
            if nombre_carpeta.startswith(pre):
                categoria_detectada = cat
                zona_detectada = nombre_carpeta.replace(pre, "")
                break
        
        # Si esta carpeta es una "Zona Conocida" (está en el CSV)
        if zona_detectada in info_zonas:
            datos_zona = info_zonas[zona_detectada]
            
            # Agregamos CADA foto como un punto
            fotos_encontradas = [f for f in files if f.lower().endswith(EXTS)]
            
            if fotos_encontradas:
                print(f"  📸 Zona {zona_detectada}: {len(fotos_encontradas)} fotos.")
            
            for foto in fotos_encontradas:
                ruta_relativa = os.path.relpath(os.path.join(root, foto), BASE_DIR).replace("\\", "/")
                
                todos_los_puntos.append({
                    "id": foto,
                    "zona": zona_detectada,
                    "capa": categoria_detectada,
                    "lat": datos_zona['lat'],   # Todas las fotos de la zona comparten coordenada
                    "lon": datos_zona['lon'],
                    "thumb": ruta_relativa,     # Ruta directa a la imagen
                    "descripcion": datos_zona['desc']
                })

    # Guardar
    with open(ARCHIVO_SALIDA, 'w', encoding='utf-8') as f:
        json.dump(todos_los_puntos, f, indent=4, ensure_ascii=False)

    print(f"\n✨ ESCANEO COMPLETO: {len(todos_los_puntos)} imágenes indexadas.")

if __name__ == "__main__":
    escanear_todo()