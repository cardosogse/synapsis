import streamlit as st
import sqlite3
import datetime
from datetime import timedelta
import random

# ========================================================
# 1. CONFIGURACIÓN DEL CHASIS Y ESTÉTICA CÓSMICA
# ========================================================
st.set_page_config(page_title="ChonpsLab Pro | Synapsis", page_icon="⚛️", layout="wide")

def inyectar_css():
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
        .bio-panel { background-color: rgba(30, 41, 59, 0.6); border-left: 5px solid #00e5ff; padding: 20px; border-radius: 8px; margin-bottom: 20px; backdrop-filter: blur(5px);}
        .card-success { background-color: rgba(76, 175, 80, 0.1); border-left: 5px solid #4caf50; padding: 15px; border-radius: 5px; margin-top: 10px; }
        .card-error { background-color: rgba(244, 67, 54, 0.1); border-left: 5px solid #f44336; padding: 15px; border-radius: 5px; margin-top: 10px; }
        .card-hint { background-color: rgba(255, 177, 66, 0.1); border-left: 5px solid #ffb142; padding: 15px; border-radius: 5px; margin-top: 10px; color: #ffda79;}
        .monitor-box { background-color: rgba(255,255,255,0.05); padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 10px;}
        .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: transparent; }
        .stTabs [data-baseweb="tab"] { background-color: rgba(255,255,255,0.05); border-radius: 4px 4px 0 0; padding: 10px 20px; color: #90a4ae; font-weight: bold;}
        .stTabs [aria-selected="true"] { background-color: rgba(0, 229, 255, 0.15) !important; color: #00e5ff !important; border-bottom: 2px solid #00e5ff !important; }
        
        /* Modificadores dinámicos para la coherencia cromática de la línea del tiempo */
        .card-dalton { background-color: rgba(144, 164, 174, 0.1); border-left: 5px solid #90a4ae; padding: 20px; border-radius: 5px; }
        .card-thomson { background-color: rgba(33, 150, 243, 0.1); border-left: 5px solid #2196f3; padding: 20px; border-radius: 5px; }
        .card-bohr { background-color: rgba(255, 177, 66, 0.1); border-left: 5px solid #ffb142; padding: 20px; border-radius: 5px; }
        .card-schrodinger { background-color: rgba(0, 229, 255, 0.1); border-left: 5px solid #00e5ff; padding: 20px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# ========================================================
# 2. CAPA DE SERVICIOS: BASE DE DATOS Y AUTENTICACIÓN
# ========================================================
DB_NAME = 'synapsis_auth.db'

def inicializar_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tokens_acceso
                 (token TEXT PRIMARY KEY, fecha_expiracion DATE, en_uso BOOLEAN, identificador_usuario TEXT)''')
    
    token_prueba = "SYNAPSIS-PRO-2026"
    fecha_futura = datetime.date.today() + timedelta(days=30)
    c.execute("INSERT OR IGNORE INTO tokens_acceso (token, fecha_expiracion, en_uso, identificador_usuario) VALUES (?, ?, ?, ?)", 
              (token_prueba, fecha_futura, False, "Admin"))
    conn.commit()
    conn.close()

def validar_y_bloquear_token(token_ingresado):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT fecha_expiracion, en_uso FROM tokens_acceso WHERE token = ?", (token_ingresado,))
    resultado = c.fetchone()
    
    if resultado:
        fecha_exp = datetime.datetime.strptime(resultado[0], "%Y-%m-%d").date()
        en_uso = resultado[1]
        
        if datetime.date.today() > fecha_exp:
            conn.close()
            return False, "El token ha expirado. Renueva tu suscripción."
            
        if en_uso:
            conn.close()
            return False, "Acceso denegado: Este token ya está activo en otro dispositivo. Cierra la sesión previa."
        
        c.execute("UPDATE tokens_acceso SET en_uso = 1 WHERE token = ?", (token_ingresado,))
        conn.commit()
        conn.close()
        return True, "Acceso concedido. Conexión segura establecida."
    
    conn.close()
    return False, "Token inexistente o inválido."

def liberar_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET en_uso = 0 WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def registrar_nuevo_usuario(token, dias_duracion, identificador="Nuevo Estudiante"):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    exp = datetime.date.today() + timedelta(days=dias_duracion)
    try:
        c.execute("INSERT INTO tokens_acceso VALUES (?, ?, ?, ?)", (token.upper(), exp, False, identificador))
        conn.commit()
        mensaje = f"Token {token} registrado con éxito hasta {exp}"
    except sqlite3.IntegrityError:
        mensaje = f"Error: El token {token} ya existe en la base de datos."
    conn.close()
    return mensaje

# ========================================================
# 3. CAPA DE DATOS Y LÓGICA CIENTÍFICA
# ========================================================
ELEMENTOS = {
    "Carbono (C)": {"fuerza": 2.55, "color": "#ffb142", "sym": "C"},
    "Hidrógeno (H)": {"fuerza": 2.20, "color": "#00e5ff", "sym": "H"},
    "Oxígeno (O)": {"fuerza": 3.44, "color": "#ff5252", "sym": "O"},
    "Nitrógeno (N)": {"fuerza": 3.04, "color": "#33d9b2", "sym": "N"},
    "Fósforo (P)": {"fuerza": 2.19, "color": "#ff7ff5", "sym": "P"},
    "Azufre (S)": {"fuerza": 2.58, "color": "#ffda79", "sym": "S"}
}

@st.cache_data
def generar_svg_tira_afloja(fuerza):
    if fuerza >= 3.0:
        return """
        <div style='display:flex; justify-content:center; align-items:center; width:100%; height:110px;'>
            <svg viewBox="0 0 240 100" width="100%" height="100%">
                <circle cx="60" cy="50" r="24" fill="#ff5252" opacity="0.9"/>
                <text x="48" y="54" fill="white" font-weight="bold" font-family="sans-serif" font-size="12">Fuerte</text>
                <circle cx="95" cy="50" r="5" fill="#00e5ff"/>
                <ellipse cx="105" cy="50" rx="65" ry="28" fill="none" stroke="#ff5252" stroke-width="1.5" stroke-dasharray="4 2"/>
                <circle cx="180" cy="50" r="12" fill="#00e5ff" opacity="0.5"/>
            </svg>
        </div>
        """
    else:
        return """
        <div style='display:flex; justify-content:center; align-items:center; width:100%; height:110px;'>
            <svg viewBox="0 0 240 100" width="100%" height="100%">
                <circle cx="60" cy="50" r="16" fill="#90a4ae" opacity="0.8"/>
                <text x="54" y="54" fill="white" font-family="sans-serif" font-size="12">Átomo</text>
                <circle cx="120" cy="50" r="5" fill="#ffffff"/>
                <circle cx="120" cy="50" r="8" fill="none" stroke="#00e5ff" stroke-width="1"/>
                <circle cx="180" cy="50" r="16" fill="#90a4ae" opacity="0.8"/>
                <ellipse cx="120" cy="50" rx="65" ry="22" fill="none" stroke="#b0bec5" stroke-width="1.2" stroke-dasharray="2 2"/>
            </svg>
        </div>
        """

@st.cache_data
def generar_svg_enlace(sym1, f1, c1, sym2, f2, c2):
    diff = abs(f1 - f2)
    if diff == 0:
        cx_e1, cx_e2 = 113, 127
        ellipse_x, ellipse_w = 120, 65
        stroke_color = "#ffffff"
        stroke_dash = "2 2"
    elif diff > 0.4:
        cx_e1, cx_e2 = (85, 95) if f1 > f2 else (145, 155)
        ellipse_x, ellipse_w = (100, 70) if f1 > f2 else (140, 70)
        stroke_color = c1 if f1 > f2 else c2
        stroke_dash = "4 2"
    else:
        cx_e1, cx_e2 = (105, 135)
        ellipse_x, ellipse_w = (120, 68)
        stroke_color = "#b0bec5"
        stroke_dash = "3 3"

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

def mezclar_memorama():
    contenido = [
        ("Dalton (1810)", 1), ("Materia indivisible sin cargas", 1),
        ("Thomson / Rutherford", 2), ("Naturaleza eléctrica (Electrón y vacío)", 2),
        ("Bohr (1913)", 3), ("Órbitas planas bidimensionales", 3),
        ("Schrödinger (1926)", 4), ("Orbitales 3D (Flexibilidad cuántica)", 4)
    ]
    random.shuffle(contenido)
    return contenido

# ========================================================
# 4. GESTIÓN DEL ESTADO GLOBAL
# ========================================================
def inicializar_estado():
    if "auth" not in st.session_state: st.session_state["auth"] = False
    if "token_actual" not in st.session_state: st.session_state["token_actual"] = ""
    if "vidas" not in st.session_state: st.session_state["vidas"] = 3
    if "errores_quiz" not in st.session_state: st.session_state["errores_quiz"] = 0
    if "advertencia_ph" not in st.session_state: st.session_state["advertencia_ph"] = False
    
    # Estados del Memorama
    if "memo_tablero" not in st.session_state: st.session_state["memo_tablero"] = mezclar_memorama()
    if "memo_reveladas" not in st.session_state: st.session_state["memo_reveladas"] = []
    if "memo_resueltas" not in st.session_state: st.session_state["memo_resueltas"] = []
    if "memo_completado" not in st.session_state: st.session_state["memo_completado"] = False

# ========================================================
# 5. CONTROLADOR PRINCIPAL DE LA INTERFAZ
# ========================================================
def main():
    inyectar_css()
    inicializar_db()
    inicializar_estado()

    if not st.session_state["auth"]:
        st.markdown("<h1 class='main-title'>Chonps<span class='main-title-suffix'>Lab</span> Pro</h1>", unsafe_allow_html=True)
        st.markdown("<p class='sub-title'>Plataforma de Simulación Bioquímica - Nodo Synapsis</p>", unsafe_allow_html=True)
        st.markdown("""
        <div class='bio-panel'>
            <span style='color:#00e5ff; font-weight:700; font-size:1.25rem;'>Acceso Restringido</span>
            <p style='color:#cfd8dc; margin-top:10px;'>Ingresa tu token de suscripción activo para desplegar el entorno de simulación.</p>
        </div>
        """, unsafe_allow_html=True)
        
        pwd = st.text_input("Token de Licencia:", type="password")
        if st.button("Autenticar Terminal", use_container_width=True):
            token_limpio = pwd.strip().upper()
            es_valido, mensaje = validar_y_bloquear_token(token_limpio)
            if es_valido:
                st.session_state["auth"] = True
                st.session_state["token_actual"] = token_limpio
                st.success(mensaje)
                st.rerun()
            else:
                st.error(f"Error: {mensaje}")
        
        with st.expander("⚙️ Panel de Administración (Generador de Tokens)"):
            st.markdown("Crea nuevas suscripciones o desbloquea tokens atascados.")
            c_admin1, c_admin2 = st.columns(2)
            with c_admin1:
                nuevo_token = st.text_input("Nuevo Token (Ej: ALUMNO-101):").strip().upper()
                dias = st.number_input("Días de vigencia:", min_value=1, value=30)
                if st.button("Crear Suscripción", type="primary"):
                    if nuevo_token:
                        res = registrar_nuevo_usuario(nuevo_token, dias)
                        st.info(res)
                    else: st.warning("Escribe un token válido.")
            with c_admin2:
                token_bloqueado = st.text_input("Forzar desbloqueo de Token:").strip().upper()
                if st.button("Liberar Token", type="secondary"):
                    if token_bloqueado:
                        liberar_token(token_bloqueado)
                        st.success(f"Token {token_bloqueado}自由 liberado forzosamente.")
                    else: st.warning("Escribe el token a liberar.")

    else:
        with st.sidebar:
            st.markdown(f"**Usuario en línea:** `{st.session_state['token_actual']}`")
            if st.button("🚪 Cerrar Sesión Segura", use_container_width=True):
                liberar_token(st.session_state["token_actual"])
                st.session_state["auth"] = False
                st.session_state["token_actual"] = ""
                st.rerun()
            st.markdown("---")
            st.caption("Cerrar sesión de forma explícita libera la concurrencia en la base de datos.")

        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown("<h2 style='color:#00e5ff; margin-top:0;'>Consola de Operaciones</h2>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='monitor-box'><span style='color:#90a4ae; font-size:12px;'>ESTABILIDAD CELULAR</span><br><b style='font-size:20px; color:#f44336;'>{st.session_state.vidas} / 3 💔</b></div>", unsafe_allow_html=True)

        if st.session_state.vidas <= 0:
            st.error("🚨 COLAPSO METABÓLICO: Lisis celular detectada por acumulación de fallos.")
            if st.button("Reiniciar Simulador"):
                st.session_state.vidas = 3
                st.session_state.advertencia_ph = False
                st.session_state.errores_quiz = 0
                st.rerun()
            return

        # ----------------------------------------------------
        # SISTEMA DE PESTAÑAS CON EL ORDEN PEDAGÓGICO NUEVO
        # ----------------------------------------------------
        tabs = st.tabs([
            "🏛️ Módulo 1: Evolución del Modelo Atómico", 
            "⚡ Módulo 2: Estira y Afloja", 
            "🧬 Módulo 3: Reactores de Enlace", 
            "🌡️ Módulo 4: Equilibrio Ácido-Base y pH", 
            "🍬 Módulo 5: Glucómica e Isomerismo", 
            "🏆 Evaluación Final"
        ])

        # ========================================================
        # MÓDULO 1: EVOLUCIÓN DEL MODELO ATÓMICO (CAPA ACTUALIZADA)
        # ========================================================
        with tabs[0]:
            st.markdown("### Línea del Tiempo Atómica")
            st.caption("*💡 Desplace o mueva la línea del tiempo horizontal para descubrir
