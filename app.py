import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN Y ESTILO (FONDO DEGRADADO AZUL Y BORDES SÓLIDOS)
st.set_page_config(page_title="Stats Lab", layout="wide")

st.markdown("""
    <style>
    /* Fondo con degradado de azul claro a oscuro */
    .stApp {
        background: linear-gradient(180deg, #1e3a8a 0%, #0f172a 100%);
        background-attachment: fixed;
        color: white;
    }
    
    .main-title { 
        font-family: 'Arial Black', sans-serif; 
        font-size: 2.8rem; 
        text-transform: uppercase; 
        line-height: 1.1; 
        margin-bottom: 25px;
        color: #ffffff;
    }

    /* Estilo para los cuadros de entrada - Bordes blancos sólidos y visibles */
    .stNumberInput div div input, .stTextInput div div input {
        background-color: rgba(0, 0, 0, 0.3) !important;
        border: 2px solid #ffffff !important;
        color: white !important;
        border-radius: 4px !important;
        height: 45px !important;
        font-weight: 700 !important;
    }

    /* Estilo para etiquetas (Labels) */
    .stMarkdown p, label {
        color: #ffffff !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        font-size: 0.85rem !important;
    }

    /* Botones con estilo de cuadro (Borde blanco, fondo translúcido) */
    .stButton>button {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid #ffffff !important;
        color: white !important;
        border-radius: 4px !important;
        height: 45px !important;
        width: 100%;
        font-weight: 900 !important;
        transition: 0.3s;
        text-transform: uppercase;
    }

    .stButton>button:hover {
        background-color: rgba(255, 255, 255, 0.3) !important;
        border-color: #60a5fa !important;
    }

    /* Botón de eliminar (Rojo sutil) */
    .btn-del > div > button {
        border-color: #ef4444 !important;
        color: #ef4444 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">STATS LAB<br>PERFORMANCE TRACKER</h1>', unsafe_allow_html=True)

# 2. GESTIÓN DE DATOS
if 'filas' not in st.session_state:
    st.session_state.filas = []
if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

# 3. ÁREA DE ENTRADA / EDICIÓN
st.subheader("📝 INGRESO DE DATOS" if st.session_state.edit_index is None else "🔄 EDITANDO REGISTRO")

# Valores por defecto si estamos editando
def_temp = ""
def_pj = 1
def_g = 0
def_a = 0

if st.session_state.edit_index is not None:
    edit_data = st.session_state.filas[st.session_state.edit_index]
    def_temp = edit_data['TEMPORADA']
    def_pj = edit_data['PJ']
    def_g = edit_data['GOLES']
    def_a = edit_data['ASIST']

c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 2])

with c1:
    temp_input = st.text_input("MES / TEMPORADA", value=def_temp)
with c2:
    pj_input = st.number_input("PJ", min_value=1, value=def_pj)
with c3:
    goles_input = st.number_input("GOLES", min_value=0, value=def_g)
with c4:
    asist_input = st.number_input("ASIST", min_value=0, value=def_a)

with c5:
    st.write(" ") # Espaciador
    st.write(" ")
    if st.session_state.edit_index is None:
        if st.button("AÑADIR REGISTRO"):
            # Lógica de cálculo
            ga = goles_input + asist_input
            gar = round(ga/pj_input, 2)
            avg = 10.0 if gar >= 6 else (0.0 if gar <= 0 else round((gar * 10) / 6, 1))
            
            st.session_state.filas.append({
                "TEMPORADA": temp_input, "PJ": pj_input, "GOLES": goles_input, 
                "G RATE": round(goles_input/pj_input, 2), "ASIST": asist_input, 
                "A RATE": round(asist_input/pj_input, 2), "G/A": ga, "G/A RATE": gar, "AVG": avg
            })
            st.rerun()
    else:
        col_edit1, col_edit2 = st.columns(2)
        if col_edit1.button("GUARDAR"):
            ga = goles_input + asist_input
            gar = round(ga/pj_input, 2)
            avg = 10.0 if gar >= 6 else (0.0 if gar <= 0 else round((gar * 10) / 6, 1))
            
            st.session_state.filas[st.session_state.edit_index] = {
                "TEMPORADA": temp_input, "PJ": pj_input, "GOLES": goles_input, 
                "G RATE": round(goles_input/pj_input, 2), "ASIST": asist_input, 
                "A RATE": round(asist_input/pj_input, 2), "G/A": ga, "G/A RATE": gar, "AVG": avg
            }
            st.session_state.edit_index = None
            st.rerun()
        if col_edit2.button("CANCELAR"):
            st.session_state.edit_index = None
            st.rerun()

st.divider()

# 4. TABLA DE RESULTADOS CON ACCIONES INDIVIDUALES
if st.session_state.filas:
    # Encabezados de la tabla manual para control total
    h = st.columns([1.5, 0.6, 0.6, 0.8, 0.6, 0.8, 0.6, 0.8, 0.6, 1, 1])
    headers = ["TEMP", "PJ", "G", "G/R", "A", "A/R", "G/A", "G/AR", "AVG", "EDIT", "DEL"]
    for col, text in zip(h, headers):
        col.markdown(f"**{text}**")

    # Filas de datos
    for i, fila in enumerate(st.session_state.filas):
        cols = st.columns([1.5, 0.6, 0.6, 0.8, 0.6, 0.8, 0.6, 0.8, 0.6, 1, 1])
        cols[0].write(fila["TEMPORADA"])
        cols[1].write(fila["PJ"])
        cols[2].write(fila["GOLES"])
        cols[3].write(fila["G RATE"])
        cols[4].write(fila["ASIST"])
        cols[5].write(fila["A RATE"])
        cols[6].write(fila["G/A"])
        cols[7].write(fila["G/A RATE"])
        cols[8].write(fila["AVG"])
        
        # Botones de acción a la derecha
        if cols[9].button("📝", key=f"edit_{i}"):
            st.session_state.edit_index = i
            st.rerun()
        
        if cols[10].button("🗑️", key=f"del_{i}"):
            st.session_state.filas.pop(i)
            st.rerun()

    st.divider()
    if st.button("🗑️ LIMPIAR TODA LA BASE DE DATOS"):
        st.session_state.filas = []
        st.rerun()
else:
    st.info("SISTEMA ONLINE. INGRESA DATOS.")
