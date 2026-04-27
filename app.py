import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN Y ESTILO AVANZADO
st.set_page_config(page_title="Stats Lab Pro", layout="wide")

st.markdown("""
    <style>
    /* Degradado de azul profundo */
    .stApp {
        background: linear-gradient(180deg, #0d1b2a 0%, #1b263b 50%, #0d1b2a 100%);
        background-attachment: fixed;
        color: #e0e1dd;
    }
    
    /* Título con peso visual */
    .main-title { 
        font-family: 'Arial Black', sans-serif; 
        font-size: 3rem; 
        text-transform: uppercase; 
        line-height: 1; 
        margin-bottom: 30px;
        color: #ffffff;
        border-left: 10px solid #4facfe;
        padding-left: 20px;
    }

    /* Contenedores de Entrada de Datos (Input Boxes) */
    .stNumberInput div div input, .stTextInput div div input {
        background-color: rgba(13, 27, 42, 0.8) !important;
        border: 2px solid #4facfe !important; /* Borde cian sólido */
        color: #ffffff !important;
        border-radius: 0px !important;
        height: 50px !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        box-shadow: inset 0 0 10px rgba(79, 172, 254, 0.2);
    }

    /* Labels - Tipografía más imponente */
    label {
        color: #4facfe !important;
        font-family: 'Verdana', sans-serif !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px !important;
    }

    /* Botones Estilo Consola */
    .stButton>button {
        background-color: transparent !important;
        border: 2px solid #ffffff !important;
        color: #ffffff !important;
        border-radius: 0px !important;
        height: 50px !important;
        width: 100%;
        font-weight: 900 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: 0.4s;
    }

    .stButton>button:hover {
        background-color: #ffffff !important;
        color: #0d1b2a !important;
        box-shadow: 0 0 20px rgba(255,255,255,0.4);
    }

    /* Filas de la tabla manual */
    .data-row {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 5px;
        border-radius: 4px;
    }

    .header-row {
        background-color: rgba(79, 172, 254, 0.15);
        padding: 10px;
        border-bottom: 2px solid #4facfe;
        font-weight: 900;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">STATS LAB<br>PERFORMANCE TRACKER</h1>', unsafe_allow_html=True)

# 2. GESTIÓN DE DATOS
if 'filas' not in st.session_state:
    st.session_state.filas = []
if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

# 3. PANEL DE CONTROL (INGRESO)
with st.container():
    st.markdown("### 🛠️ CONFIGURACIÓN DE REGISTRO")
    
    # Valores para edición
    def_temp, def_pj, def_g, def_a = ("", 1, 0, 0)
    if st.session_state.edit_index is not None:
        e = st.session_state.filas[st.session_state.edit_index]
        def_temp, def_pj, def_g, def_a = e['TEMP'], e['PJ'], e['GOLES'], e['ASIST']

    c1, c2, c3, c4 = st.columns([2.5, 1, 1, 1])
    with c1: temp_in = st.text_input("Temporada / Mes", value=def_temp)
    with c2: pj_in = st.number_input("Partidos", min_value=1, value=def_pj)
    with c3: g_in = st.number_input("Goles", min_value=0, value=def_g)
    with c4: a_in = st.number_input("Asistencias", min_value=0, value=def_a)

    # Botones de Acción
    ca, cb = st.columns([1, 1])
    with ca:
        if st.session_state.edit_index is None:
            if st.button("🚀 AGREGAR NUEVO REGISTRO"):
                ga = g_in + a_in
                gar = round(ga/pj_in, 2)
                avg = 10.0 if gar >= 6 else (0.0 if gar <= 0 else round((gar * 10) / 6, 1))
                st.session_state.filas.append({
                    "TEMP": temp_in, "PJ": pj_in, "GOLES": g_in, "G_RATE": round(g_in/pj_in, 2),
                    "ASIST": a_in, "A_RATE": round(a_in/pj_in, 2), "GA": ga, "GA_RATE": gar, "AVG": avg
                })
                st.rerun()
        else:
            if st.button("💾 GUARDAR CAMBIOS"):
                ga = g_in + a_in
                gar = round(ga/pj_in, 2)
                avg = 10.0 if gar >= 6 else (0.0 if gar <= 0 else round((gar * 10) / 6, 1))
                st.session_state.filas[st.session_state.edit_index] = {
                    "TEMP": temp_in, "PJ": pj_in, "GOLES": g_in, "G_RATE": round(g_in/pj_in, 2),
                    "ASIST": a_in, "A_RATE": round(a_in/pj_in, 2), "GA": ga, "GA_RATE": gar, "AVG": avg
                }
                st.session_state.edit_index = None
                st.rerun()
    with cb:
        if st.button("🧹 LIMPIAR TODO"):
            st.session_state.filas = []
            st.session_state.edit_index = None
            st.rerun()

st.divider()

# 4. DASHBOARD DE RESULTADOS
if st.session_state.filas:
    # Encabezados Reales
    st.markdown('<div class="header-row">', unsafe_allow_html=True)
    h = st.columns([2, 1, 1, 1, 1, 1, 1, 1, 1, 0.8, 0.8])
    labels = ["Temporada", "PJ", "Goles", "G Rate", "Asistencias", "A Rate", "G/A", "G/A Rate", "AVG", "Edit", "Del"]
    for col, text in zip(h, labels):
        col.write(text)
    st.markdown('</div>', unsafe_allow_html=True)

    # Datos
    for i, f in enumerate(st.session_state.filas):
        row = st.columns([2, 1, 1, 1, 1, 1, 1, 1, 1, 0.8, 0.8])
        row[0].write(f"**{f['TEMP']}**")
        row[1].write(f['PJ'])
        row[2].write(f['GOLES'])
        row[3].write(f"{f['G_RATE']:.2f}")
        row[4].write(f['ASIST'])
        row[5].write(f"{f['A_RATE']:.2f}")
        row[6].write(f['GA'])
        row[7].write(f"{f['GA_RATE']:.2f}")
        row[8].write(f"⭐ {f['AVG']:.1f}")
        
        if row[9].button("✏️", key=f"e_{i}"):
            st.session_state.edit_index = i
            st.rerun()
        if row[10].button("❌", key=f"d_{i}"):
            st.session_state.filas.pop(i)
            st.rerun()

    # Métricas Finales
    st.divider()
    df = pd.DataFrame(st.session_state.filas)
    m1, m2, m3 = st.columns(3)
    m1.metric("PARTIDOS TOTALES", df["PJ"].sum())
    m2.metric("GOLES TOTALES", df["GOLES"].sum())
    m3.metric("RATING PROMEDIO", f"{df['AVG'].mean():.1f}")

else:
    st.info("SISTEMA DE MONITOREO ACTIVO. INGRESE DATOS PARA COMENZAR.")
