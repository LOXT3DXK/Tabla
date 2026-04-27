import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN Y ESTILO AGRESIVO PARA SIMETRÍA
st.set_page_config(page_title="Stats Lab Pro", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #050a14 0%, #0d1b2a 40%, #1e3a8a 80%, #3b82f6 100%);
        background-attachment: fixed;
    }
    
    /* Contenedor maestro para las filas añadidas */
    .data-rows-container {
        display: flex;
        flex-direction: column;
        gap: 2px !important; /* SEPARACIÓN EXACTA E IGUAL PARA TODAS LAS FILAS */
    }

    .table-cell {
        border: 1px solid #ffffff;
        background-color: #0b1221;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        width: 100%;
    }

    .header-cell {
        border: 1px solid #ffffff;
        background-color: #1a2639;
        font-weight: 900;
        text-transform: uppercase;
        font-size: 0.7rem;
        height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 2px;
    }

    /* Forzar a los botones a ignorar márgenes internos de Streamlit */
    div[data-testid="column"] {
        padding: 0px !important;
        margin: 0px !important;
    }
    
    .stButton > button {
        border-radius: 0px !important;
        height: 40px !important;
        width: 100% !important;
        margin: 0px !important;
        padding: 0px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ... (Lógica de datos y panel de ingreso igual a la anterior) ...
if 'filas' not in st.session_state: st.session_state.filas = []
if 'edit_index' not in st.session_state: st.session_state.edit_index = None

# PANEL DE INGRESO (Resumido para el ejemplo)
with st.container():
    c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
    # ... inputs aquí ...
    if st.button("GUARDAR / AGREGAR"):
        # ... lógica de guardado ...
        st.rerun()

st.write("")

# 5. TABLA CON SEPARACIÓN MATEMÁTICAMENTE IDÉNTICA
if st.session_state.filas:
    anchos = [1.5, 0.6, 0.6, 0.8, 1, 0.8, 0.6, 0.8, 0.6, 0.6, 0.6]
    
    # Encabezado (mantiene su propio espacio)
    h = st.columns(anchos)
    for col, txt in zip(h, ["TEMPORADA", "PJ", "GOLES", "G RATE", "ASISTENCIAS", "A RATE", "G/A", "G/A RATE", "AVG", "", ""]):
        if txt: col.markdown(f'<div class="header-cell">{txt}</div>', unsafe_allow_html=True)

    # ABRIMOS CONTENEDOR DE FILAS
    st.markdown('<div class="data-rows-container">', unsafe_allow_html=True)
    
    for i, f in enumerate(st.session_state.filas):
        # Usamos un div con margen negativo para anular el salto de línea de Streamlit
        # y que el 'gap' del CSS tome el control total
        st.markdown('<div style="margin-top: -15px;">', unsafe_allow_html=True)
        r = st.columns(anchos)
        r[0].markdown(f'<div class="table-cell">{f["TEMP"]}</div>', unsafe_allow_html=True)
        r[1].markdown(f'<div class="table-cell">{f["PJ"]}</div>', unsafe_allow_html=True)
        r[2].markdown(f'<div class="table-cell">{f["GOLES"]}</div>', unsafe_allow_html=True)
        r[3].markdown(f'<div class="table-cell">{f["G_RATE"]:.2f}</div>', unsafe_allow_html=True)
        r[4].markdown(f'<div class="table-cell">{f["ASIST"]}</div>', unsafe_allow_html=True)
        r[5].markdown(f'<div class="table-cell">{f["A_RATE"]:.2f}</div>', unsafe_allow_html=True)
        r[6].markdown(f'<div class="table-cell">{f["GA"]}</div>', unsafe_allow_html=True)
        r[7].markdown(f'<div class="table-cell">{f["GA_RATE"]:.2f}</div>', unsafe_allow_html=True)
        r[8].markdown(f'<div class="table-cell">{f["AVG"]:.1f}</div>', unsafe_allow_html=True)
        with r[9]:
            if st.button("EDIT", key=f"e_{i}"):
                st.session_state.edit_index = i
                st.rerun()
        with r[10]:
            if st.button("DEL", key=f"d_{i}"):
                st.session_state.filas.pop(i)
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True) # CERRAMOS CONTENEDOR
