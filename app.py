import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Stats Lab", layout="wide")

# CSS para fondo oscuro, degradado y diseño unificado
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
        letter-spacing: -1.5px;
        text-transform: uppercase;
        color: #ffffff;
        line-height: 1;
        margin-bottom: 20px;
    }

    h3, p, span, label {
        font-family: 'Verdana', sans-serif !important;
        font-weight: 700 !important;
        color: #ffffff !important;
    }

    /* Unificar estilo de inputs y botones */
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
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #4facfe;
        color: #ffffff;
        border-color: #4facfe;
    }

    [data-testid="stDataFrame"] {
        border: 2px solid #ffffff;
        background-color: rgba(0, 0, 0, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">STATS LAB<br>PERFORMANCE TRACKER</h1>', unsafe_allow_html=True)

if 'filas' not in st.session_state:
    st.session_state.filas = []

# --- FILA DE ENTRADA UNIFICADA ---
c1, c2, c3, c4, c5, c6 = st.columns([2, 1, 1, 1, 1.5, 1.5])

with c1:
    temp = st.text_input("TEMPORADA", placeholder="ABRIL")
with c2:
    pj = st.number_input("PJ", min_value=1, value=1)
with c3:
    goles = st.number_input("GOLES", min_value=0, value=0)
with c4:
    asist = st.number_input("ASIST", min_value=0, value=0)
with c5:
    btn_add = st.button("AÑADIR")
with c6:
    btn_clear = st.button("BORRAR")

if btn_add:
    g_rate = round(goles / pj, 2)
    a_rate = round(asist / pj, 2)
    ga_total = goles + asist
    ga_rate = round(ga_total / pj, 2)
    
    if ga_rate >= 6:
        avg = 10.0
    elif ga_rate <= 0:
        avg = 0.0
    else:
        avg = round((ga_rate * 10) / 6, 1)

    # Nombres de columnas consistentes
    st.session_state.filas.append({
        "TEMPORADA": temp,
        "PJ": pj,
        "GOLES": goles,
        "G RATE": g_rate,
        "ASIST": asist,
        "A RATE": a_rate,
        "G/A": ga_total,
        "G/A RATE": ga_rate,
        "AVG": avg
    })
    st.rerun()

if btn_clear:
    st.session_state.filas = []
    st.rerun()

st.divider()

# --- RESULTADOS ---
if st.session_state.filas:
    df = pd.DataFrame(st.session_state.filas)
    
    col_m1, col_m2, col_m3 = st.columns(3)
    # Aquí estaba el error: usamos "GOLES" en lugar de "G"
    col_m1.metric("TOTAL PJ", df["PJ"].sum())
    col_m2.metric("TOTAL GOLES", df["GOLES"].sum())
    col_m3.metric("AVG GLOBAL", f"{round(df['AVG'].mean(), 1)}")

    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("SISTEMA ONLINE: INGRESA DATOS.")
