import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN Y ESTILO TÉCNICO
st.set_page_config(page_title="Stats Lab Pro", layout="wide")

st.markdown("""
    <style>
    /* Fondo degradado azul oscuro */
    .stApp {
        background: linear-gradient(180deg, #0d1b2a 0%, #1b263b 100%);
        background-attachment: fixed;
        color: #e0e1dd;
    }
    
    /* Título limpio sin barras laterales */
    .main-title { 
        font-family: 'Arial Black', sans-serif; 
        font-size: 2.8rem; 
        text-transform: uppercase; 
        line-height: 1; 
        margin-bottom: 30px;
        color: #ffffff;
    }

    /* CORRECCIÓN DE BORDES EN CUADROS RELLENABLES */
    /* Forzamos el borde en el contenedor y el input para que no desaparezca */
    .stNumberInput div, .stTextInput div {
        border-radius: 0px !important;
    }

    .stNumberInput div div input, .stTextInput div div input {
        background-color: rgba(13, 27, 42, 0.9) !important;
        border: 2px solid #ffffff !important; /* Borde blanco sólido constante */
        color: #ffffff !important;
        border-radius: 0px !important;
        height: 48px !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        padding-left: 15px !important;
    }

    /* Quitar el borde azul por defecto de Streamlit al hacer foco */
    .stNumberInput div div input:focus, .stTextInput div div input:focus {
        border-color: #4facfe !important;
        box-shadow: none !important;
    }

    /* Etiquetas de los campos */
    label {
        color: #ffffff !important;
        font-family: 'Verdana', sans-serif !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px !important;
    }

    /* Botones de acción unificados */
    .stButton>button {
        background-color: transparent !important;
        border: 2px solid #ffffff !important;
        color: #ffffff !important;
        border-radius: 0px !important;
        height: 48px !important;
        width: 100%;
        font-weight: 900 !important;
        text-transform: uppercase;
        transition: 0.3s;
        margin-top: 5px;
    }

    .stButton>button:hover {
        background-color: #ffffff !important;
        color: #0d1b2a !important;
    }

    /* Estilo de la cabecera de la tabla */
    .header-row {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 12px;
        border-top: 2px solid #ffffff;
        border-bottom: 2px solid #ffffff;
        font-weight: 900;
        text-transform: uppercase;
        margin-top: 20px;
    }

    /* Estilo de las filas de datos */
    .data-row {
        padding: 10px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">STATS LAB<br>PERFORMANCE TRACKER</h1>', unsafe_allow_html=True)

# 2. GESTIÓN DE DATOS
if 'filas' not in st.session_state:
    st.session_state.filas = []
if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

# 3. PANEL DE INGRESO (CUADROS RELLENABLES)
with st.container():
    # Valores para edición
    def_temp, def_pj, def_g, def_a = ("", 1, 0, 0)
    if st.session_state.edit_index is not None:
        e = st.session_state.filas[st.session_state.edit_index]
        def_temp, def_pj, def_g, def_a = e['TEMP'], e['PJ'], e['GOLES'], e['ASIST']

    c1, c2, c3, c4 = st.columns([2.5, 1, 1, 1])
    with c1: temp_in = st.text_input("Temporada / Mes", value=def_temp)
    with c2: pj_in = st.number_input("Partidos", min_value=1, value=def_pj)
    with c3: g_in = st.number_input("Goles", min_value=0, value=def_g)
    with c4: a_in = st.number_input("Asistencias", min_value=0, value=def_a)

    # Fila de botones de control
    ca, cb = st.columns([1, 1])
    with ca:
        if st.session_state.edit_index is None:
            if st.button("AGREGAR REGISTRO"):
                ga = g_in + a_in
                gar = round(ga/pj_in, 2)
                avg = 10.0 if gar >= 6 else (0.0 if gar <= 0 else round((gar * 10) / 6, 1))
                st.session_state.filas.append({
                    "TEMP": temp_in, "PJ": pj_in, "GOLES": g_in, "G_RATE": round(g_in/pj_in, 2),
                    "ASIST": a_in, "A_RATE": round(a_in/pj_in, 2), "GA": ga, "GA_RATE": gar, "AVG": avg
                })
                st.rerun()
        else:
            if st.button("GUARDAR CAMBIOS"):
                ga = g_in + a_in
                gar = round(ga/pj_in, 2)
                avg = 10.0 if gar >= 6 else (0.0 if gar <= 0 else round((gar * 10) / 6, 1))
                st.session_state.filas[st.session_state.edit_index] = {
                    "TEMP": temp_in, "PJ": pj_in, "GOLES": g_in, "G_RATE": round(g_in/pj_in, 2),
                    "ASIST": a_in, "A_RATE": round(a_in/pj_in, 2), "GA": ga, "GA_RATE": gar, "AVG": avg
                }
                st.session_state.edit_index = None
                st.rerun()
    with cb:
        if st.button("LIMPIAR TODO"):
            st.session_state.filas = []
            st.session_state.edit_index = None
            st.rerun()

st.divider()

# 4. LISTADO DE RESULTADOS
if st.session_state.filas:
    # Encabezados
    st.markdown('<div class="header-row">', unsafe_allow_html=True)
    h = st.columns([2, 1, 1, 1, 1, 1, 1, 1, 1, 0.8, 0.8])
    labels = ["Temporada", "PJ", "Goles", "G Rate", "Asistencias", "A Rate", "G/A", "G/A Rate", "AVG", "Editar", "Borrar"]
    for col, text in zip(h, labels):
        col.write(text)
    st.markdown('</div>', unsafe_allow_html=True)

    # Filas de datos
    for i, f in enumerate(st.session_state.filas):
        st.markdown('<div class="data-row">', unsafe_allow_html=True)
        row = st.columns([2, 1, 1, 1, 1, 1, 1, 1, 1, 0.8, 0.8])
        row[0].write(f['TEMP'])
        row[1].write(f['PJ'])
        row[2].write(f['GOLES'])
        row[3].write(f"{f['G_RATE']:.2f}")
        row[4].write(f['ASIST'])
        row[5].write(f"{f['A_RATE']:.2f}")
        row[6].write(f['GA'])
        row[7].write(f"{f['GA_RATE']:.2f}")
        row[8].write(f"{f['AVG']:.1f}")
        
        # Botones de acción sin iconos de texto, solo etiquetas limpias
        if row[9].button("EDIT", key=f"e_{i}"):
            st.session_state.edit_index = i
            st.rerun()
        if row[10].button("DEL", key=f"d_{i}"):
            st.session_state.filas.pop(i)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Resumen Final
    st.write("")
    df = pd.DataFrame(st.session_state.filas)
    m1, m2, m3 = st.columns(3)
    m1.metric("PARTIDOS TOTALES", df["PJ"].sum())
    m2.metric("GOLES TOTALES", df["GOLES"].sum())
    m3.metric("RATING PROMEDIO", f"{df['AVG'].mean():.1f}")
else:
    st.info("SISTEMA ONLINE. INGRESE DATOS.")
