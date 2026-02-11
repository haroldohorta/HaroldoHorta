import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
from datetime import datetime

# ==========================================
# 📷 CONFIGURACIÓN: LEGADO HAROLDO HORTA
# ==========================================
st.set_page_config(
    page_title="Atlas Haroldo Horta | Archivo",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos "Darkroom" (Cuarto Oscuro)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e6e6e6; }
    h1, h2, h3 { color: #ff9f1c; font-family: 'Helvetica', sans-serif; }
    .stMetric { background-color: #262730; border-left: 5px solid #ff9f1c; }
    div[data-testid="stExpander"] details summary p { color: #ff9f1c; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🧠 CARGA DE DATOS (INTELIGENTE)
# ==========================================
@st.cache_data
def cargar_datos():
    # Buscamos el JSON en lugares probables
    rutas_posibles = [
        "data/puntos_mapa.json", 
        "puntos_mapa.json", 
        "F:/data/puntos_mapa.json"
    ]
    
    for ruta in rutas_posibles:
        if os.path.exists(ruta):
            try:
                with open(ruta, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return pd.DataFrame(data), ruta
            except Exception as e:
                continue
    
    return pd.DataFrame(), None

df, ruta_cargada = cargar_datos()

# ==========================================
# 🧭 BARRA LATERAL
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/ff9f1c/camera.png", width=60)
    st.title("ARCHIVO H.H.")
    st.caption("Memoria, Etnografía y Territorio")
    st.divider()
    
    if not df.empty:
        st.success(f"✅ Índice Cargado\n({len(df)} Registros)")
        
        # --- FILTROS ---
        st.subheader("🔍 Filtros de Búsqueda")
        
        # Filtro 1: Capa (Categoría)
        if 'capa' in df.columns:
            capas_disponibles = sorted(df['capa'].unique())
            capas_sel = st.multiselect(
                "Categoría:",
                options=capas_disponibles,
                default=capas_disponibles
            )
        else:
            capas_sel = []

        # Filtro 2: Zona (Lugar específico)
        if 'zona' in df.columns:
            zonas_disponibles = sorted(df['zona'].unique())
            zona_sel = st.multiselect(
                "Lugar / Zona:",
                options=zonas_disponibles,
                default=[] # Por defecto vacío para mostrar todo
            )
        
        # Aplicar Lógica de Filtrado
        df_filtrado = df[df['capa'].isin(capas_sel)]
        
        if zona_sel:
            df_filtrado = df_filtrado[df_filtrado['zona'].isin(zona_sel)]
            
    else:
        st.error("⚠️ No se encontró 'puntos_mapa.json'")
        df_filtrado = pd.DataFrame()

# ==========================================
# 🗺️ EL MAPA (Geografía del Legado)
# ==========================================
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Atlas Haroldo Horta")
    st.markdown("### *Rescate de Trayectorias: 1990 - 2026*")

with col2:
    if not df.empty:
        st.metric("Imágenes en Vista", len(df_filtrado))

st.divider()

# Solo mostramos mapa si hay datos
if not df_filtrado.empty:
    fig = px.scatter_mapbox(
        df_filtrado,
        lat="lat",
        lon="lon",
        hover_name="zona",
        hover_data=["capa", "relato"],
        color="capa",
        zoom=2,
        height=600,
        mapbox_style="carto-darkmatter",
        title="Distribución Geográfica"
    )
    # Personalización de puntos
    fig.update_traces(marker=dict(size=12, opacity=0.8))
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    
    st.plotly_chart(fig, use_container_width=True)

    # ==========================================
    # 🖼️ GALERÍA INMERSIVA (GRID INFINITO)
    # ==========================================
    st.divider()
    st.subheader(f"📸 Galería Visual ({len(df_filtrado)} elementos)")
    
    # Checkbox para depuración (ocultar errores)
    mostrar_errores = st.checkbox("Ocultar imágenes no encontradas", value=True)

    # Grid de 4 columnas
    cols = st.columns(4)
    
    # Contador para distribuir en columnas
    contador_visual = 0
    
    for idx, row in df_filtrado.iterrows():
        ruta_img = row.get('thumb', '')
        existe = os.path.exists(ruta_img)
        
        # Si decidimos ocultar errores y no existe, saltamos
        if mostrar_errores and not existe:
            continue
            
        # Asignar columna rotativa (0, 1, 2, 3)
        with cols[contador_visual % 4]:
            if existe:
                st.image(ruta_img, caption=f"{row['zona']} | {row['capa']}", use_container_width=True)
            else:
                # Placeholder si no existe la imagen
                st.markdown(f"""
                <div style="border: 1px dashed #555; border-radius: 5px; padding: 20px; text-align: center; margin-bottom: 20px;">
                    <h3 style="color: #444;">🚫</h3>
                    <small style="color: #666;">Imagen no hallada:<br>{ruta_img}</small>
                </div>
                """, unsafe_allow_html=True)
        
        contador_visual += 1

else:
    st.info("📡 Esperando conexión con la base de datos...")
    st.warning("Verifica que hayas ejecutado 'Scripts/unificar_atlas.py' para generar el índice.")

# ==========================================
# 📂 PIE DE PÁGINA (Técnico)
# ==========================================
st.divider()
col_f1, col_f2 = st.columns(2)
with col_f1:
    st.caption(f"📍 Fuente: {ruta_cargada}")
with col_f2:
    st.caption(f"🕒 Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M')}")