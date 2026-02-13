from PIL import Image
import os

ruta_entrada = r"C:\PROYECTOS\entradas\5_estrellas (1).tif"
ruta_salida = r"F:\fotos\reagan_nuclear.jpg"

print("🚁 Iniciando conversión del TIF...")

try:
    img = Image.open(ruta_entrada)
    if img.mode in ("RGBA", "P", "CMYK", "I;16"):
        img = img.convert("RGB")
    
    # Redimensionar a Full HD
    img.thumbnail((1920, 1920), Image.Resampling.LANCZOS)
    img.save(ruta_salida, "JPEG", quality=85, optimize=True)
    
    print(f"✅ Éxito: Guardado en {ruta_salida}")

except Exception as e:
    print(f"❌ Error: {e}")