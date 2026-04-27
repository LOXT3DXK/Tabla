import streamlit as st
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Performance Tracker", layout="wide")

# Estilos personalizados para el look que buscas
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, #001f3f, #000000);
        color: white;
    }
    h1 {
        color: #ffffff;
        text-shadow: 2px 2px #007bff;
        font-family: 'Courier New', Courier, monospace;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Performance Statistics")

# 1. Inicializar el estado de la tabla si no existe
if 'df_stats' not in st.session_state:
    # Creamos la fila inicial por defecto
    data = {
        "Mes o Temporada": ["Temporada 1"],
        "PJ": [0],
        "Goles": [0],
        "Asistencias": [0],
        "G Rate": [0.0],
        "A Rate": [0.0],
        "G/A": [0],
        "G/A Rate": [0.0],
        "AVG": [0.0]
    }
    st.session_state.df_stats = pd.DataFrame(data)

# 2. Función para realizar los cálculos automáticos
def calcular_metricas(df):
    # Asegurar que PJ no sea 0 para evitar error de división
    pj_safe = df['PJ'].replace(0, 1)
    
    df['G Rate'] = (df['Goles'] / pj_safe).round(2)
    df['A Rate'] = (df['Asistencias'] / pj_safe).round(2)
    df['G/A'] = df['Goles'] + df['Asistencias']
    df['G/A Rate'] = (df['G/A'] / pj_safe).round(2)
    
    # Lógica del AVG (Escala 0-10)
    # 0 G/A Rate = 0 AVG
    # 6+ G/A Rate = 10 AVG
    # Entre 0.1 y 5.9 es proporcional
    def calcular_avg(rate):
        if rate >= 6:
            return 10.0
        elif rate <= 0:
            return 0.0
        else:
            # Mapeo lineal de 0-6 a 0-10
            return round((rate * 10) / 6, 1)
            
    df['AVG'] = df['G/A Rate'].apply(calcular_avg)
    return df

# 3. Interfaz de la Tabla
st.subheader("Registro de Actividad")
st.info("Puedes editar las celdas de Mes, PJ, Goles y Asistencias. El resto se calcula solo.")

# El editor de datos
edited_df = st.data_editor(
    st.session_state.df_stats,
    num_rows="dynamic", # Permite agregar/eliminar filas con el botón (+) abajo
    max_rows=31,        # Encabezado + 30 filas
    column_config={
        "G Rate": st.column_config.NumberColumn(disabled=True),
        "A Rate": st.column_config.NumberColumn(disabled=True),
        "G/A": st.column_config.NumberColumn(disabled=True),
        "G/A Rate": st.column_config.NumberColumn(disabled=True),
        "AVG": st.column_config.NumberColumn(disabled=True, format="%.1f ⭐"),
        "PJ": st.column_config.NumberColumn(min_value=0),
        "Goles": st.column_config.NumberColumn(min_value=0),
        "Asistencias": st.column_config.NumberColumn(min_value=0),
    },
    hide_index=True,
    use_container_width=True,
    key="stats_editor"
)

# 4. Botón para procesar y guardar cambios
if st.button("Actualizar y Calcular Metas"):
    # Aplicamos los cálculos al DataFrame editado
    st.session_state.df_stats = calcular_metricas(edited_df)
    st.rerun()

# 5. Resumen visual (Opcional)
if not st.session_state.df_stats.empty:
    avg_total = st.session_state.df_stats['AVG'].mean()
    st.metric("Promedio de Nota General", f"{avg_total:.1f} / 10")