import streamlit as st
import pandas as pd

st.set_page_config(page_title="Performance Tracker", layout="wide")

# Estilo visual
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #001f3f, #000000); color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Performance Statistics")

# 1. Función de lógica para los cálculos
def aplicar_calculos(df):
    # Evitar división por cero
    pj = df['PJ'].replace(0, 1)
    
    df['G Rate'] = (df['Goles'] / pj).round(2)
    df['A Rate'] = (df['Asistencias'] / pj).round(2)
    df['G/A'] = df['Goles'] + df['Asistencias']
    df['G/A Rate'] = (df['G/A'] / pj).round(2)
    
    # Lógica de AVG: 0 es 0, 6+ es 10, intermedio es escala
    def calcular_avg(rate):
        if rate >= 6: return 10.0
        if rate <= 0: return 0.0
        return round((rate * 10) / 6, 1)
        
    df['AVG'] = df['G/A Rate'].apply(calcular_avg)
    return df

# 2. Inicializar datos si no existen
if 'datos' not in st.session_state:
    df_init = pd.DataFrame([{
        "Mes o Temporada": "Temp 1",
        "PJ": 0, "Goles": 0, "Asistencias": 0,
        "G Rate": 0.0, "A Rate": 0.0, "G/A": 0, "G/A Rate": 0.0, "AVG": 0.0
    }])
    st.session_state.datos = df_init

# 3. Mostrar el editor
st.subheader("Registro de Actividad")
st.info("Presiona Enter tras editar una celda. Las columnas calculadas se actualizarán al final.")

# Configuramos qué columnas son editables
edited_df = st.data_editor(
    st.session_state.datos,
    num_rows="dynamic",
    max_rows=31,
    column_config={
        "Mes o Temporada": st.column_config.TextColumn("Mes o Temporada", width="medium"),
        "PJ": st.column_config.NumberColumn("PJ", min_value=0, default=0),
        "Goles": st.column_config.NumberColumn("Goles", min_value=0, default=0),
        "Asistencias": st.column_config.NumberColumn("Asistencias", min_value=0, default=0),
        # Deshabilitamos las calculadas
        "G Rate": st.column_config.NumberColumn("G Rate", disabled=True),
        "A Rate": st.column_config.NumberColumn("A Rate", disabled=True),
        "G/A": st.column_config.NumberColumn("G/A", disabled=True),
        "G/A Rate": st.column_config.NumberColumn("G/A Rate", disabled=True),
        "AVG": st.column_config.NumberColumn("AVG", disabled=True, format="%.1f pts")
    },
    hide_index=True,
    use_container_width=True
)

# 4. Botón para procesar
if st.button("Calcular Metas y Guardar"):
    # Aplicamos los cálculos al dataframe que el usuario editó
    resultado = aplicar_calculos(edited_df)
    # Guardamos en el estado y recargamos
    st.session_state.datos = resultado
    st.rerun()

# Resumen rápido
if not st.session_state.datos.empty:
    avg_total = st.session_state.datos['AVG'].mean()
    st.metric("Nota Promedio Global", f"{avg_total:.2f}")
