import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN Y ESTILO (ESTILO EXCEL / DASHBOARD TÉCNICO)
st.set_page_config(page_title="Stats Lab Pro", layout="wide")

st.markdown("""
    <style>
    /* Fondo degradado azul técnico */
    .stApp {
        background: linear-gradient(180deg, #0d1b2a 0%, #1e3a8a 100%);
        background-attachment: fixed;
        color: #ffffff;
    }
    
    .main-title { 
        font-family: 'Arial Black', sans-serif; 
        font-size: 2.8rem; 
        text-transform: uppercase; 
        margin-bottom: 30px;
    }

    /* CORRECCIÓN DEFINITIVA DE BORDES EN INPUTS */
    /* Quitamos cualquier estilo previo de Streamlit que interfiera con el borde inferior */
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    
    .stTextInput div, .stNumberInput div {
        background-color: transparent !important;
        border: none !important;
    }

    /* Marco sólido para los cuadros de entrada */
    .stTextInput input, .stNumberInput input {
        background-color: rgba(0, 0, 0, 0.4) !important;
        border: 2px solid #ffffff !important; /* Borde completo y cerrado */
        color: white !important;
        border-radius: 0px !important;
        height: 45px !important;
        font-weight: 700 !important;
        padding: 10px !important;
    }

    label {
        font-family: 'Verdana', sans-serif !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        font-size: 0.9rem !important;
        margin-bottom: 5px !important;
    }

    /* Botones con estilo de celda */
    .stButton>button {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid #ffffff !important;
        color: white !important;
        border-radius: 0px !important;
        height: 45px !important;
        font-weight: 900 !important;
        text-transform: uppercase;
    }

    .stButton>button:hover {
        background-color: #ffffff !important;
        color: #0d1b2a !important;
    }

    /* ESTILO TABLA EXCEL */
    .excel-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        background-color: rgba(0, 0, 0, 0.3);
    }

    .excel-table th {
        border: 1px solid #ffffff;
        padding: 12px;
        text-align: left;
        background-color: rgba(255, 255, 255, 0.1);
        text-transform: uppercase;
        font-size: 0.85rem;
    }

    .excel-table td {
        border: 1px solid rgba(255, 255, 255, 0.5);
        padding: 10px;
        font-size: 0.9rem;
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
    def_temp, def_pj, def_g, def_a = ("", 1, 0, 0)
    if st.session_state.edit_index is not None:
        e = st.session_state.filas[st.session_state.edit_index]
        def_temp, def_pj, def_g, def_a = e['TEMP'], e['PJ'], e['GOLES'], e['ASIST']

    c1, c2, c3, c4 = st.columns([2.5, 1, 1, 1])
    with c1: t_in = st.text_input("Temporada / Mes", value=def_temp)
    with c2: p_in = st.number_input("Partidos", min_value=1, value=def_pj)
    with c3: g_in = st.number_input("Goles", min_value=0, value=def_g)
    with c4: a_in = st.number_input("Asistencias", min_value=0, value=def_a)

    ca, cb = st.columns([1, 1])
    with ca:
        label_btn = "GUARDAR CAMBIOS" if st.session_state.edit_index is not None else "AGREGAR REGISTRO"
        if st.button(label_btn):
            ga = g_in + a_in
            gar = round(ga/p_in, 2)
            avg = 10.0 if gar >= 6 else (0.0 if gar <= 0 else round((gar * 10) / 6, 1))
            
            nueva_data = {
                "TEMP": t_in, "PJ": p_in, "GOLES": g_in, "G_RATE": round(g_in/p_in, 2),
                "ASIST": a_in, "A_RATE": round(a_in/p_in, 2), "GA": ga, "GA_RATE": gar, "AVG": avg
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

st.divider()

# 4. TABLA TIPO EXCEL
if st.session_state.filas:
    # Construcción de la tabla mediante HTML para control total de bordes
    tabla_html = """
    <table class="excel-table">
        <tr>
            <th>Temporada</th>
            <th>PJ</th>
            <th>Goles</th>
            <th>G Rate</th>
            <th>Asistencias</th>
            <th>A Rate</th>
            <th>G/A</th>
            <th>G/A Rate</th>
            <th>AVG</th>
            <th>Acciones</th>
        </tr>
    """
    
    st.markdown(tabla_html, unsafe_allow_html=True)

    for i, f in enumerate(st.session_state.filas):
        col_data = st.columns([1.5, 0.6, 0.6, 0.8, 1, 0.8, 0.6, 0.8, 0.6, 0.8, 0.8])
        col_data[0].write(f['TEMP'])
        col_data[1].write(f['PJ'])
        col_data[2].write(f['GOLES'])
        col_data[3].write(f"{f['G_RATE']:.2f}")
        col_data[4].write(f['ASIST'])
        col_data[5].write(f"{f['A_RATE']:.2f}")
        col_data[6].write(f['GA'])
        col_data[7].write(f"{f['GA_RATE']:.2f}")
        col_data[8].write(f"{f['AVG']:.1f}")
        
        if col_data[9].button("EDIT", key=f"e_{i}"):
            st.session_state.edit_index = i
            st.rerun()
        if col_data[10].button("DEL", key=f"d_{i}"):
            st.session_state.filas.pop(i)
            st.rerun()
    
    # Resumen inferior
    st.write("")
    df = pd.DataFrame(st.session_state.filas)
    m1, m2, m3 = st.columns(3)
    m1.metric("TOTAL PJ", df["PJ"].sum())
    m2.metric("TOTAL GOLES", df["GOLES"].sum())
    m3.metric("AVG GLOBAL", f"{df['AVG'].mean():.1f}")
else:
    st.info("SISTEMA ONLINE. INGRESE DATOS.")
