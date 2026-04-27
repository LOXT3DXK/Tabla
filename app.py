import streamlit as st
import pandas as pd

# Configuración de la página - compacta
st.set_page_config(page_title="Stats Lab", layout="wide")

# CSS para fondo oscuro, degradado y diseño compacto
st.markdown("""
    <style>
    /* Fondo degradado más oscuro (Azul Noche a Negro) */
    .stApp {
        background: linear-gradient(180deg, #001529 0%, #000000 100%);
        background-attachment: fixed;
        color: #ffffff;
    }
    
    /* Título imponente pero más pequeño para ahorrar espacio */
    .main-title {
        font-family: 'Arial Black', sans-serif;
        font-size: 2.2rem;
        letter-spacing: -1px;
        text-transform: uppercase;
        color: #ffffff;
        margin-bottom: -10px;
    }

    /* Reducción de espacios (Padding) generales */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
    }

    /* Fuentes robustas y sólidas */
    h2, h3, p, span, label {
        font-family: 'Verdana', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
    }

    /* Input compactos */
    .stNumberInput, .stTextInput {
        margin-bottom: -15px;
    }

    /* Botón sólido */
    .stButton>button {
        background-color: #ffffff;
        color: #001529;
        font-weight: 900;
        border-radius: 2px;
        border: none;
        padding: 5px;
        height: 40px;
    }
    
    .stButton>button:hover {
        background-color: #4facfe;
        color: #ffffff;
    }

    /* Tabla compacta */
    [data-testid="stDataFrame"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Título
st.markdown('<h1 class="main-title">PERFORMANCE TRACKER</h1>', unsafe_allow_html=True)
st.divider()

# Inicializar estado
if 'filas' not in st.session_state:
    st.session_state.filas = []

# Sección de Entrada - Layout más apretado
with st.container():
    c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 1.5])
    
    with c1:
        temp = st.text_input("MES/TEMP", placeholder="EJ: ABRIL")
    with c2:
        pj = st.number_input("PJ", min_value=1, step=1, value=1)
    with c3:
        goles = st.number_input("G", min_value=0, step=1, value=0)
    with c4:
        asist = st.number_input("A", min_value=0, step=1, value=0)
    with c5:
        st.write(" ") # Espaciador para alinear botón
        st.write(" ") 
        btn_add = st.button("AÑADIR STATS")

    if btn_add:
        # Cálculos redondeados
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

# Resumen y Tabla en una vista compacta
if st.session_state.filas:
    df = pd.DataFrame(st.session_state.filas)
    
    # Métricas pequeñas
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("TOTAL PJ", df["PJ"].sum())
    m2.metric("TOTAL G/A", df["G/A"].sum())
    m3.metric("AVG GLOBAL", f"{round(df['AVG'].mean(), 1)}")
    if m4.button("LIMPIAR TODO"):
        st.session_state.filas = []
        st.rerun()

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=300 # Altura fija para evitar scroll infinito
    )
else:
    st.caption("Esperando datos...")
