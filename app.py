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

    /* ESTILO UNIFICADO PARA INPUTS Y BOTONES: Borde blanco, fondo oscuro */
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

    /* Alineación del botón con los inputs */
    .stButton>button {
        margin-top: 28px;
        transition: 0.3s ease;
    }

    /* Efecto Hover para los botones */
    .stButton>button:hover {
        background-color: rgba(255, 255, 255, 0.3) !important;
        border-color: #4facfe !important;
    }

    /* Estilo del Editor de Datos */
    [data-testid="stDataFrame"] {
        border: 2px solid #ffffff;
        background-color: rgba(0, 0, 0, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">STATS LAB<br>PERFORMANCE TRACKER</h1>', unsafe_allow_html=True)

# 2. INICIALIZACIÓN DE DATOS
if 'filas' not in st.session_state:
    st.session_state.filas = pd.DataFrame(columns=[
        "TEMPORADA", "PJ", "GOLES", "G RATE", "ASIST", "A RATE", "G/A", "G/A RATE", "AVG"
    ])

# 3. FILA DE ENTRADA (CABECERA)
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
        # Lógica AVG
        if ga_rate >= 6: avg = 10.0
        elif ga_rate <= 0: avg = 0.0
        else: avg = round((ga_rate * 10) / 6, 1)

        nueva_fila = pd.DataFrame([{
            "TEMPORADA": temp_val,
            "PJ": pj_val,
            "GOLES": goles_val,
            "G RATE": round(goles_val / pj_val, 2),
            "ASIST": asist_val,
            "A RATE": round(asist_val / pj_val, 2),
            "G/A": ga_total,
            "G/A RATE": ga_rate,
            "AVG": avg
        }])
        st.session_state.filas = pd.concat([st.session_state.filas, nueva_fila], ignore_index=True)
        st.rerun()

with c6:
    if st.button("LIMPIAR TODO"):
        st.session_state.filas = st.session_state.filas.iloc[0:0]
        st.rerun()

st.divider()

# 4. TABLA INTERACTIVA (EDITAR Y BORRAR FILAS INDIVIDUALES)
if not st.session_state.filas.empty:
    st.subheader("📊 REGISTRO (EDICIÓN DIRECTA ACTIVADA)")
    st.caption("Puedes editar cualquier dato directamente en la tabla o seleccionar una fila y pulsar 'Suprimir' para borrarla.")
    
    # El Data Editor permite editar celdas y borrar filas
    # Las columnas calculadas se deshabilitan para que no se rompan las fórmulas
    edited_df = st.data_editor(
        st.session_state.filas,
        use_container_width=True,
        hide_index=False, # Índice útil para identificar filas
        num_rows="dynamic", # Permite borrar filas seleccionándolas
        column_config={
            "G RATE": st.column_config.NumberColumn(disabled=True),
            "A RATE": st.column_config.NumberColumn(disabled=True),
            "G/A": st.column_config.NumberColumn(disabled=True),
            "G/A RATE": st.column_config.NumberColumn(disabled=True),
            "AVG": st.column_config.NumberColumn(disabled=True),
        }
    )
    
    # Guardar cambios automáticamente si el usuario edita PJ, G o A
    if not edited_df.equals(st.session_state.filas):
        # Recalcular las columnas automáticas tras la edición manual
        pj_s = edited_df["PJ"].replace(0, 1)
        edited_df["G RATE"] = (edited_df["GOLES"] / pj_s).round(2)
        edited_df["A RATE"] = (edited_df["ASIST"] / pj_s).round(2)
        edited_df["G/A"] = edited_df["GOLES"] + edited_df["ASIST"]
        edited_df["G/A RATE"] = (edited_df["G/A"] / pj_s).round(2)
        
        def recalc_avg(r):
            if r >= 6: return 10.0
            if r <= 0: return 0.0
            return round((r * 10) / 6, 1)
        
        edited_df["AVG"] = edited_df["G/A RATE"].apply(recalc_avg)
        
        st.session_state.filas = edited_df
        st.rerun()

    # Métricas Globales
    m1, m2, m3 = st.columns(3)
    m1.metric("TOTAL PJ", int(st.session_state.filas["PJ"].sum()))
    m2.metric("TOTAL GOLES", int(st.session_state.filas["GOLES"].sum()))
    m3.metric("AVG GLOBAL", round(st.session_state.filas["AVG"].mean(), 1))

else:
    st.info("SISTEMA LISTO. INGRESA DATOS ARRIBA.")
