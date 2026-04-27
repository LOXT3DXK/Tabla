import streamlit as st
import pandas as pd

st.set_page_config(page_title="Performance Tracker", layout="wide")

# Estilo visual Cyberpunk/Futbolístico
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #000d1a, #000000); color: white; }
    [data-testid="stMetricValue"] { color: #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Stats Performance App")

# 1. Estructura base de las columnas de entrada
COLUMNAS_INPUT = ["Mes o Temporada", "PJ", "Goles", "Asistencias"]

# 2. Inicializar el estado de los datos de entrada
if 'raw_data' not in st.session_state:
    st.session_state.raw_data = pd.DataFrame([{
        "Mes o Temporada": "Enero",
        "PJ": 0, "Goles": 0, "Asistencias": 0
    }])

# 3. Interfaz de Edición
st.subheader("📝 Entrada de Datos")
st.caption("Añade filas con el botón (+) al final de la tabla. PJ debe ser mayor a 0 para calcular rates.")

# Editor simplificado: Solo lo que el usuario DEBE escribir
input_df = st.data_editor(
    st.session_state.raw_data,
    num_rows="dynamic",
    max_rows=30,
    column_config={
        "Mes o Temporada": st.column_config.TextColumn(required=True),
        "PJ": st.column_config.NumberColumn(min_value=0, default=0),
        "Goles": st.column_config.NumberColumn(min_value=0, default=0),
        "Asistencias": st.column_config.NumberColumn(min_value=0, default=0),
    },
    hide_index=True,
    use_container_width=True,
    key="editor_principal"
)

# 4. Lógica de cálculo (Se ejecuta siempre sobre el input_df)
def procesar_stats(df):
    df_calc = df.copy()
    # Evitar división por cero
    pj_safe = df_calc['PJ'].apply(lambda x: x if x > 0 else 1)
    
    df_calc['G Rate'] = (df_calc['Goles'] / pj_safe).round(2)
    df_calc['A Rate'] = (df_calc['Asistencias'] / pj_safe).round(2)
    df_calc['G/A'] = df_calc['Goles'] + df_calc['Asistencias']
    df_calc['G/A Rate'] = (df_calc['G/A'] / pj_safe).round(2)
    
    def calcular_avg(rate):
        if rate >= 6: return 10.0
        if rate <= 0: return 0.0
        return round((rate * 10) / 6, 1)
    
    df_calc['AVG'] = df_calc['G/A Rate'].apply(calcular_avg)
    
    # Reordenar columnas para que coincida con tu pedido
    columnas_finales = [
        "Mes o Temporada", "PJ", "Goles", "G Rate", 
        "Asistencias", "A Rate", "G/A", "G/A Rate", "AVG"
    ]
    return df_calc[columnas_finales]

# 5. Mostrar Resultados
st.divider()
st.subheader("📈 Tabla de Resultados Reales")

# Procesamos los datos actuales del editor
df_final = procesar_stats(input_df)

# Mostramos la tabla final (estática, no editable para evitar errores)
st.dataframe(
    df_final,
    column_config={
        "AVG": st.column_config.NumberColumn(format="%.1f pts ⭐"),
        "G Rate": st.column_config.NumberColumn(format="%.2f"),
        "A Rate": st.column_config.NumberColumn(format="%.2f"),
        "G/A Rate": st.column_config.NumberColumn(format="%.2f"),
    },
    hide_index=True,
    use_container_width=True
)

# Métricas rápidas
if not df_final.empty:
    c1, c2, c3 = st.columns(3)
    c1.metric("Total PJ", df_final['PJ'].sum())
    c2.metric("Total G/A", df_final['G/A'].sum())
    c3.metric("AVG Promedio", f"{df_final['AVG'].mean():.1f}")
