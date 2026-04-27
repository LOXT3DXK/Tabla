import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Performance Stats Lab", layout="wide")

# CSS para fondo degradado y tipografía robusta
st.markdown("""
    <style>
    /* Fondo con degradado de celeste a azul marino */
    .stApp {
        background: linear-gradient(135deg, #4facfe 0%, #003366 100%);
        background-attachment: fixed;
        color: #ffffff;
    }
    
    /* Título imponente */
    .main-title {
        font-family: 'Arial Black', Gadget, sans-serif;
        font-size: 3rem;
        letter-spacing: -2px;
        text-transform: uppercase;
        color: #ffffff;
        margin-bottom: 0px;
        line-height: 1;
    }

    /* Fuentes robustas para el resto de la app */
    h2, h3, p, span, label {
        font-family: 'Verdana', Geneva, sans-serif !important;
        font-weight: 700 !important;
    }

    /* Estilo para los cuadros de entrada de datos */
    .stNumberInput, .stTextInput {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        border: 2px solid #ffffff;
    }

    /* Botón sólido y robusto */
    .stButton>button {
        width: 100%;
        background-color: #ffffff;
        color: #003366;
        font-weight: 900;
        font-size: 1.1rem;
        border-radius: 0px;
        border: none;
        padding: 15px;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #4facfe;
        color: #ffffff;
    }

    /* Estilo de la tabla de resultados */
    [data-testid="stDataFrame"] {
        background-color: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Título Imponente
st.markdown('<h1 class="main-title">PERFORMANCE<br>STATS TRACKER</h1>', unsafe_allow_html=True)
st.divider()

# Inicializar estado
if 'filas' not in st.session_state:
    st.session_state.filas = []

# Formulario de entrada de datos
st.subheader("📥 DATA ENTRY")
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        temp = st.text_input("MES O TEMPORADA", placeholder="EJ: TEMP 2026")
    with col2:
        pj = st.number_input("PJ", min_value=1, step=1, value=1)
    with col3:
        goles = st.number_input("GOLES", min_value=0, step=1, value=0)
    with col4:
        asist = st.number_input("ASISTENCIAS", min_value=0, step=1, value=0)

    if st.button("REGISTRAR DATOS"):
        # Cálculos con redondeo
        g_rate = round(goles / pj, 2)
        a_rate = round(asist / pj, 2)
        ga_total = goles + asist
        ga_rate = round(ga_total / pj, 2)
        
        # Lógica de AVG (Escala 0-10 basada en GA Rate de 6)
        if ga_rate >= 6:
            avg = 10.0
        elif ga_rate <= 0:
            avg = 0.0
        else:
            avg = round((ga_rate * 10) / 6, 1)

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

st.divider()

# Visualización de Resultados
if st.session_state.filas:
    df = pd.DataFrame(st.session_state.filas)
    
    # Métricas de Resumen
    m1, m2, m3 = st.columns(3)
    m1.metric("TOTAL PARTIDOS", df["PJ"].sum())
    m2.metric("TOTAL G/A", df["G/A"].sum())
    m3.metric("AVG PROMEDIO", f"{round(df['AVG'].mean(), 1)}")

    st.subheader("📊 RESULTADOS")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    if st.button("LIMPIAR REGISTROS"):
        st.session_state.filas = []
        st.rerun()
else:
    st.write("NO HAY DATOS REGISTRADOS EN LA SESIÓN ACTUAL.")
