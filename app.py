import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Stats Lab Pro", layout="wide")

# Estilos CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #050a14 0%, #0d1b2a 40%, #1e3a8a 80%, #3b82f6 100%);
        background-attachment: fixed;
        color: #ffffff;
    }
    .main-title { 
        font-family: 'Arial Black', sans-serif; font-size: 2.5rem; 
        text-transform: uppercase; margin-bottom: 20px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    /* ESTILO DE LA TABLA HTML PURA */
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        font-family: sans-serif;
    }
    .custom-table th {
        background-color: #1a2639;
        border: 1px solid #ffffff;
        padding: 12px;
        font-size: 0.75rem;
        text-transform: uppercase;
        font-weight: 900;
        text-align: center;
    }
    .custom-table td {
        border: 1px solid #ffffff;
        padding: 10px;
        background-color: #0b1221;
        text-align: center;
        font-weight: 600;
    }

    /* INPUTS */
    .stTextInput input, .stNumberInput input {
        background-color: rgba(0, 0, 0, 0.5) !important;
        border: none !important;
        border-bottom: 2px solid #ffffff !important;
        color: white !important;
        border-radius: 0px !important;
        font-weight: 700 !important;
    }

    /* MÉTRICAS */
    .metric-box {
        text-align: center; padding: 10px; border: 1px solid #ffffff;
        background-color: rgba(0,0,0,0.5); font-size: 0.8rem; text-transform: uppercase;
    }
    .metric-value { font-size: 1.4rem; font-weight: 900; display: block; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">STATS LAB PERFORMANCE TRACKER</h1>', unsafe_allow_html=True)

# 2. LÓGICA DE DATOS
if 'filas' not in st.session_state:
    st.session_state.filas = []
if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

# 3. PANEL DE INGRESO
with st.container():
    def_temp, def_pj, def_g, def_a = ("", 0, 0, 0)
    if st.session_state.edit_index is not None:
        e = st.session_state.filas[st.session_state.edit_index]
        def_temp, def_pj, def_g, def_a = e['TEMP'], e['PJ'], e['GOLES'], e['ASIST']

    c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
    with c1: t_in = st.text_input("Temporada / Mes", value=def_temp, key="input_temp")
    with c2: p_in = st.number_input("Partidos", min_value=0, value=def_pj, key="input_pj")
    with c3: g_in = st.number_input("Goles", min_value=0, value=def_g, key="input_g")
    with c4: a_in = st.number_input("Asistencias", min_value=0, value=def_a, key="input_a")

    b1, b2 = st.columns(2)
    with b1:
        if st.button("GUARDAR REGISTRO" if st.session_state.edit_index is None else "ACTUALIZAR"):
            if t_in:
                pj_calc = p_in if p_in > 0 else 1
                ga = g_in + a_in
                gar = round(ga/pj_calc, 2) if p_in > 0 else 0.0
                avg = round(min(max(gar * 10 / 6, 0.0), 10.0), 1)
                
                nueva_data = {
                    "TEMP": t_in, "PJ": p_in, "GOLES": g_in, 
                    "G_RATE": round(g_in/pj_calc, 2) if p_in > 0 else 0.0,
                    "ASIST": a_in, "A_RATE": round(a_in/pj_calc, 2) if p_in > 0 else 0.0, 
                    "GA": ga, "GA_RATE": gar, "AVG": avg
                }
                if st.session_state.edit_index is not None:
                    st.session_state.filas[st.session_state.edit_index] = nueva_data
                    st.session_state.edit_index = None
                else:
                    st.session_state.filas.append(nueva_data)
                st.rerun()
    with b2:
        if st.button("LIMPIAR TODO"):
            st.session_state.filas = []
            st.session_state.edit_index = None
            st.rerun()

# 4. MÉTRICAS
if st.session_state.filas:
    df = pd.DataFrame(st.session_state.filas)
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.markdown(f'<div class="metric-box">TOTAL PJ<span class="metric-value">{int(df["PJ"].sum())}</span></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="metric-box">TOTAL GOLES<span class="metric-value">{int(df["GOLES"].sum())}</span></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="metric-box">TOTAL ASIST<span class="metric-value">{int(df["ASIST"].sum())}</span></div>', unsafe_allow_html=True)
    m4.markdown(f'<div class="metric-box">TOTAL G/A<span class="metric-value">{int(df["GA"].sum())}</span></div>', unsafe_allow_html=True)
    m5.markdown(f'<div class="metric-box">AVG GLOBAL<span class="metric-value">{df["AVG"].mean():.1f}</span></div>', unsafe_allow_html=True)

# 5. TABLA DEFINITIVA (HTML)
if st.session_state.filas:
    # Construimos el HTML de la tabla manualmente para asegurar simetría total
    html_table = """
    <table class="custom-table">
        <thead>
            <tr>
                <th>Temporada</th>
                <th>PJ</th>
                <th>Goles</th>
                <th>G Rate</th>
                <th>Asistencias</th>
                <th>A Rate</th>
                <th>G/A</th>
                <th>G/A Rate</th>
                <th>AVG</th>
            </tr>
        </thead>
        <tbody>
    """
    for f in st.session_state.filas:
        html_table += f"""
            <tr>
                <td>{f['TEMP']}</td>
                <td>{f['PJ']}</td>
                <td>{f['GOLES']}</td>
                <td>{f['G_RATE']:.2f}</td>
                <td>{f['ASIST']}</td>
                <td>{f['A_RATE']:.2f}</td>
                <td>{f['GA']}</td>
                <td>{f['GA_RATE']:.2f}</td>
                <td>{f['AVG']:.1f}</td>
            </tr>
        """
    html_table += "</tbody></table>"
    
    st.markdown(html_table, unsafe_allow_html=True)

    # Controles de edición (separados para no romper la tabla)
    st.write("")
    col_ed1, col_ed2 = st.columns([1, 5])
    with col_ed1:
        idx_to_edit = st.number_input("ID fila (1, 2...)", min_value=1, max_value=len(st.session_state.filas), step=1)
    with col_ed2:
        st.write("") # Alineación visual
        eb1, eb2, _ = st.columns([1, 1, 4])
        if eb1.button("EDITAR"):
            st.session_state.edit_index = idx_to_edit - 1
            st.rerun()
        if eb2.button("BORRAR"):
            st.session_state.filas.pop(idx_to_edit - 1)
            st.rerun()
else:
    st.info("SISTEMA ONLINE. INGRESE REGISTROS.")
