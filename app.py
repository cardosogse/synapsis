import streamlit as st
import time
import sqlite3
import hashlib
import uuid
from datetime import datetime, timedelta

# ========================================================
# 1. MOTOR DE BASE DE DATOS Y SEGURIDAD ANTIPIRATERÍA
# ========================================================
DB_NAME = "licenses.db"

def init_db():
    """Inicializa la base de datos de licencias con control de hardware y caducidad."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS licenses (
            token TEXT PRIMARY KEY,
            is_active INTEGER,
            activation_date TIMESTAMP,
            expiration_date TIMESTAMP,
            device_fingerprint TEXT
        )
    ''')
    # Inyectar una licencia de prueba si no existe
    c.execute("SELECT * FROM licenses WHERE token='ADMIN-TEST-2026'")
    if not c.fetchone():
        now = datetime.now()
        exp = now + timedelta(days=30)
        c.execute("INSERT INTO licenses VALUES (?, 1, ?, ?, NULL)", 
                  ('ADMIN-TEST-2026', now, exp))
    conn.commit()
    conn.close()

def get_device_fingerprint():
    """
    Genera un hash único basado en las cabeceras del cliente.
    Arquitectura robusta para Streamlit Cloud sin dependencias privadas.
    """
    # 1. Intentar usar la API oficial moderna de Streamlit (v1.37+)
    if hasattr(st, "context") and hasattr(st.context, "headers"):
        headers = st.context.headers
        user_agent = headers.get("User-Agent", "Unknown-Agent")
        accept_lang = headers.get("Accept-Language", "Unknown-Lang")
        
        raw_fingerprint = f"{user_agent}-{accept_lang}"
        return hashlib.sha256(raw_fingerprint.encode()).hexdigest()
    
    # 2. Mecanismo de contingencia (Fallback) si la API falla
    if "session_device_id" not in st.session_state:
        fallback_id = str(uuid.uuid4())
        st.session_state["session_device_id"] = hashlib.sha256(fallback_id.encode()).hexdigest()
        
    return st.session_state["session_device_id"]

def validate_token(token_input):
    """Lógica estricta de validación y bloqueo."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT is_active, expiration_date, device_fingerprint FROM licenses WHERE token=?", (token_input,))
    record = c.fetchone()
    
    if not record:
        conn.close()
        return False, "Token inexistente en la matriz de acceso."
    
    is_active, expiration_str, stored_fingerprint = record
    
    if not is_active:
        conn.close()
        return False, "Esta licencia ha sido revocada por violaciones de seguridad."
        
    # Manejar formatos de fecha con o sin microsegundos
    try:
        expiration_date = datetime.strptime(expiration_str.split('.')[0], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        expiration_date = datetime.strptime(expiration_str, '%Y-%m-%d %H:%M:%S.%f')
        
    if datetime.now() > expiration_date:
        conn.close()
        return False, "Tu suscripción de 30 días ha caducado. Adquiere una nueva licencia."
        
    current_fingerprint = get_device_fingerprint()
    
    if stored_fingerprint is None:
        # Primer uso: Acoplar licencia al dispositivo actual
        c.execute("UPDATE licenses SET device_fingerprint=? WHERE token=?", (current_fingerprint, token_input))
        conn.commit()
        conn.close()
        return True, "Licencia acoplada exitosamente a este dispositivo."
    elif stored_fingerprint != current_fingerprint:
        # Intento de piratería detectado (diferente dispositivo)
        c.execute("UPDATE licenses SET is_active=0 WHERE token=?", (token_input,))
        conn.commit()
        conn.close()
        return False, "🚨 INFRACCIÓN: Uso concurrente detectado. La licencia ha sido destruida y el acceso bloqueado permanentemente."
        
    conn.close()
    return True, "Acceso Autorizado."

# ========================================================
# 2. CONFIGURACIÓN DEL CHASIS Y ESTÉTICA CÓSMICA
# ========================================================
st.set_page_config(page_title="ChonpsLab | Entorno Metabólico", page_icon="⚛️", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #000000 !important;
        background-image: 
            radial-gradient(white, rgba(255,255,255,.2) 1px, transparent 20px),
            radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 30px);
        background-size: 350px 350px, 200px 200px;
        background-position: 0 0, 40px 60px;
    }
    .main-title { text-align: center; color: #ffffff; font-size: 3.8rem; font-weight: 800; margin-bottom: 0px; letter-spacing: 2px;}
    .main-title-suffix { color: #00e5ff; font-weight: 300; }
    .sub-title { text-align: center; font-style: italic; color: #90a4ae; font-size: 1.2rem; margin-top: 5px; margin-bottom: 30px; }
    .bio-panel { background-color: rgba(30, 41, 59, 0.8); border-left: 5px solid #00e5ff; padding: 20px; border-radius: 8px; margin-bottom: 20px; backdrop-filter: blur(5px);}
    .card-success { background-color: rgba(76, 175, 80, 0.15); border-left: 5px solid #4caf50; padding: 15px; border-radius: 5px; margin-top: 10px; color: white;}
    .card-error { background-color: rgba(244, 67, 54, 0.15); border-left: 5px solid #f44336; padding: 15px; border-radius: 5px; margin-top: 10px; color: white;}
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] { background-color: rgba(255,255,255,0.05); border-radius: 4px 4px 0 0; padding: 10px 20px; color: #90a4ae; font-weight: bold;}
    .stTabs [aria-selected="true"] { background-color: rgba(0, 229, 255, 0.15) !important; color: #00e5ff !important; border-bottom: 2px solid #00e5ff !important; }
</style>
""", unsafe_allow_html=True)

# ========================================================
# 3. BASE DE DATOS MAESTRA CHONPS Y MOTOR SVG
# ========================================================
ELEMENTOS = {
    "Carbono (C)": {"fuerza": 2.55, "color": "#ffb142", "sym": "C"},
    "Hidrógeno (H)": {"fuerza": 2.20, "color": "#00e5ff", "sym": "H"},
    "Oxígeno (O)": {"fuerza": 3.44, "color": "#ff5252", "sym": "O"},
    "Nitrógeno (N)": {"fuerza": 3.04, "color": "#33d9b2", "sym": "N"}
}

@st.cache_data
def generar_svg_enlace(sym1, f1, c1, sym2, f2, c2):
    diff = abs(f1 - f2)
    if diff == 0:
        cx_e1, cx_e2, ellipse_x, ellipse_w, stroke_color, stroke_dash = 113, 127, 120, 65, "#ffffff", "2 2"
    elif diff > 0.4:
        cx_e1, cx_e2 = (85, 95) if f1 > f2 else (145, 155)
        ellipse_x, ellipse_w = (100, 70) if f1 > f2 else (140, 70)
        stroke_color, stroke_dash = (c1 if f1 > f2 else c2), "4 2"
    else:
        cx_e1, cx_e2, ellipse_x, ellipse_w, stroke_color, stroke_dash = 105, 135, 120, 68, "#b0bec5", "3 3"

    return f"""
    <div style='display:flex; justify-content:center; align-items:center; width:100%; height:130px;'>
        <svg viewBox="0 0 240 120" width="100%" height="100%">
            <circle cx="70" cy="60" r="22" fill="{c1}" opacity="0.85"/>
            <text x="64" y="65" fill="black" font-weight="bold" font-family="sans-serif" font-size="14">{sym1}</text>
            <circle cx="170" cy="60" r="18" fill="{c2}" opacity="0.85"/>
            <text x="164" y="64" fill="black" font-weight="bold" font-family="sans-serif" font-size="12">{sym2}</text>
            <ellipse cx="{ellipse_x}" cy="60" rx="{ellipse_w}" ry="32" fill="none" stroke="{stroke_color}" stroke-width="1.5" stroke-dasharray="{stroke_dash}"/>
            <circle cx="{cx_e1}" cy="60" r="4" fill="#ffffff"/>
            <circle cx="{cx_e2}" cy="60" r="4" fill="#ffffff"/>
        </svg>
    </div>
    """

# ========================================================
# 4. GESTIÓN DE ESTADOS Y FLUJO PEDAGÓGICO
# ========================================================
if "auth" not in st.session_state: st.session_state["auth"] = False
if "vidas" not in st.session_state: st.session_state["vidas"] = 3
if "nivel_desbloqueado" not in st.session_state: st.session_state["nivel_desbloqueado"] = 1

init_db()

# ========================================================
# 5. PORTAL DE ACCESO CRIPTOGRÁFICO
# ========================================================
if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>Chonps<span class='main-title-suffix'>Lab</span></h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Entorno Híbrido de Aprendizaje Metabólico</p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        <div class='bio-panel'>
            <span style='color:#00e5ff; font-weight:700; font-size:1.25rem;'>🔐 Terminal de Autenticación</span>
            <p style='color:#cfd8dc; margin-top:10px;'>Este software está protegido por un sistema de hardware-lock temporal. Ingresa tu token de suscripción mensual. Las licencias son intransferibles.</p>
        </div>
        """, unsafe_allow_html=True)
        
        pwd = st.text_input("Licencia de Acceso (Token Único):", type="password")
        if st.button("Verificar Credenciales y Desencriptar", use_container_width=True):
            is_valid, message = validate_token(pwd.strip())
            if is_valid:
                st.session_state["auth"] = True
                st.success(message)
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"Acceso Denegado: {message}")

# ========================================================
# 6. LABORATORIO Y RUTA DE APRENDIZAJE
# ========================================================
else:
    c1, c2 = st.columns([3, 1])
    with c1: st.markdown("<h2 style='color:#00e5ff; margin-top:0;'>Consola de Operaciones</h2>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div style='text-align:right; color:#90a4ae;'>Integridad del Sistema: <b style='color:#f44336; font-size:18px;'>{st.session_state.vidas}/3 💔</b></div>", unsafe_allow_html=True)

    if st.session_state.vidas <= 0:
        st.error("🚨 COLAPSO: Límite de errores alcanzado. Debes repasar la teoría para volver a intentarlo.")
        if st.button("Reiniciar Entorno de Pruebas"):
            st.session_state.vidas = 3
            st.session_state.nivel_desbloqueado = 1
            st.rerun()
        st.stop()

    # Pestañas Dinámicas (Progreso Escalonado)
    tab_titles = ["📖 Módulo 1: Teoría Atómica", "⚡ Módulo 2: Enlaces (Práctica)", "🏆 Módulo 3: Evaluación Final"]
    tabs = st.tabs(tab_titles)

    # --- MÓDULO 1: TEORÍA ---
    with tabs[0]:
        st.markdown("### Paso 1: Fundamentos Bioquímicos")
        st.info("💡 **Objetivo Pedagógico:** Comprender cómo la evolución de la teoría atómica impacta directamente en la formación de macromoléculas biológicas.")
        
        modelo = st.selectbox("Analiza los modelos históricos:", ["Seleccionar...", "Bohr (1913)", "Schrödinger (Modelo Cuántico)"])
        if modelo == "Bohr (1913)":
            st.write("El electrón gira en órbitas fijas. Útil para química básica, pero insuficiente para explicar enlaces complejos.")
        elif modelo == "Schrödinger (Modelo Cuántico)":
            st.write("Introduce los **orbitales** (nubes de probabilidad). Fundamental para entender la hibridación del carbono ($sp^3$) en moléculas orgánicas.")
            st.markdown("<div class='card-success'>✅ Teoría asimilada. Procede a confirmar tu entendimiento.</div>", unsafe_allow_html=True)
            
            if st.button("Confirmar Comprensión y Desbloquear Laboratorio"):
                if st.session_state.nivel_desbloqueado < 2:
                    st.session_state.nivel_desbloqueado = 2
                    st.success("Módulo 2 Desbloqueado. Ve a la siguiente pestaña.")
                    time.sleep(0.5)
                    st.rerun()

    # --- MÓDULO 2: LABORATORIO PRÁCTICO ---
    with tabs[1]:
        if st.session_state.nivel_desbloqueado < 2:
            st.warning("🔒 Debes completar el Módulo 1 para acceder a los reactores de enlace.")
        else:
            st.markdown("### Paso 2: Reactor de Electronegatividad")
            st.write("Experimenta combinando átomos para visualizar el comportamiento de la nube electrónica según la escala de Pauling.")
            
            c1, c2 = st.columns(2)
            atom1 = c1.selectbox("Átomo Central (A):", list(ELEMENTOS.keys()))
            atom2 = c2.selectbox("Átomo de Reacción (B):", list(ELEMENTOS.keys()))
            
            if st.button("Ensamblar Enlace", use_container_width=True):
                a1, a2 = ELEMENTOS[atom1], ELEMENTOS[atom2]
                st.components.v1.html(generar_svg_enlace(a1['sym'], a1['fuerza'], a1['color'], a2['sym'], a2['fuerza'], a2['color']), height=140)
                
                diff = abs(a1['fuerza'] - a2['fuerza'])
                if diff == 0:
                    st.markdown("<div class='card-success'><b>✅ Enlace Covalente No Polar Puro</b> (Simetría orbital perfecta).</div>", unsafe_allow_html=True)
                elif diff <= 1.7:
                    st.markdown("<div class='card-success' style='border-left-color:#ffb142;'><b>⚡ Enlace Covalente Polar</b> (Formación de dipolos activos).</div>", unsafe_allow_html=True)
                
                if st.session_state.nivel_desbloqueado < 3:
                    st.session_state.nivel_desbloqueado = 3
                    st.info("Experimentación completada. Tienes autorización para el Desafío Final.")

    # --- MÓDULO 3: EVALUACIÓN ---
    with tabs[2]:
        if st.session_state.nivel_desbloqueado < 3:
            st.warning("🔒 Experimenta en el Módulo 2 para habilitar tu evaluación final.")
        else:
            st.markdown("### Desafío Final: Certificación de Matriz")
            st.write("Responde basándote en la teoría y práctica previas. Una respuesta incorrecta deducirá una vida del sistema.")
            
            q1 = st.radio("Según el simulador, ¿qué sucede cuando se unen dos átomos con idéntica electronegatividad?", 
                          ["Selecciona...", "Se forma un dipolo eléctrico.", "La nube electrónica mantiene una simetría perfecta (Covalente No Polar).", "El enlace colapsa iónicamente."], index=0)
            
            if st.button("Evaluar Bitácora"):
                if q1 == "Selecciona...":
                    st.warning("Debes responder la pregunta.")
                elif q1 == "La nube electrónica mantiene una simetría perfecta (Covalente No Polar).":
                    st.balloons()
                    st.success("🏆 **CERTIFICACIÓN APROBADA.** Has dominado la hibridación de teoría y experimentación digital.")
                else:
                    st.session_state.vidas -= 1
                    st.error("❌ Respuesta incorrecta. Impacto crítico en el sistema. Has perdido 1 Vida.")
                    time.sleep(1)
                    st.rerun()
