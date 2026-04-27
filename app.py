import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN Y ESTILO
st.set_page_config(page_title="Stats Lab Pro", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #0d1b2a 0%, #1e3a8a 100%);
        background-attachment: fixed;
        color: #ffffff;
    }
    
    .main-title { 
        font-family: 'Arial Black', sans-serif; 
        font-size: 2.5rem; 
        text-transform: uppercase; 
        margin-bottom: 20px;
    }

    /* ESTILO DE INPUTS SIN BORDES TOTALES */
    .stTextInput div div input, .stNumberInput div div input {
        background-color: rgba(0, 0, 0, 0.2) !important;
        border: none !important;
        border-bottom: 2px solid rgba(255, 255, 255, 0.5) !important;
        color: white !important;
        border-radius: 0px !important;
        font-weight: 700 !important;
    }

    /* CELDAS DE LA TABLA */
    .table-cell {
        border: 1px solid #ffffff;
        padding: 8px;
        text-align: center;
        background-color: rgba(255, 255, 255, 0.05);
        min-height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        color: white;
    }

    .header-cell {
        border: 1px solid #ffffff;
        background-color: rgba(255, 255, 255, 0.2);
        font-weight: 900;
        text-transform: uppercase;
        font-size: 0.8rem;
        padding: 8px;
        text-align: center;
    }

    .stButton>button {
        background-color: transparent !important;
        border: 1px solid #ffffff !important;
        color: white !important;
        border-radius: 0px !important;
        height: 35px !important;
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
    }

    .stButton>button:hover {
        background-color: #ffffff !important;
        color: #0d1b2a !important;
    }

    .metric-box {
        text-align: center;
        padding: 10px;
        border: 1px dashed rgba(255, 255, 255, 0.5);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">STATS LAB<br>PERFORMANCE TRACKER</h1>', unsafe_allow_html=True)

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
    with c1: t_in = st.text_input("Temporada / Mes", value=def_temp)
    # CAMBIO AQUÍ: min_value=0
    with c2: p_in = st.number_input("Partidos", min_value=0, value=def_pj)
    with c3: g_in = st.number_input("Goles", min_value=0, value=def_g)
    with c4: a_in = st.number_input("Asistencias", min_value=0, value=def_a)

    ca, cb = st.columns([1.5, 1.5])
    with ca:
        label_btn = "GUARDAR CAMBIOS" if st.session_state.edit_index is not None else "AGREGAR REGISTRO"
        if st.button(label_btn):
            # Seguridad para evitar división por cero si PJ es 0
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
    with cb:
        if st.button("LIMPIAR TODO"):
            st.session_state.filas = []
            st.session_state.edit_index = None
            st.rerun()

# 4. RESUMEN DE MÉTRICAS
if st.session_state.filas:
    df = pd.DataFrame(st.session_state.filas)
    m1, m2, m3 = st.columns(3)
    with m1: st.markdown(f'<div class="metric-box">TOTAL PJ<br><span style="font-size:1.5rem; font-weight:900;">{int(df["PJ"].sum())}</span></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-box">TOTAL GOLES<br><span style="font-size:1.5rem; font-weight:900;">{int(df["GOLES"].sum())}</span></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-box">AVG GLOBAL<br><span style="font-size:1.5rem; font-weight:900;">{df["AVG"].mean():.1f}</span></div>', unsafe_allow_html=True)

st.divider()

# 5. TABLA TIPO REJILLA
if st.session_state.filas:
    cols_h = st.columns([2, 0.8, 0.8, 1, 1.2, 1, 0.8, 1, 0.8, 0.8, 0.8])
    labels = ["TEMPORADA", "PJ", "GOLES", "G RATE", "ASISTENCIAS", "A RATE", "G/A", "G/A RATE", "AVG", "EDIT", "DEL"]
    for col, text in zip(cols_h, labels):
        col.markdown(f'<div class="header-cell">{text}</div>', unsafe_allow_html=True)

    for i, f in enumerate(st.session_state.filas):
        row = st.columns([2, 0.8, 0.8, 1, 1.2, 1, 0.8, 1, 0.8, 0.8, 0.8])
        row[0].markdown(f'<div class="table-cell">{f["TEMP"]}</div>', unsafe_allow_html=True)
        row[1].markdown(f'<div class="table-cell">{f["PJ"]}</div>', unsafe_allow_html=True)
        row[2].markdown(f'<div class="table-cell">{f["GOLES"]}</div>', unsafe_allow_html=True)
        row[3].markdown(f'<div class="table-cell">{f["G_RATE"]:.2f}</div>', unsafe_allow_html=True)
        row[4].markdown(f'<div class="table-cell">{f["ASIST"]}</div>', unsafe_allow_html=True)
        row[5].markdown(f'<div class="table-cell">{f["A_RATE"]:.2f}</div>', unsafe_allow_html=True)
        row[6].markdown(f'<div class="table-cell">{f["GA"]}</div>', unsafe_allow_html=True)
        row[7].markdown(f'<div class="table-cell">{f["GA_RATE"]:.2f}</div>', unsafe_allow_html=True)
        row[8].markdown(f'<div class="table-cell">{f["AVG"]}</div>', unsafe_allow_html=True)
        
        if row[9].button("EDIT", key=f"e_{i}"):
            st.session_state.edit_index = i
            st.rerun()
        if row[10].button("DEL", key=f"d_{i}"):
            st.session_state.filas.pop(i)
            st.rerun()
else:
    st.info("SISTEMA ONLINE. INGRESE DATOS.")
