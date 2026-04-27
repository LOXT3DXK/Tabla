import streamlit as st
import pandas as pd

# 1. ESTILO Y CONFIGURACIÓN
st.set_page_config(page_title="Stats Lab", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(180deg, #000814 0%, #001d3d 100%); background-attachment: fixed; color: white; }
    .main-title { font-family: 'Arial Black', sans-serif; font-size: 2.5rem; text-transform: uppercase; line-height: 1; margin-bottom: 20px; }
    .stNumberInput input, .stTextInput input { background-color: rgba(255, 255, 255, 0.1) !important; border: 2px solid white !important; color: white !important; border-radius: 0px !important; height: 45px !important; }
    .stButton>button { width: 100%; background-color: white; color: #000814; font-weight: 900; text-transform: uppercase; border-radius: 0px; border: 2px solid white; height: 45px; margin-top: 28px; }
    .stButton>button:hover { background-color: #4facfe; color: white; border-color: #4facfe; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">STATS LAB<br>PERFORMANCE TRACKER</h1>', unsafe_allow_html=True)

# 2. GESTIÓN DE ESTADO (CON REINICIO AUTOMÁTICO SI HAY ERROR)
if 'filas' not in st.session_state:
    st.session_state.filas = []

# 3. INTERFAZ DE ENTRADA
c1, c2, c3, c4, c5, c6 = st.columns([2, 1, 1, 1, 1.5, 1.5])

with c1:
    temp_val = st.text_input("TEMPORADA", placeholder="ABRIL")
with c2:
    pj_val = st.number_input("PJ", min_value=1, value=1)
with c3:
    goles_val = st.number_input("GOLES", min_value=0, value=0)
with c4:
    asist_val = st.number_input("ASIST", min_value=0, value=0)

with c5:
    if st.button("AÑADIR"):
        ga_total = goles_val + asist_val
        ga_rate = round(ga_total / pj_val, 2)
        
        # Tu lógica de AVG
        if ga_rate >= 6: avg = 10.0
        elif ga_rate <= 0: avg = 0.0
        else: avg = round((ga_rate * 10) / 6, 1)

        # Guardamos con nombres consistentes
        st.session_state.filas.append({
            "TEMPORADA": temp_val,
            "PJ": pj_val,
            "GOLES": goles_val,
            "G RATE": round(goles_val / pj_val, 2),
            "ASIST": asist_val,
            "A RATE": round(asist_val / pj_val, 2),
            "G/A": ga_total,
            "G/A RATE": ga_rate,
            "AVG": avg
        })
        st.rerun()

with c6:
    if st.button("BORRAR"):
        st.session_state.filas = []
        st.rerun()

st.divider()

# 4. PROCESAMIENTO SEGURO (USANDO .get() PARA EVITAR KEYERROR)
if st.session_state.filas:
    try:
        # Usamos .get(key, 0) para que si no existe la columna, use un 0 en vez de dar error
        total_pj = sum(int(f.get("PJ", 0)) for f in st.session_state.filas)
        total_g = sum(int(f.get("GOLES", 0)) for f in st.session_state.filas)
        
        # Evitar división por cero en el promedio general
        lista_avg = [f.get("AVG", 0) for f in st.session_state.filas]
        prom_avg = round(sum(lista_avg) / len(lista_avg), 1) if lista_avg else 0.0

        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("TOTAL PJ", total_pj)
        col_m2.metric("TOTAL GOLES", total_g)
        col_m3.metric("AVG GLOBAL", prom_avg)

        # Mostrar tabla
        df = pd.DataFrame(st.session_state.filas)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.error("Se detectó un conflicto de datos viejos. Limpiando sesión...")
        st.session_state.filas = []
        st.rerun()
else:
    st.info("SISTEMA ONLINE: INGRESA DATOS.")
