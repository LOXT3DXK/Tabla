import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Stats Lab Pro", layout="wide")

# CSS para Interfaz Futurista / Neón Opaco
st.markdown("""
    <style>
    /* Fondo general oscuro */
    .stApp {
        background-color: #050b14;
        color: #e0e0e0;
    }
    
    /* Títulos con brillo neón sutil */
    h1, h2, h3 {
        color: #00d4ff;
        text-shadow: 0px 0px 10px rgba(0, 212, 255, 0.3);
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* Estilo para los cuadros de métricas */
    [data-testid="stMetricValue"] {
        color: #00ffc3 !important;
        font-family: 'Courier New', monospace;
    }

    /* Botones con estilo futurista */
    .stButton>button {
        width: 100%;
        background-color: #0a192f;
        color: #00d4ff;
        border: 1px solid #00d4ff;
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #00d4ff;
        color: #050b14;
        box-shadow: 0px 0px 15px rgba(0, 212, 255, 0.5);
    }

    /* Estilo de la tabla */
    .stTable {
        border: 1px solid #1f2937;
        background-color: #0f172a;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📂 STATS LAB: PERFORMANCE TRACKER")

# Inicializar estado
if 'filas' not in st.session_state:
    st.session_state.filas = []

# Formulario de entrada de datos (Data Entry)
with st.container():
    st.subheader("🛠 Data Entry")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        temp = st.text_input("Mes / Temporada", placeholder="Ej: Marzo 2026")
    with col2:
        pj = st.number_input("PJ (Partidos)", min_value=1, step=1, value=1)
    with col3:
        goles = st.number_input("Goles", min_value=0, step=1, value=0)
    with col4:
        asist = st.number_input("Asistencias", min_value=0, step=1, value=0)

    if st.button("REGISTRAR ENTRADA"):
        # Cálculos con redondeo aplicado
        g_rate = round(goles / pj, 2)
        a_rate = round(asist / pj, 2)
        ga_total = goles + asist
        ga_rate = round(ga_total / pj, 2)
        
        # Lógica de AVG (0 a 10)
        if ga_rate >= 6:
            avg = 10.0
        elif ga_rate <= 0:
            avg = 0.0
        else:
            avg = round((ga_rate * 10) / 6, 1)

        st.session_state.filas.append({
            "Mes/Temp": temp,
            "PJ": pj,
            "Goles": goles,
            "G Rate": g_rate,
            "Asist": asist,
            "A Rate": a_rate,
            "G/A": ga_total,
            "G/A Rate": ga_rate,
            "AVG": avg
        })
        st.success("Dato procesado en el sistema.")

st.divider()

# Visualización de Resultados
if st.session_state.filas:
    df = pd.DataFrame(st.session_state.filas)
    
    # Métricas de Resumen arriba de la tabla
    m1, m2, m3 = st.columns(3)
    m1.metric("TOTAL PJ", df["PJ"].sum())
    m2.metric("TOTAL G/A", df["G/A"].sum())
    m3.metric("AVG GLOBAL", f"{round(df['AVG'].mean(), 1)}")

    st.subheader("📊 Database")
    # Mostramos la tabla (usamos st.dataframe para que se vea más moderna)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    if st.button("RESETEAR BASE DE DATOS"):
        st.session_state.filas = []
        st.rerun()
else:
    st.info("Esperando ingreso de datos para generar reporte...")
