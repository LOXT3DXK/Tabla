import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN Y ESTILO (ELIMINACIÓN DE GAP DINÁMICO)
st.set_page_config(page_title="Stats Lab Pro", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #050a14 0%, #0d1b2a 40%, #1e3a8a 80%, #3b82f6 100%);
        background-attachment: fixed;
    }

    /* Forzar que el contenedor de cada columna no tenga margen inferior extra */
    [data-testid="stVerticalBlock"] > div {
        gap: 0rem !important;
    }

    .table-cell {
        border: 1px solid #ffffff;
        background-color: #0b1221;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 0.9rem;
        color: white;
    }

    .header-cell {
        border: 1px solid #ffffff;
        background-color: #1a2639;
        font-weight: 900;
        text-transform: uppercase;
        font-size: 0.7rem;
        height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
    }

    .stButton > button {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid #ffffff !important;
        color: white !important;
        border-radius: 0px !important;
        height: 40px !important;
        width: 100% !important;
        padding: 0px !important;
        margin: 0px !important;
    }

    /* Estilo para los inputs de arriba */
    .stTextInput input, .stNumberInput input {
        background-color: rgba(0, 0, 0, 0.5) !important;
        color: white !important;
        border: 1px solid white !important;
        border-radius: 0px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 style="color:white; text-transform:uppercase;">STATS LAB PERFORMANCE TRACKER</h1>', unsafe_allow_html=True)

# 2. LÓGICA DE DATOS
if 'filas' not in st.session_state:
    st.session_state.filas = []
if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

# 3. PANEL DE INGRESO
with st.container():
    def_temp, def_pj, def_g, def_a = ("", 0, 0, 0)
    if st.session_state.edit_index is not None:
        e = st.session_state.filas[st.session_state.edit_index]
        def_temp, def_pj, def_g, def_a = e['TEMP'], e['PJ'], e['GOLES'], e['ASIST']

    c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
    t_in = c1.text_input("Temporada / Mes", value=def_temp)
    p_in = c2.number_input("Partidos", min_value=0, value=def_pj)
    g_in = c3.number_input("Goles", min_value=0, value=def_g)
    a_in = c4.number_input("Asistencias", min_value=0, value=def_a)

    if st.button("GUARDAR CAMBIOS" if st.session_state.edit_index is not None else "AGREGAR REGISTRO"):
        if t_in:
            pj_calc = p_in if p_in > 0 else 1
            ga = g_in + a_in
            gar = round(ga/pj_calc, 2) if p_in > 0 else 0.0
            avg = 10.0 if gar >= 6 else (0.0 if gar <= 0 else round((gar * 10) / 6, 1))
            nueva_data = {
                "TEMP": t_in, "PJ": p_in, "GOLES": g_in, "G_RATE": round(g_in/pj_calc, 2) if p_in > 0 else 0.0,
                "ASIST": a_in, "A_RATE": round(a_in/pj_calc, 2) if p_in > 0 else 0.0, 
                "GA": ga, "GA_RATE": gar, "AVG": avg
            }
            if st.session_state.edit_index is not None:
                st.session_state.filas[st.session_state.edit_index] = nueva_data
                st.session_state.edit_index = None
            else:
                st.session_state.filas.append(nueva_data)
            st.rerun()

st.write("---")

# 4. TABLA CON SEPARACIÓN CONSTANTE
if st.session_state.filas:
    anchos = [1.5, 0.6, 0.6, 0.8, 1, 0.8, 0.6, 0.8, 0.6, 0.6, 0.6]
    
    # Encabezado (Espacio normal respecto a los inputs)
    h = st.columns(anchos)
    headers = ["TEMPORADA", "PJ", "GOLES", "G RATE", "ASISTENCIAS", "A RATE", "G/A", "G/A RATE", "AVG", "", ""]
    for col, txt in zip(h, headers):
        if txt: col.markdown(f'<div class="header-cell">{txt}</div>', unsafe_allow_html=True)

    # Bucle de filas añadidas
    for i, f in enumerate(st.session_state.filas):
        # El secreto: este div inyectado reduce el espacio que Streamlit pone entre las columnas del bucle
        st.markdown('<div style="margin-top: -10px;"></div>', unsafe_allow_html=True)
        
        r = st.columns(anchos)
        r[0].markdown(f'<div class="table-cell">{f["TEMP"]}</div>', unsafe_allow_html=True)
        r[1].markdown(f'<div class="table-cell">{f["PJ"]}</div>', unsafe_allow_html=True)
        r[2].markdown(f'<div class="table-cell">{f["GOLES"]}</div>', unsafe_allow_html=True)
        r[3].markdown(f'<div class="table-cell">{f["G_RATE"]:.2f}</div>', unsafe_allow_html=True)
        r[4].markdown(f'<div class="table-cell">{f["ASIST"]}</div>', unsafe_allow_html=True)
        r[5].markdown(f'<div class="table-cell">{f["A_RATE"]:.2f}</div>', unsafe_allow_html=True)
        r[6].markdown(f'<div class="table-cell">{f["GA"]}</div>', unsafe_allow_html=True)
        r[7].markdown(f'<div class="table-cell">{f["GA_RATE"]:.2f}</div>', unsafe_allow_html=True)
        r[8].markdown(f'<div class="table-cell">{f["AVG"]:.1f}</div>', unsafe_allow_html=True)
        with r[9]:
            if st.button("EDIT", key=f"edit_{i}"):
                st.session_state.edit_index = i
                st.rerun()
        with r[10]:
            if st.button("DEL", key=f"del_{i}"):
                st.session_state.filas.pop(i)
                st.rerun()
