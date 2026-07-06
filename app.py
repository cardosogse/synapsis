import streamlit as st
import time

# 1. CONFIGURACIÓN DEL ENTORNO DE SIMULACIÓN NATIVA
st.set_page_config(page_title="ChonpsLab Pro", page_icon="⚛️", layout="centered")

# --- BANCO DE DATOS MAESTRO ---
ELEMENTOS = {
    "Carbono (C)": {"fuerza": 2.55, "color": "#ffb142", "sym": "C"},
    "Hidrógeno (H)": {"fuerza": 2.20, "color": "#00e5ff", "sym": "H"},
    "Oxígeno (O)": {"fuerza": 3.44, "color": "#ff5252", "sym": "O"},
    "Nitrógeno (N)": {"fuerza": 3.04, "color": "#33d9b2", "sym": "N"},
    "Fósforo (P)": {"fuerza": 2.19, "color": "#ff7ff5", "sym": "P"},
    "Azufre (S)": {"fuerza": 2.58, "color": "#ffda79", "sym": "S"}
}

PREGUNTAS_DESAFIO = [
    {"id": 1, "pregunta": "1. [LÍPIDOS] Las cadenas de ácidos grasos (C-H) tienen diferencia < 0.4. ¿Propiedad resultante?", "opciones": ["Polares", "Apolares/Hidrofóbicos"], "correcta": "Apolares/Hidrofóbicos", "retro": "Correcto. Son hidrofóbicos ideales para membranas."},
    {"id": 2, "pregunta": "2. [PROTEÍNAS] Enlace Peptídico (C-N). ¿Cómo se distribuye la densidad electrónica?", "opciones": ["Polar (Dipolo)", "Apolar"], "correcta": "Polar (Dipolo)", "retro": "Correcto. El Nitrógeno es más electronegativo."},
    {"id": 3, "pregunta": "3. [ADN] Enlaces Fósforo-Oxígeno (Diff 1.25). ¿Característica?", "opciones": ["Polares/Alta Energía", "Apolares"], "correcta": "Polares/Alta Energía", "retro": "Correcto. Tensión ideal para ATP/ADN."},
    {"id": 4, "pregunta": "4. [CARBOHIDRATOS] ¿Por qué la glucosa es soluble en agua?", "opciones": ["Por enlaces O-H polares", "Por ser apolar"], "correcta": "Por enlaces O-H polares", "retro": "Correcto. Forma puentes de H."},
    {"id": 5, "pregunta": "5. [PROTEÍNAS] Puentes Disulfuro (S-S). ¿Estatus?", "opciones": ["Covalente No Polar", "Iónico"], "correcta": "Covalente No Polar", "retro": "Correcto. Dif 0.0, rigidez total."}
]

# --- MOTOR GRÁFICO ---
def generar_svg_tira_afloja(fuerza):
    return """<div style='display:flex; justify-content:center; align-items:center; width:100%; height:110px;'>
        <svg viewBox="0 0 240 100" width="100%" height="100%">
            <circle cx="60" cy="50" r="24" fill="#ff5252" opacity="0.9"/>
            <text x="48" y="54" fill="white" font-weight="bold" font-family="sans-serif" font-size="12">Fuerte</text>
            <circle cx="95" cy="50" r="5" fill="#00e5ff"/>
            <ellipse cx="105" cy="50" rx="65" ry="28" fill="none" stroke="#ff5252" stroke-width="1.5" stroke-dasharray="4 2"/>
            <circle cx="180" cy="50" r="12" fill="#00e5ff" opacity="0.5"/>
        </svg>
    </div>""" if fuerza >= 3.0 else """<div style='display:flex; justify-content:center; align-items:center; width:100%; height:110px;'>
        <svg viewBox="0 0 240 100" width="100%" height="100%">
            <circle cx="60" cy="50" r="16" fill="#90a4ae" opacity="0.8"/>
            <text x="54" y="54" fill="white" font-family="sans-serif" font-size="12">Átomo</text>
            <circle cx="120" cy="50" r="5" fill="#ffffff"/>
            <circle cx="120" cy="50" r="8" fill="none" stroke="#00e5ff" stroke-width="1"/>
            <circle cx="180" cy="50" r="16" fill="#90a4ae" opacity="0.8"/>
            <ellipse cx="120" cy="50" rx="65" ry="22" fill="none" stroke="#b0bec5" stroke-width="1.2" stroke-dasharray="2 2"/>
        </svg>
    </div>"""

def generar_svg_enlace(sym1, f1, c1, sym2, f2, c2):
    diff = abs(f1 - f2)
    if diff == 0:
        cx1, cx2, ex, ew, sc, sd = 113, 127, 120, 65, "#ffffff", "2 2"
    elif diff > 0.4:
        cx1, cx2, ex, ew, sc, sd = (85, 95) if f1 > f2 else (145, 155), (100, 70) if f1 > f2 else (140, 70), (c1 if f1 > f2 else c2), "4 2"
        # Corrección de estructura para el if/else anidado
        if f1 > f2: cx1, cx2, ex, ew, sc, sd = 85, 95, 100, 70, c1, "4 2"
        else: cx1, cx2, ex, ew, sc, sd = 145, 155, 140, 70, c2, "4 2"
    else:
        cx1, cx2, ex, ew, sc, sd = 105, 135, 120, 68, "#b0bec5", "3 3"
        
    return f"""<div style='display:flex; justify-content:center; align-items:center; width:100%; height:130px;'>
        <svg viewBox="0 0 240 120" width="100%" height="100%">
            <circle cx="70" cy="60" r="22" fill="{c1}" opacity="0.85"/>
            <text x="64" y="65" fill="black" font-weight="bold" font-family="sans-serif" font-size="14">{sym1}</text>
            <circle cx="170" cy="60" r="18" fill="{c2}" opacity="0.85"/>
            <text x="164" y="64" fill="black" font-weight="bold" font-family="sans-serif" font-size="12">{sym2}</text>
            <ellipse cx="{ex}" cy="60" rx="{ew}" ry="32" fill="none" stroke="{sc}" stroke-width="1.5" stroke-dasharray="{sd}"/>
            <circle cx="{cx1}" cy="60" r="4" fill="#ffffff"/>
            <circle cx="{cx2}" cy="60" r="4" fill="#ffffff"/>
        </svg>
    </div>"""

# --- CSS CÓSMICO ---
st.markdown("""<style>.stApp{background-color:#000; background-image:radial-gradient(white, rgba(255,255,255,.2) 1px, transparent 20px);}</style>""", unsafe_allow_html=True)

# --- LOGIC ---
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; color:#fff;'>ChonpsLab Pro</h1>", unsafe_allow_html=True)
    pwd = st.text_input("Token:", type="password")
    if st.button("Entrar"): st.session_state.auth = (pwd=="CHONPS"); st.rerun()
else:
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🏛️ Atómica", "⚡ Estira", "🧬 Enlace", "🍬 Glucómica", "🌡️ pH", "🏆 Examen"])
    with tab1: st.write("Modelos atómicos...")
    with tab2: st.write("Estira y afloja...")
    with tab3: st.write("Reactor...")
    with tab4: st.write("Epímeros...")
    with tab5: st.write("Buffers...")
    with tab6: st.write("Examen...")
