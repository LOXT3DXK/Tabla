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

    /* INPUTS */
    .stTextInput input, .stNumberInput input {
        background-color: rgba(0, 0, 0, 0.5) !important;
        border: none !important;
        border-bottom: 2px solid #ffffff !important;
        color: white !important;
        border-radius: 0px !important;
        font-weight: 700 !important;
        height: 45px !important;
    }

    /* REJILLA UNIFICADA */
    .table-cell {
        border: 1px solid #ffffff;
        padding: 0px;
        text-align: center;
        background-color: #0b1221;
        min-height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        color: #ffffff;
        width: 100%;
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
        width: 100%;
    }

    /* BOTONES */
    .stButton>button {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid #ffffff !important;
        color: white !important;
        border-radius: 0px !important;
        height: 45px !important;
        width: 100% !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        margin: 0px !important;
    }

    .stButton>button:hover {
        background-color: #ffffff !important;
        color: #0d1b2a !important;
    }

    /* MÉTRICAS */
    .metric-box {
        text-align: center;
        padding: 10px;
        border: 1px solid #ffffff;
        background-color: rgba(0,0,0,0.5);
        font-size: 0.8rem;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 1.4rem;
        font-weight: 900;
        display: block;
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">STATS LAB PERFORMANCE TRACKER</h1>', unsafe_allow_html=True)

# 2. LÓGICA DE DATOS
if 'filas' not in st.session_state:
    st.session_state.filas = []
if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

# 3. PANEL DE INGRESO
with st.container():
    # Valores por defecto
    def_temp, def_pj, def_g, def_a = "", 0, 0, 0
    
    # Si estamos editando, cargar los datos de la fila seleccionada
    if st.session_state.edit_index is not None:
        idx = st.session_state.edit_index
        e = st.session_state.filas[idx]
        def_temp, def_pj, def_g, def_a = e['TEMP'], e['PJ'], e['GOLES'], e['ASIST']

    c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
    # Importante: el valor 'value' se actualiza con def_X
    t_in = c1.text_input("Temporada / Mes", value=def_temp)
    p_in = c2.number_input("Partidos", min_value=0, value=def_pj)
    g_in = c3.number_input("Goles", min_value=0, value=def_g)
    a_in = c4.number_input("Asistencias", min_value=0, value=def_a)

    b1, b2 = st.columns(2)
    with b1:
        texto_btn = "GUARDAR CAMBIOS" if st.session_state.edit_index is not None else "AGREGAR REGISTRO"
        if st.button(texto_btn):
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
                    st.session_state.edit_index = None # Resetear modo edición
                else:
                    st.session_state.filas.append(nueva_data)
                st.rerun()
    with b2:
        if st.button("LIMPIAR TODO"):
            st.session_state.filas = []
            st.session_state.edit_index = None
            st.rerun()

# 4. RESUMEN DE 5 MÉTRICAS
if st.session_state.filas:
    df = pd.DataFrame(st.session_state.filas)
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1: st.markdown(f'<div class="metric-box">TOTAL PJ<span class="metric-value">{int(df["PJ"].sum())}</span></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-box">TOTAL GOLES<span class="metric-value">{int(df["GOLES"].sum())}</span></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-box">TOTAL ASIST<span class="metric-value">{int(df["ASIST"].sum())}</span></div>', unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="metric-box">TOTAL G/A<span class="metric-value">{int(df["GA"].sum())}</span></div>', unsafe_allow_html=True)
    with m5: st.markdown(f'<div class="metric-box">AVG GLOBAL<span class="metric-value">{df["AVG"].mean():.1f}</span></div>', unsafe_allow_html=True)

st.write("")

# 5. TABLA (FILAS JUNTAS Y MODO EDIT FUNCIONANDO)
if st.session_state.filas:
    # Encabezado
    h = st.columns([1.5, 0.6, 0.6, 0.8, 1, 0.8, 0.6, 0.8, 0.6, 0.6, 0.6])
    labels = ["TEMPORADA", "PJ", "GOLES", "G RATE", "ASISTENCIAS", "A RATE", "G/A", "G/A RATE", "AVG", "", ""]
    for col, label in zip(h, labels):
        if label != "":
            col.markdown(f'<div class="header-cell">{label}</div>', unsafe_allow_html=True)

    # Datos
    for i, f in enumerate(st.session_state.filas):
        # El margen negativo -8px elimina la separación entre filas que pone Streamlit
        st.markdown('<div style="margin-top:-8px;">', unsafe_allow_html=True) 
        r = st.columns([1.5, 0.6, 0.6, 0.8, 1, 0.8, 0.6, 0.8, 0.6, 0.6, 0.6])
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
            # Al presionar EDIT, guardamos el índice y recargamos
            if st.button("EDIT", key=f"edit_{i}"):
                st.session_state.edit_index = i
                st.rerun()
        with r[10]:
            if st.button("DEL", key=f"del_{i}"):
                st.session_state.filas.pop(i)
                if st.session_state.edit_index == i:
                    st.session_state.edit_index = None
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("SISTEMA ONLINE. INGRESE REGISTROS.")
