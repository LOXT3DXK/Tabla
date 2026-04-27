import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN Y ESTILO DEFINITIVO
st.set_page_config(page_title="Stats Lab Pro", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #050a14 0%, #0d1b2a 40%, #1e3a8a 80%, #3b82f6 100%);
        background-attachment: fixed;
        color: #ffffff;
    }
    
    .main-title { 
        font-family: 'Arial Black', sans-serif; 
        font-size: 2.5rem; 
        text-transform: uppercase; 
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    /* --- SOLUCIÓN DEFINITIVA DE SIMETRÍA --- */
    /* Eliminamos cualquier espacio automático de Streamlit en la sección de la tabla */
    [data-testid="stVerticalBlock"] > div:has(.header-cell), 
    [data-testid="stVerticalBlock"] > div:has(.table-cell) {
        gap: 0px !important;
        margin: 0px !important;
        padding: 0px !important;
    }

    /* Controlamos el espacio manualmente para que sea idéntico en todos */
    .header-cell, .table-cell {
        margin-bottom: 10px !important; /* Ajusta este número para más o menos separación */
    }

    /* Evita que los botones de EDIT/DEL empujen la fila hacia abajo */
    div[data-testid="stButton"] {
        margin-bottom: 10px !important;
    }
    /* -------------------------------------- */

    .table-cell {
        border: 1px solid #ffffff;
        text-align: center;
        background-color: #0b1221;
        min-height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        color: #ffffff;
    }

    .header-cell {
        border: 1px solid #ffffff;
        background-color: #1a2639;
        font-weight: 900;
        text-transform: uppercase;
        font-size: 0.7rem;
        padding: 10px 2px;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 50px;
    }

    .stButton>button {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid #ffffff !important;
        color: white !important;
        border-radius: 0px !important;
        height: 45px !important;
        width: 100% !important;
        font-weight: 800 !important;
        text-transform: uppercase;
    }

    .metric-box {
        text-align: center;
        padding: 10px;
        border: 1px solid #ffffff;
        background-color: rgba(0,0,0,0.5);
        font-size: 0.8rem;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# (Sección 2, 3 y 4 se mantienen igual...)
if 'filas' not in st.session_state: st.session_state.filas = []
if 'edit_index' not in st.session_state: st.session_state.edit_index = None

# PANEL DE INGRESO (Simplificado para el ejemplo)
c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
with c1: t_in = st.text_input("Temporada / Mes")
with c2: p_in = st.number_input("Partidos", min_value=0)
with c3: g_in = st.number_input("Goles", min_value=0)
with c4: a_in = st.number_input("Asistencias", min_value=0)

if st.button("AGREGAR REGISTRO"):
    if t_in:
        pj_calc = p_in if p_in > 0 else 1
        st.session_state.filas.append({
            "TEMP": t_in, "PJ": p_in, "GOLES": g_in, "G_RATE": round(g_in/pj_calc, 2),
            "ASIST": a_in, "A_RATE": round(a_in/pj_calc, 2), "GA": g_in+a_in, "AVG": 0.0
        })
        st.rerun()

st.write("---")

# 5. TABLA INTEGRADA CON ESPACIADO UNIFICADO
if st.session_state.filas:
    col_config = [1.5, 0.6, 0.6, 0.8, 1, 0.8, 0.6, 0.8, 0.6, 0.6, 0.6]
    
    # Encabezado
    h = st.columns(col_config)
    labels = ["TEMPORADA", "PJ", "GOLES", "G RATE", "ASISTENCIAS", "A RATE", "G/A", "G/A RATE", "AVG", "", ""]
    for col, label in zip(h, labels):
        if label != "":
            col.markdown(f'<div class="header-cell">{label}</div>', unsafe_allow_html=True)

    # Filas de datos
    for i, f in enumerate(st.session_state.filas):
        r = st.columns(col_config)
        r[0].markdown(f'<div class="table-cell">{f["TEMP"]}</div>', unsafe_allow_html=True)
        r[1].markdown(f'<div class="table-cell">{f["PJ"]}</div>', unsafe_allow_html=True)
        r[2].markdown(f'<div class="table-cell">{f["GOLES"]}</div>', unsafe_allow_html=True)
        r[3].markdown(f'<div class="table-cell">{f["G_RATE"]:.2f}</div>', unsafe_allow_html=True)
        r[4].markdown(f'<div class="table-cell">{f["ASIST"]}</div>', unsafe_allow_html=True)
        r[5].markdown(f'<div class="table-cell">{f["A_RATE"]:.2f}</div>', unsafe_allow_html=True)
        r[6].markdown(f'<div class="table-cell">{f["GA"]}</div>', unsafe_allow_html=True)
        r[7].markdown(f'<div class="table-cell">{f["GA"]:.2f}</div>', unsafe_allow_html=True) # GA RATE simplificado
        r[8].markdown(f'<div class="table-cell">{f["AVG"]:.1f}</div>', unsafe_allow_html=True)
        with r[9]: st.button("EDIT", key=f"e_{i}")
        with r[10]: st.button("DEL", key=f"d_{i}")
