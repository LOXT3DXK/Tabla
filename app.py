import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN Y ESTILO UNIFICADO
st.set_page_config(page_title="Stats Lab", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(180deg, #000814 0%, #001d3d 100%); background-attachment: fixed; color: white; }
    
    .main-title { 
        font-family: 'Arial Black', sans-serif; 
        font-size: 2.5rem; 
        text-transform: uppercase; 
        line-height: 1; 
        margin-bottom: 20px; 
    }

    /* ESTILO UNIFICADO: Borde blanco, fondo oscuro para Inputs y Botones */
    .stNumberInput input, .stTextInput input, .stButton>button {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid #ffffff !important;
        color: white !important;
        border-radius: 0px !important;
        height: 45px !important;
        font-family: 'Verdana', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase;
    }

    .stButton>button {
        margin-top: 28px;
        transition: 0.3s ease;
    }

    .stButton>button:hover {
        background-color: rgba(255, 255, 255, 0.2) !important;
        border-color: #4facfe !important;
    }

    /* Tabla */
    [data-testid="stDataFrame"] {
        border: 2px solid #ffffff;
        background-color: rgba(0, 0, 0, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">STATS LAB<br>PERFORMANCE TRACKER</h1>', unsafe_allow_html=True)

# 2. INICIALIZACIÓN DE DATOS (Lista de diccionarios es más estable para el estado)
if 'filas_list' not in st.session_state:
    st.session_state.filas_list = []

# 3. FILA DE ENTRADA
c1, c2, c3, c4, c5, c6 = st.columns([2, 1, 1, 1, 1.5, 1.5])

with c1:
    temp_val = st.text_input("TEMPORADA", placeholder="ABRIL")
with c2:
    pj_val = st.number_input("PJ", min_value=1, value=1)
with c3:
    goles_val = st.number_input("GOLES", min_value=0, value=0)
with c4:
    asist_val = st.number_input("ASIST", min_value=0, value=0)

with c5:
    if st.button("AÑADIR"):
        ga_total = goles_val + asist_val
        ga_rate = round(ga_total / pj_val, 2)
        avg = 10.0 if ga_rate >= 6 else (0.0 if ga_rate <= 0 else round((ga_rate * 10) / 6, 1))
        
        st.session_state.filas_list.append({
            "TEMPORADA": temp_val, "PJ": pj_val, "GOLES": goles_val, 
            "G RATE": round(goles_val / pj_val, 2), "ASIST": asist_val, 
            "A RATE": round(asist_val / pj_val, 2), "G/A": ga_total, 
            "G/A RATE": ga_rate, "AVG": avg
        })
        st.rerun()

with c6:
    if st.button("LIMPIAR TODO"):
        st.session_state.filas_list = []
        st.rerun()

st.divider()

# 4. TABLA INTERACTIVA
if len(st.session_state.filas_list) > 0:
    df_actual = pd.DataFrame(st.session_state.filas_list)
    
    st.subheader("📊 REGISTRO (EDICIÓN Y BORRADO ACTIVADO)")
    
    # Data editor para borrar/editar
    edited_df = st.data_editor(
        df_actual,
        use_container_width=True,
        hide_index=False,
        num_rows="dynamic",
        column_config={
            "G RATE": st.column_config.NumberColumn(disabled=True),
            "A RATE": st.column_config.NumberColumn(disabled=True),
            "G/A": st.column_config.NumberColumn(disabled=True),
            "G/A RATE": st.column_config.NumberColumn(disabled=True),
            "AVG": st.column_config.NumberColumn(disabled=True),
        }
    )

    # Si hay cambios en la tabla (edición o borrado individual)
    if not edited_df.equals(df_actual):
        # Recalcular métricas de las filas editadas
        pj_s = edited_df["PJ"].replace(0, 1)
        edited_df["G RATE"] = (edited_df["GOLES"] / pj_s).round(2)
        edited_df["A RATE"] = (edited_df["ASIST"] / pj_s).round(2)
        edited_df["G/A"] = edited_df["GOLES"] + edited_df["ASIST"]
        edited_df["G/A RATE"] = (edited_df["G/A"] / pj_s).round(2)
        edited_df["AVG"] = edited_df["G/A RATE"].apply(lambda r: 10.0 if r >= 6 else (0.0 if r <= 0 else round((r * 10) / 6, 1)))
        
        st.session_state.filas_list = edited_df.to_dict('records')
        st.rerun()

    # Métricas Globales
    m1, m2, m3 = st.columns(3)
    m1.metric("TOTAL PJ", int(df_actual["PJ"].sum()))
    m2.metric("TOTAL GOLES", int(df_actual["GOLES"].sum()))
    m3.metric("AVG GLOBAL", round(df_actual["AVG"].mean(), 1))
else:
    st.info("SISTEMA ONLINE. INGRESA DATOS.")
