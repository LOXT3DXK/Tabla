import streamlit as st
import pandas as pd

st.set_page_config(page_title="Stats Tracker", layout="wide")

# Título con estilo
st.title("📊 Control de Estadísticas")

# 1. Inicializar la lista de datos en el estado de la sesión
if 'filas' not in st.session_state:
    st.session_state.filas = []

# 2. Formulario de entrada (Más estable que el data_editor directo)
with st.expander("➕ Añadir Nueva Entrada", expanded=True):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        temp = st.text_input("Mes o Temporada", placeholder="Enero")
    with col2:
        pj = st.number_input("PJ", min_value=1, step=1, value=1)
    with col3:
        goles = st.number_input("Goles", min_value=0, step=1, value=0)
    with col4:
        asist = st.number_input("Asistencias", min_value=0, step=1, value=0)
    
    if st.button("Agregar a la Tabla"):
        # Lógica de cálculos al momento de insertar
        g_rate = round(goles / pj, 2)
        a_rate = round(asist / pj, 2)
        ga = goles + asist
        ga_rate = round(ga / pj, 2)
        
        # Lógica de tu AVG (Escala 0-10 basada en GA Rate de 6)
        if ga_rate >= 6:
            avg = 10.0
        elif ga_rate <= 0:
            avg = 0.0
        else:
            avg = round((ga_rate * 10) / 6, 1)

        nueva_fila = {
            "Mes o Temporada": temp,
            "PJ": pj,
            "Goles": goles,
            "G Rate": g_rate,
            "Asistencias": asist,
            "A Rate": a_rate,
            "G/A": ga,
            "G/A Rate": ga_rate,
            "AVG": avg
        }
        st.session_state.filas.append(nueva_fila)
        st.success("¡Fila agregada!")

# 3. Mostrar la tabla de resultados
if st.session_state.filas:
    df = pd.DataFrame(st.session_state.filas)
    
    st.subheader("📈 Tus Estadísticas")
    st.table(df) # st.table es la opción más estable contra errores de servidor

    if st.button("Limpiar Tabla"):
        st.session_state.filas = []
        st.rerun()
else:
    st.info("Aún no hay datos. Usa el formulario de arriba para empezar.")
