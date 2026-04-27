import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN Y ESTILO COMPACTO
st.set_page_config(page_title="Stats Lab Pro", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #050a14 0%, #0d1b2a 40%, #1e3a8a 80%, #3b82f6 100%);
        background-attachment: fixed;
        color: #ffffff;
    }
    
    /* REDUCIR ESPACIADO GENERAL */
    [data-testid="stVerticalBlock"] {
        gap: 0.5rem !important;
    }
    
    /* FILAS COMPACTAS Y SIMÉTRICAS */
    .row-wrapper {
        margin-bottom: 6px !important; /* Separación sutil entre filas */
    }

    .table-cell {
        border: 1px solid #ffffff;
        background-color: #0b1221;
        height: 35px; /* Altura reducida */
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 0.85rem;
    }

    .header-cell {
        border: 1px solid #ffffff;
        background-color: #1a2639;
        font-weight: 900;
        text-transform: uppercase;
        font-size: 0.7rem;
        height: 40px; /* Encabezado más bajo */
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 4px;
    }

    /* MÉTRICAS COMPACTAS */
    .metric-container {
        border: 1px solid #ffffff;
        text-align: center;
        padding: 8px;
        background: rgba(0,0,0,0.4);
    }

    /* BOTONES DELGADOS */
    .stButton > button {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid #ffffff !important;
        color: white !important;
        border-radius: 0px !important;
        height: 35px !important; /* Misma altura que las celdas */
        width: 100% !important;
        padding: 0px !important;
        font-size: 0.75rem !important;
        font-weight: 800 !important;
        text-transform: uppercase;
    }

    .stButton > button:hover {
        background-color: #ffffff !important;
        color: #0d1b2a !important;
    }
    
    /* Ajustar inputs para que no se vean gigantes */
    .stNumberInput input, .stTextInput input {
        height: 35px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h2 style="text-transform: uppercase; margin-bottom:10px;">STATS LAB PERFORMANCE TRACKER</h2>', unsafe_allow_html=True)

# 2. LÓGICA DE DATOS
if 'filas' not in st.session_state:
    st.session_state.filas = []
if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

# 3. PANEL DE INGRESO (STRICTLY COMPACT)
with st.container():
    def_temp, def_pj, def_g, def_a = ("", 0, 0, 0)
    if st.session_state.edit_index is not None:
        e = st.session_state.filas[st.session_state.edit_index]
        def_temp, def_pj, def_g, def_a = e['TEMP'], e['PJ'], e['GOLES'], e['ASIST']

    c1, c2, c3, c4 = st.columns([2.5, 1, 1, 1])
    t_in = c1.text_input("Temp/Mes", value=def_temp)
    p_in = c2.number_input("PJ", min_value=0, value=def_pj)
    g_in = c3.number_input("Goles", min_value=0, value=def_g)
    a_in = c4.number_input("Asist", min_value=0, value=def_a)

    b1, b2 = st.columns(2)
    with b1:
        txt = "GUARDAR" if st.session_state.edit_index is not None else "AGREGAR"
        if st.button(txt):
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
    with b2:
        if st.button("LIMPIAR"):
            st.session_state.filas = []
            st.session_state.edit_index = None
            st.rerun()

# 4. MÉTRICAS PEQUEÑAS
if st.session_state.filas:
    df = pd.DataFrame(st.session_state.filas)
    m1, m2, m3, m4, m5 = st.columns(5)
    metrics = [("PJ", int(df["PJ"].sum())), ("GOLES", int(df["GOLES"].sum())), 
               ("ASIST", int(df["ASIST"].sum())), ("G/A", int(df["GA"].sum())), 
               ("AVG", round(df["AVG"].mean(), 1))]
    for col, (l, v) in zip([m1, m2, m3, m4, m5], metrics):
        col.markdown(f'<div class="metric-container"><span style="font-size:0.7rem; color:#aaa;">{l}</span><br><b>{v}</b></div>', unsafe_allow_html=True)

st.write("")

# 5. TABLA COMPACTA
if st.session_state.filas:
    anchos = [1.3, 0.5, 0.5, 0.7, 0.8, 0.7, 0.5, 0.7, 0.5, 0.6, 0.6]
    
    h = st.columns(anchos)
    headers = ["TEMP", "PJ", "G", "G/R", "AST", "A/R", "G/A", "G/A/R", "AVG", "", ""]
    for col, txt in zip(h, headers):
        if txt: col.markdown(f'<div class="header-cell">{txt}</div>', unsafe_allow_html=True)

    for i, f in enumerate(st.session_state.filas):
        st.markdown('<div class="row-wrapper">', unsafe_allow_html=True)
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
            if st.button("EDIT", key=f"ed_{i}"):
                st.session_state.edit_index = i
                st.rerun()
        with r[10]:
            if st.button("DEL", key=f"de_{i}"):
                st.session_state.filas.pop(i)
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
