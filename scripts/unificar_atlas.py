import os
import pandas as pd
import json

# ================= CONFIGURACIÓN =================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_FOTOS = os.path.join(BASE_DIR, "fotos")
RUTA_CSV = os.path.join(BASE_DIR, "data", "zonas.csv")
ARCHIVO_SALIDA = os.path.join(BASE_DIR, "data", "puntos_mapa.json")

# Diccionario de categorías
CATEGORIAS = {
    "pub_": "Crónica & Etnografía",
    "nomad_": "Bitácora Nómada",
    "fly_": "Registro Aéreo",
    "nav_": "Registro Naval"
}

# Extensiones válidas
EXTS = ('.jpg', '.jpeg', '.png', '.webp', '.gif')

def escanear_todo():
    print("🚀 Iniciando Protocolo de Rescate y Sincronización...")

    if not os.path.exists(RUTA_CSV):
        print("❌ ERROR: No encuentro data/zonas.csv")
        return

    # Cargar CSV
    df_zonas = pd.read_csv(RUTA_CSV)
    
    # --- AQUÍ ESTÁ EL TRUCO MAESTRO ---
    # Convertimos lo que dice el CSV al mismo formato "aplanado" de las carpetas
    # 1. Minúsculas. 2. Espacios por guiones bajos. 3. Tildes fuera (básico)
    df_zonas['zona_normalizada'] = df_zonas['zona'].astype(str).str.strip().lower().str.replace(" ", "_")
    # ----------------------------------
    
    # Mapa de coordenadas en memoria (Usamos la clave normalizada para buscar)
    info_zonas = {}
    for _, row in df_zonas.iterrows():
        # Guardamos usando 'san_pedro' como clave, pero mantenemos los datos originales
        clave = row['zona_normalizada']
        info_zonas[clave] = {
            'nombre_real': row['zona'], # Para mostrar "San Pedro" bonito en el mapa
            'lat': float(row['lat']), 
            'lon': float(row['lon']), 
            'desc': row['descripcion']
        }

    todos_los_puntos = []

    # Recorrer el disco
    for root, dirs, files in os.walk(RUTA_FOTOS):
        carpeta_real = os.path.basename(root)
        nombre_lower = carpeta_real.lower() # Esto ya viene con guiones bajos del script anterior
        
        # Detectar Zona
        zona_detectada = nombre_lower
        categoria_detectada = "Archivo General"
        
        for pre, cat in CATEGORIAS.items():
            if nombre_lower.startswith(pre):
                categoria_detectada = cat
                zona_detectada = nombre_lower.replace(pre, "")
                break
        
        # ¿Esta carpeta coincide con alguna del CSV (normalizado)?
        if zona_detectada in info_zonas:
            datos = info_zonas[zona_detectada]
            
            fotos_validas = [f for f in files if f.lower().endswith(EXTS)]
            
            if fotos_validas:
                # Usamos el nombre bonito del CSV para el print
                print(f"  ✅ Zona Rescatada: {datos['nombre_real']} ({len(fotos_validas)} fotos)")
            
            for foto in fotos_validas:
                ruta_completa = os.path.join(root, foto)
                ruta_relativa = os.path.relpath(ruta_completa, BASE_DIR).replace("\\", "/")
                
                if foto.startswith(".") or foto.startswith("._"): continue

                todos_los_puntos.append({
                    "id": foto,
                    "zona": zona_detectada, # Clave técnica (san_pedro) para filtrar
                    "titulo": datos['nombre_real'], # Título bonito (San Pedro)
                    "capa": categoria_detectada,
                    "lat": datos['lat'],
                    "lon": datos['lon'],
                    "thumb": ruta_relativa,
                    "descripcion": datos['desc']
                })

    # Guardar JSON
    with open(ARCHIVO_SALIDA, 'w', encoding='utf-8') as f:
        json.dump(todos_los_puntos, f, indent=4, ensure_ascii=False)

    print(f"\n✨ BASE DE DATOS REPARADA: {len(todos_los_puntos)} imágenes listas.")

if __name__ == "__main__":
    escanear_todo()