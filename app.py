import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Stats Lab Performance Tracker", layout="wide")

# CSS para fondo oscuro, degradado y diseño unificado
st.markdown("""
    <style>
    /* Fondo degradado oscuro (Azul Noche a Negro) */
    .stApp {
        background: linear-gradient(180deg, #000814 0%, #001d3d 100%);
        background-attachment: fixed;
        color: #ffffff;
    }
    
    /* Título imponente pero equilibrado */
    .main-title {
        font-family: 'Arial Black', sans-serif;
        font-size: 2.8rem;
        letter-spacing: -1.5px;
        text-transform: uppercase;
        color: #ffffff;
        text-align: left;
        margin-bottom: 5px;
    }

    /* Fuentes robustas y sólidas */
    h2, h3, p, span, label {
        font-family: 'Verdana', sans-serif !important;
        font-weight: 700 !important;
        color: #ffffff !important;
    }

    /* Estilo para los inputs para que no desentonen */
    .stNumberInput input, .stTextInput input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid #ffffff !important;
        color: white !important;
        border-radius: 0px !important;
    }

    /* Botones sólidos que encajan con la interfaz */
    .stButton>button {
        width: 100%;
        background-color: #ffffff;
        color: #000814;
        font-weight: 900;
        text-transform: uppercase;
        border-radius: 0px;
        border: 2px solid #ffffff;
        height: 45px;
        margin-top: 24px; /* Alineación con los inputs */
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #4facfe;
        color: #ffffff;
        border-color: #4facfe;
    }

    /* Estilo de la tabla */
    [data-testid="stDataFrame"] {
        border: 2px solid #ffffff;
        background-color: rgba(0, 0, 0, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# Título de la App
st.markdown('<h1 class="main-title">STATS LAB<br>PERFORMANCE TRACKER</h1>', unsafe_allow_html=True)
st.divider()

# Inicializar estado de la sesión
if 'filas' not in st.session_state:
    st.session_state.filas = []

# --- FILA DE ENTRADA Y ACCIONES ---
# Usamos una sola fila para que todo se vea como una misma herramienta
c1, c2, c3, c4, c5, c6 = st.columns([2, 1, 1, 1, 1.5, 1.5])

with c1:
    temp = st.text_input("TEMPORADA", placeholder="EJ: ABRIL")
with c2:
    pj = st.number_input("PJ", min_value=1, step=1, value=1)
with c3:
    goles = st.number_input("G", min_value=0, step=1, value=0)
with c4:
    asist = st.number_input("A", min_value=0, step=1, value=0)
with c5:
    # Botón Añadir integrado
    btn_add = st.button("AÑADIR")
with c6:
    # Botón Borrar integrado
    btn_clear = st.button("BORRAR TODO")

# Lógica del botón Añadir
if btn_add:
    g_rate = round(goles / pj, 2)
    a_rate = round(asist / pj, 2)
    ga_total = goles + asist
    ga_rate = round(ga_total / pj, 2)
    
    # Lógica AVG (0-10)
    if ga_rate >= 6:
        avg = 10.0
    elif ga_rate <= 0:
        avg = 0.0
    else:
        avg = round((ga_rate * 10) / 6, 1)

    st.session_state.filas.append({
        "TEMPORADA": temp,
        "PJ": pj,
        "G": goles,
        "G RATE": g_rate,
        "A": asist,
        "A RATE": a_rate,
        "G/A": ga_total,
        "G/A RATE": ga_rate,
        "AVG": avg
    })
    st.rerun()

# Lógica del botón Borrar
if btn_clear:
    st.session_state.filas = []
    st.rerun()

st.divider()

# --- MOSTRAR RESULTADOS ---
if st.session_state.filas:
    df = pd.DataFrame(st.session_state.filas)
    
    # Métricas de resumen rápidas
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("TOTAL PARTIDOS", df["PJ"].sum())
    col_m2.metric("TOTAL GOLES", df["G"].sum())
    col_m3.metric("PROMEDIO AVG", f"{round(df['AVG'].mean(), 1)}")

    # Tabla de datos
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
else:
    st.write("SISTEMA LISTO: INGRESA DATOS PARA COMENZAR.")
