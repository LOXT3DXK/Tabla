import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN Y ESTILO
st.set_page_config(page_title="Stats Lab", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #000814 0%, #001d3d 100%);
        background-attachment: fixed;
        color: #ffffff;
    }
    .main-title {
        font-family: 'Arial Black', sans-serif;
        font-size: 2.5rem;
        text-transform: uppercase;
        color: #ffffff;
        line-height: 1;
        margin-bottom: 20px;
    }
    .stNumberInput input, .stTextInput input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid #ffffff !important;
        color: white !important;
        border-radius: 0px !important;
        height: 45px !important;
    }
    .stButton>button {
        width: 100%;
        background-color: #ffffff;
        color: #000814;
        font-weight: 900;
        text-transform: uppercase;
        border-radius: 0px;
        border: 2px solid #ffffff;
        height: 45px;
        margin-top: 28px; 
    }
    .stButton>button:hover {
        background-color: #4facfe;
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">STATS LAB<br>PERFORMANCE TRACKER</h1>', unsafe_allow_html=True)

# 2. INICIALIZACIÓN DE DATOS
# Definimos las columnas exactas para evitar el KeyError
COLUMNAS_SISTEMA = ["TEMPORADA", "PJ", "GOLES", "G RATE", "ASIST", "A RATE", "G/A", "G/A RATE", "AVG"]

if 'filas' not in st.session_state:
    st.session_state.filas = []

# 3. INTERFAZ DE ENTRADA
c1, c2, c3, c4, c5, c6 = st.columns([2, 1, 1, 1, 1.5, 1.5])

with c1:
    temp = st.text_input("TEMPORADA", placeholder="ABRIL")
with c2:
    pj_input = st.number_input("PJ", min_value=1, value=1)
with c3:
    goles_input = st.number_input("GOLES", min_value=0, value=0)
with c4:
    asist_input = st.number_input("ASIST", min_value=0, value=0)
with c5:
    btn_add = st.button("AÑADIR")
with c6:
    btn_clear = st.button("BORRAR")

# LÓGICA DE BOTONES
if btn_add:
    g_rate = round(goles_input / pj_input, 2)
    a_rate = round(asist_input / pj_input, 2)
    ga_total = goles_input + asist_input
    ga_rate = round(ga_total / pj_input, 2)
    
    # Tu fórmula de AVG
    if ga_rate >= 6: avg = 10.0
    elif ga_rate <= 0: avg = 0.0
    else: avg = round((ga_rate * 10) / 6, 1)

    # Insertamos con los nombres exactos de COLUMNAS_SISTEMA
    nueva_entrada = {
        "TEMPORADA": temp,
        "PJ": pj_input,
        "GOLES": goles_input,
        "G RATE": g_rate,
        "ASIST": asist_input,
        "A RATE": a_rate,
        "G/A": ga_total,
        "G/A RATE": ga_rate,
        "AVG": avg
    }
    st.session_state.filas.append(nueva_entrada)
    st.rerun()

if btn_clear:
    st.session_state.filas = []
    st.rerun()

st.divider()

# 4. RENDERIZADO DE RESULTADOS
# Creamos el DataFrame siempre con las columnas base para que no falle
if st.session_state.filas:
    df = pd.DataFrame(st.session_state.filas)
else:
    df = pd.DataFrame(columns=COLUMNAS_SISTEMA)

if not df.empty:
    col_m1, col_m2, col_m3 = st.columns(3)
    # Usamos .get() o verificamos la columna para seguridad extra
    col_m1.metric("TOTAL PJ", int(df["PJ"].sum()))
    col_m2.metric("TOTAL GOLES", int(df["GOLES"].sum()))
    col_m3.metric("AVG GLOBAL", f"{round(df['AVG'].mean(), 1)}")

    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("SISTEMA ONLINE: INGRESA DATOS EN LA FILA SUPERIOR.")
