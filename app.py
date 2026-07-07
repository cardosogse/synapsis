import streamlit as st
import sqlite3
import datetime
from datetime import timedelta
import random

# ========================================================
# 1. CONFIGURACIÓN DEL CHASIS Y ESTÉTICA CÓSMICA DE ALTA LEGIBILIDAD
# ========================================================
st.set_page_config(page_title="ChonpsLab Pro | Synapsis", page_icon="⚛️", layout="wide")

def inyectar_css():
    st.markdown("""
    <style>
        /* Fondo cósmico purgado: estrellas tipo píxel de 1px sin auras de neblina para contraste del 100% */
        .stApp {
            background-color: #000000 !important;
            background-image: 
                radial-gradient(white 1px, transparent 1px),
                radial-gradient(white 1px, transparent 1px);
            background-size: 250px 250px, 150px 150px;
            background-position: 0 0, 30px 40px;
        }
        .main-title { text-align: center; color: #ffffff; font-size: 3.8rem; font-weight: 800; margin-bottom: 0px; letter-spacing: 2px;}
        .main-title-suffix { color: #00e5ff; font-weight: 300; }
        .sub-title { text-align: center; font-style: italic; color: #90a4ae; font-size: 1.2rem; margin-top: 5px; margin-bottom: 30px; }
        .bio-panel { background-color: rgba(30, 41, 59, 0.6); border-left: 5px solid #00e5ff; padding: 20px; border-radius: 8px; margin-bottom: 20px; backdrop-filter: blur(5px);}
        .card-success { background-color: rgba(76, 175, 80, 0.1); border-left: 5px solid #4caf50; padding: 15px; border-radius: 5px; margin-top: 10px; }
        .card-error { background-color: rgba(244, 67, 54, 0.1); border-left: 5px solid #f44336; padding: 15px; border-radius: 5px; margin-top: 10px; }
        .card-hint { background-color: rgba(255, 177, 66, 0.1); border-left: 5px solid #ffb142; padding: 15px; border-radius: 5px; margin-top: 10px; color: #ffda79;}
        .monitor-box { background-color: rgba(255,255,255,0.05); padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 10px;}
        
        /* Estilizado de pestañas principales */
        .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: transparent; }
        .stTabs [data-baseweb="tab"] { background-color: rgba(255,255,255,0.05); border-radius: 4px 4px 0 0; padding: 10px 20px; color: #90a4ae; font-weight: bold;}
        .stTabs [aria-selected="true"] { background-color: rgba(0, 229, 255, 0.15) !important; color: #00e5ff !important; border-bottom: 2px solid #00e5ff !important; }
        
        /* INYECCIÓN DE ESTILOS PARA EL SUB-NAVEGADOR TÁCTIL (BOTONERA DE ESTACIONES) */
        div[data-testid="stRadio"] > div{
            flex-direction: row !important;
            gap: 12px !important;
            flex-wrap: wrap;
        }
        div[data-testid="stRadio"] label {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            padding: 10px 18px !important;
            border-radius: 20px !important;
            color: #cfd8dc !important;
            transition: all 0.2s ease-in-out !important;
            cursor: pointer !important;
        }
        div[data-testid="stRadio"] label:hover {
            background-color: rgba(0, 229, 255, 0.08) !important;
            border-color: #00e5ff !important;
            color: #ffffff !important;
        }
        div[data-testid="stRadio"] label[data-checked="true"] {
            background-color: rgba(0, 229, 255, 0.18) !important;
            border-color: #00e5ff !important;
            color: #00e5ff !important;
            font-weight: bold !important;
        }
        /* Ocultar el círculo nativo feo del radio button para simular botones limpios */
        div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"]-prefix {
            display: none !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
            display: none !important;
        }

        /* Animación de pulso/parpadeo sutil para el foco instructivo */
        @keyframes parpadeoPulso {
            0% { opacity: 0.3; text-shadow: 0 0 0px transparent; }
            50% { opacity: 1; text-shadow: 0 0 8px #ffb142; }
            100% { opacity: 0.3; text-shadow: 0 0 0px transparent; }
        }
        .foco-parpadeante {
            animation: parpadeoPulso 2.5s infinite ease-in-out;
            color: #ffb142;
            font-weight: bold;
            display: inline-block;
        }

        /* Paneles cromáticos para la coherencia visual con la identidad de cada átomo */
        .card-dalton { background-color: rgba(144, 164, 174, 0.08); border: 1px solid rgba(144, 164, 174, 0.3); border-left: 5px solid #90a4ae; padding: 20px; border-radius: 6px; margin-bottom: 15px; }
        .card-thomson { background-color: rgba(156, 39, 176, 0.08); border: 1px solid rgba(156, 39, 176, 0.3); border-left: 5px solid #9c27b0; padding: 20px; border-radius: 6px; margin-bottom: 15px; }
        .card-rutherford { background-color: rgba(33, 150, 243, 0.08); border: 1px solid rgba(33, 150, 243, 0.3); border-left: 5px solid #2196f3; padding: 20px; border-radius: 6px; margin-bottom: 15px; }
        .card-bohr { background-color: rgba(255, 177, 66, 0.08); border: 1px solid rgba(255, 177, 66, 0.3); border-left: 5px solid #ffb142; padding: 20px; border-radius: 6px; margin-bottom: 15px; }
        .card-schrodinger { background-color: rgba(0, 229, 255, 0.08); border: 1px solid rgba(0, 229, 255, 0.3); border-left: 5px solid #00e5ff; padding: 20px; border-radius: 6px; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# ========================================================
# 2. CAPA DE SERVICIOS: BASE DE DATOS Y PERSISTENCIA REAL ANTI-F5
# ========================================================
DB_NAME = 'synapsis_auth.db'

def inicializar_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tokens_acceso
                 (token TEXT PRIMARY KEY, 
                  fecha_expiracion DATE, 
                  en_uso BOOLEAN, 
                  identificador_usuario TEXT,
                  modulo_actual INTEGER DEFAULT 1,
                  score_puntos INTEGER DEFAULT 0,
                  memo_completado INTEGER DEFAULT 0)''')
    
    token_prueba = "SYNAPSIS-PRO-2026"
    fecha_futura = datetime.date.today() + timedelta(days=30)
    c.execute("INSERT OR IGNORE INTO tokens_acceso (token, fecha_expiracion, en_uso, identificador_usuario, modulo_actual, score_puntos, memo_completado) VALUES (?, ?, ?, ?, 1, 0, 0)", 
              (token_prueba, fecha_futura, False, "Admin"))
    conn.commit()
    conn.close()

def obtener_datos_usuario(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT score_puntos, memo_completado FROM tokens_acceso WHERE token = ?", (token,))
    res = c.fetchone()
    conn.close()
    return res if res else (0, 0)

def sincronizar_progreso_db(token, puntos, memo_comp):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET score_puntos = ?, memo_completado = ? WHERE token = ?", (puntos, memo_comp, token))
    conn.commit()
    conn.close()

def otorgar_tiempo_extra_db(token, dias=7):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT fecha_expiracion FROM tokens_acceso WHERE token = ?", (token,))
    res = c.fetchone()
    if res:
        fecha_act = datetime.datetime.strptime(res[0], "%Y-%m-%d").date()
        nueva_fecha = fecha_act + timedelta(days=dias)
        c.execute("UPDATE tokens_acceso SET fecha_expiracion = ? WHERE token = ?", (nueva_fecha.strftime("%Y-%m-%d"), token))
        conn.commit()
    conn.close()

def forzar_cancelacion_licencia(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    ayer = datetime.date.today() - timedelta(days=1)
    c.execute("UPDATE tokens_acceso SET fecha_expiracion = ? WHERE token = ?", (ayer.strftime("%Y-%m-%d"), token))
    conn.commit()
    conn.close()

def eliminar_registro_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM tokens_acceso WHERE token = ?", (token,))
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
            return False, "El token ha expirado o fue cancelado por el administrador."
        if en_uso:
            conn.close()
            return False, "Acceso denegado: Token activo en otro dispositivo."
        
        c.execute("UPDATE tokens_acceso SET en_uso = 1 WHERE token = ?", (token_ingresado,))
        conn.commit()
        conn.close()
        return True, "Acceso concedido."
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
        c.execute("INSERT INTO tokens_acceso (token, fecha_expiracion, en_uso, identificador_usuario, modulo_actual, score_puntos, memo_completado) VALUES (?, ?, ?, ?, 1, 0, 0)", 
                  (token.upper(), exp, False, identificador))
        conn.commit()
        mensaje = f"Token {token} registrado con éxito hasta {exp}"
    except sqlite3.IntegrityError:
        mensaje = f"Error: El token ya existe en el servidor."
    conn.close()
    return mensaje

# ========================================================
# 3. MOTORES GRÁFICOS SVG NATIVOS
# ========================================================
def obtener_svg_atomo(modelo_nombre):
    if "Dalton" in modelo_nombre:
        return """
        <svg viewBox="0 0 100 100" width="90" height="90">
            <circle cx="50" cy="50" r="34" fill="none" stroke="#90a4ae" stroke-width="2.5"/>
            <circle cx="50" cy="50" r="31" fill="#90a4ae" opacity="0.15"/>
        </svg>
        """
    elif "Thomson" in modelo_nombre:
        return """
        <svg viewBox="0 0 100 100" width="90" height="90">
            <circle cx="50" cy="50" r="34" fill="#9c27b0" opacity="0.15" stroke="#9c27b0" stroke-width="1.5"/>
            <circle cx="34" cy="38" r="4" fill="#ffffff"/><text x="32" y="41" fill="black" font-size="9" font-weight="bold">-</text>
            <circle cx="66" cy="42" r="4" fill="#ffffff"/><text x="64" y="45" fill="black" font-size="9" font-weight="bold">-</text>
            <circle cx="48" cy="68" r="4" fill="#ffffff"/><text x="46" y="71" fill="black" font-size="9" font-weight="bold">-</text>
            <text x="45" y="54" fill="#9c27b0" font-size="14" font-weight="bold">+</text>
        </svg>
        """
    elif "Rutherford" in modelo_nombre:
        return """
        <svg viewBox="0 0 100 100" width="90" height="90">
            <circle cx="50" cy="50" r="6" fill="#2196f3"/>
            <text x="47" y="54" fill="white" font-size="9" font-weight="bold">+</text>
            <ellipse cx="50" cy="50" rx="38" ry="10" fill="none" stroke="#2196f3" stroke-width="1" opacity="0.6" transform="rotate(30 50 50)"/>
            <ellipse cx="50" cy="50" rx="38" ry="10" fill="none" stroke="#2196f3" stroke-width="1" opacity="0.6" transform="rotate(-30 50 50)"/>
            <circle cx="22" cy="34" r="2.5" fill="#ffffff"/>
            <circle cx="78" cy="66" r="2.5" fill="#ffffff"/>
        </svg>
        """
    elif "Bohr" in modelo_nombre:
        return """
        <svg viewBox="0 0 100 100" width="90" height="90">
            <circle cx="50" cy="50" r="7" fill="#ffb142"/>
            <circle cx="50" cy="50" r="20" fill="none" stroke="#ffb142" stroke-width="1" stroke-dasharray="2 2"/>
            <circle cx="50" cy="50" r="36" fill="none" stroke="#ffb142" stroke-width="1"/>
            <circle cx="50" cy="14" r="3" fill="#ffffff"/>
            <circle cx="68" cy="38" r="3" fill="#ffffff"/>
        </svg>
        """
    else:
        return """
        <svg viewBox="0 0 100 100" width="90" height="90">
            <defs>
                <radialGradient id="cloud" cx="50%" cy="50%" r="50%">
                    <stop offset="0%" stop-color="#00e5ff" stop-opacity="0.8"/>
                    <stop offset="50%" stop-color="#00e5ff" stop-opacity="0.25"/>
                    <stop offset="100%" stop-color="#00e5ff" stop-opacity="0"/>
                </radialGradient>
            </defs>
            <circle cx="50" cy="50" r="38" fill="url(#cloud)"/>
            <circle cx="50" cy="50" r="4" fill="#ffffff"/>
        </svg>
        """

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
        ("Thomson (1897)", 2), ("Esfera positiva con electrones incrustados", 2),
        ("Rutherford (1911)", 3), ("Núcleo denso positivo y espacio vacío", 3),
        ("Bohr (1913)", 4), ("Órbitas circulares planas cuantizadas", 4),
        ("Schrödinger (1926)", 5), ("Orbitales 3D (Flexibilidad cuántica)", 5)
    ]
    random.shuffle(contenido)
    return contenido

# ========================================================
# 4. GESTIÓN DEL ESTADO DE LA SESIÓN
# ========================================================
def inicializar_estado():
    if "auth" not in st.session_state: st.session_state["auth"] = False
    if "token_actual" not in st.session_state: st.session_state["token_actual"] = ""
    if "vidas" not in st.session_state: st.session_state["vidas"] = 3
    if "errores_quiz" not in st.session_state: st.session_state["errores_quiz"] = 0
    if "advertencia_ph" not in st.session_state: st.session_state["advertencia_ph"] = False
    
    if "puntos_acumulados" not in st.session_state: st.session_state["puntos_acumulados"] = 0
    if "racha_consecutiva" not in st.session_state: st.session_state["racha_consecutiva"] = 0
    if "licencia_extendida" not in st.session_state: st.session_state["licencia_extendida"] = False
    
    if "memo_tablero" not in st.session_state: st.session_state["memo_tablero"] = mezclar_memorama()
    if "memo_reveladas" not in st.session_state: st.session_state["memo_reveladas"] = []
    if "memo_resueltas" not in st.session_state: st.session_state["memo_resueltas"] = []
    if "memo_completado" not in st.session_state: st.session_state["memo_completado"] = False

# ========================================================
# 5. CONTROLADOR CENTRAL DE LA INTERFAZ DE USUARIO
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
                
                pts, comp = obtener_datos_usuario(token_limpio)
                st.session_state["puntos_acumulados"] = pts
                if comp == 1:
                    st.session_state["memo_completado"] = True
                    st.session_state["memo_resueltas"] = [1, 2, 3, 4, 5]
                
                st.success(mensaje)
                st.rerun()
            else:
                st.error(f"Error: {mensaje}")
        
        # PANEL DE ADMINISTRACIÓN ROBUSTECIDO CON HERRAMIENTAS AVANZADAS
        with st.expander("⚙️ Panel de Administración (Gestor de Licencias y Tokens)"):
            st.markdown("Consola jerárquica para la creación, liberación o revocación de credenciales.")
            c_admin1, c_admin2 = st.columns(2)
            with c_admin1:
                nuevo_token = st.text_input("Nuevo Token (Ej: ALUMNO-101):").strip().upper()
                dias = st.number_input("Días de vigencia:", min_value=1, value=30)
                if st.button("Crear Suscripción", type="primary", use_container_width=True):
                    if nuevo_token:
                        res = registrar_nuevo_usuario(nuevo_token, dias)
                        st.info(res)
                    else: st.warning("Escribe un token válido.")
            with c_admin2:
                token_bloqueado = st.text_input("Token Objetivo (Gestión/Desbloqueo):").strip().upper()
                c_b1, c_b2, c_b3 = st.columns(3)
                with c_b1:
                    if st.button("🔓 Desbloquear", use_container_width=True):
                        if token_bloqueado:
                            liberar_token(token_bloqueado)
                            st.success("Concurrencia liberada.")
                        else: st.warning("Escribe un token.")
                with c_b2:
                    if st.button("❌ Cancelar", use_container_width=True):
                        if token_bloqueado:
                            forzar_cancelacion_licencia(token_bloqueado)
                            liberar_token(token_bloqueado)
                            st.error("Licencia expirada forzosamente.")
                        else: st.warning("Escribe un token.")
                with c_b3:
                    if st.button("🗑️ Eliminar", use_container_width=True):
                        if token_bloqueado:
                            if token_bloqueado == "SYNAPSIS-PRO-2026":
                                st.error("No puedes eliminar el token raíz.")
                            else:
                                eliminar_registro_token(token_bloqueado)
                                st.error("Fila borrada de SQLite.")
                        else: st.warning("Escribe un token.")

    else:
        with st.sidebar:
            st.markdown(f"**Usuario en línea:** `{st.session_state['token_actual']}`")
            st.markdown(f"**Marcador Global:** `🪙 {st.session_state['puntos_acumulados']} PTS`")
            if st.button("🚪 Cerrar Sesión Segura", use_container_width=True):
                liberar_token(st.session_state["token_actual"])
                st.session_state["auth"] = False
                st.session_state["token_actual"] = ""
                st.rerun()
            st.markdown("---")
            st.caption("Cerrar sesión explícitamente libera la concurrencia en SQLite.")

        _, c_vid = st.columns([3, 1])
        with c_vid:
            st.markdown(f"<div class='monitor-box'><span style='color:#90a4ae; font-size:12px;'>ESTABILIDAD CELULAR</span><br><b style='font-size:20px; color:#f44336;'>{st.session_state.vidas} / 3 💔</b></div>", unsafe_allow_html=True)

        if st.session_state.vidas <= 0:
            st.error("🚨 COLAPSO METABÓLICO: Lisis celular detectada por acumulación de fallos.")
            if st.button("Reiniciar Simulador"):
                st.session_state.vidas = 3
                st.session_state.advertencia_ph = False
                st.session_state.errores_quiz = 0
                st.rerun()
            return

        # ========================================================
        # ARQUITECTURA DE MACRO-MÓDULOS DE NAVEGACIÓN
        # ========================================================
        tabs = st.tabs(["🏛️ Módulo 1", "⚡ Módulo 2", "🧬 Módulo 3", "🌡️ Módulo 4", "🍬 Módulo 5", "🏆 Examen"])

        # ========================================================
        # MÓDULO 1: FUNDAMENTOS DE QUÍMICA BIOLÓGICA (UNIDAD 1 UNAM)
        # ========================================================
        with tabs[0]:
            st.markdown("<h2 style='color:#00e5ff; margin-top:0;'>Módulo 1: Fundamentos de Química Biológica</h2>", unsafe_allow_html=True)
            
            # SUB-NAVEGADOR MEJORADO CON ESTILOS VISUALES DE BOTONERA INDEPENDIENTE (CSS)
            estacion_actual = st.radio(
                "Selecciona una Estación de Trabajo FMVZ:",
                options=[
                    "⚛️ Estación A: Estructura y Enlaces",
                    "💧 Estación B: Fuerzas del Agua",
                    "🧬 Estación C: Grupos Funcionales",
                    "🩸 Estación D: pH y Buffers respiratorios"
                ],
                horizontal=True,
                label_visibility="collapsed"
            )
            st.markdown("---")

            # ----------------------------------------------------
            # ESTACIÓN A: ESTRUCTURA Y ENLACES QUÍMICOS
            # ----------------------------------------------------
            if "Estación A" in estacion_actual:
                st.markdown("### Línea del Tiempo Atómica y Enlaces Químicos")
                st.markdown("""
                <span class='foco-parpadeante'>💡</span> <i>Deslice la línea del tiempo horizontal para descubrir la evolución del átomo.</i>
                """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                
                modelo = st.select_slider(
                    "Navegación Cronológica:",
                    options=["Dalton (1810)", "Thomson (1897)", "Rutherford (1911)", "Bohr (1913)", "Schrödinger (1926)"],
                    label_visibility="collapsed"
                )
                
                col_txt, col_svg = st.columns([3, 1])
                with col_txt:
                    if "Dalton" in modelo:
                        st.markdown("""
                        <div class='card-dalton'>
                            <b style='color:#90a4ae; font-size: 1.2rem;'>Modelo de Dalton (1810) — Átomo Indivisible</b><br><br>
                            • <b>Principio:</b> El átomo es una esfera sólida sin cargas. Explica la conservación de la masa en proporciones fijas.<br>
                            • <b>Límite en Bioquímica:</b> Al carecer de electrones y cargas eléctricas, es incapaz de explicar la unión química.
                        </div>
                        """, unsafe_allow_html=True)
                    elif "Thomson" in modelo:
                        st.markdown("""
                        <div class='card-thomson'>
                            <b style='color:#9c27b0; font-size: 1.2rem;'>Modelo de Thomson (1897) — El Electrón</b><br><br>
                            • <b>Principio:</b> Descubre el electrón. Concibe el átomo como una masa esférica positiva atascada de cargas negativas.<br>
                            • <b>Aporte Molecular:</b> Introduce la naturaleza eléctrica, revelando el origen de las interacciones químicas.
                        </div>
                        """, unsafe_allow_html=True)
                    elif "Rutherford" in modelo:
                        st.markdown("""
                        <div class='card-rutherford'>
                            <b style='color:#2196f3; font-size: 1.2rem;'>Modelo de Rutherford (1911) — El Espacio Vacío</b><br><br>
                            • <b>Principio:</b> Demuestra un núcleo central denso positivo con electrones orbitando en un inmenso espacio vacío.<br>
                            • <b>Aporte Molecular:</b> Posiciona a los electrones en la periferia libres para interactuar, ser robados o compartidos.
                        </div>
                        """, unsafe_allow_html=True)
                    elif "Bohr" in modelo:
                        st.markdown("""
                        <div class='card-bohr'>
                            <b style='color:#ffb142; font-size: 1.2rem;'>Modelo de Bohr (1913) — Órbitas Cuantizadas</b><br><br>
                            • <b>Principio:</b> Los electrones giran en órbitas circulares y estables con niveles de energía definidos.<br>
                            • <b>Límite en Bioquímica:</b> Su rigidez bidimensional impide deducir los ángulos tridimensionales de las moléculas orgánicas.
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class='card-schrodinger'>
                            <b style='color:#00e5ff; font-size: 1.2rem;'>Modelo de Schrödinger (1926) — Mecánica Cuántica (Eje Estructural)</b><br><br>
                            • <b>Principio:</b> Sustituye órbitas rígidas por <b>orbitales</b>: nubes probabilísticas tridimensionales de electrones.<br><br>
                            <b>¿Por qué define a la bioquímica moderna?</b><br>
                            Demuestra que los enlaces son nubes electrónicas flexibles que se hibridan y deforman. Esto justifica matemáticamente la geometría angular exacta del agua en 'V', las uniones débiles que estabilizan la doble hélice del ADN y el acoplamiento tridimensional preciso de los sitios activos de las enzimas.
                        </div>
                        """, unsafe_allow_html=True)
                
                with col_svg:
                    st.components.v1.html(f"""
                    <div style='display:flex; justify-content:center; align-items:center; width:100%; height:110px; background-color:rgba(255,255,255,0.02); border-radius:8px;'>
                        {obtener_svg_atomo(modelo)}
                    </div>
                    """, height=120, scrolling=False)

                st.markdown("---")
                st.markdown("### 🧬 Pon a prueba tu Bitácora Atómica")
                if st.session_state["memo_completado"]:
                    st.caption("✨ *Modo Práctica Activo: Avance oficial sellado en el servidor. Repasa libremente.*")
                else:
                    st.caption("🔥 *Modo Oficial Activo: Consigue una racha de 2 aciertos consecutivos sin errores para ganar puntos y extender tu licencia.*")

                if len(st.session_state["memo_reveladas"]) == 2:
                    idx1, idx2 = st.session_state["memo_reveladas"]
                    val1, id_par1 = st.session_state["memo_tablero"][idx1]
                    val2, id_par2 = st.session_state["memo_tablero"][idx2]
                    
                    if id_par1 == id_par2:
                        if id_par1 not in st.session_state["memo_resueltas"]:
                            st.session_state["memo_resueltas"].append(id_par1)
                            if not st.session_state["memo_completado"]:
                                st.session_state["racha_consecutiva"] += 1
                                puntos_ganados = 100
                                if st.session_state["racha_consecutiva"] >= 2 and not st.session_state["licencia_extendida"]:
                                    puntos_ganados += 300
                                    st.session_state["licencia_extendida"] = True
                                    otorgar_tiempo_extra_db(st.session_state["token_actual"], dias=7)
                                    st.toast("🚀 ¡RACHA CUÁNTICA! +7 días de licencia extra.", icon="🎁")
                                st.session_state["puntos_acumulados"] += puntos_ganados
                                sincronizar_progreso_db(st.session_state["token_actual"], st.session_state["puntos_acumulados"], 0)
                        st.toast("⚡ ¡Afinidad molecular correcta!", icon="✅")
                    else:
                        st.session_state["racha_consecutiva"] = 0
                        st.toast("❌ Los modelos no interactúan.", icon="⚠️")
                    st.session_state["memo_reveladas"] = []

                if len(st.session_state["memo_resueltas"]) == 5 and not st.session_state["memo_completado"]:
                    st.session_state["memo_completado"] = True
                    sincronizar_progreso_db(st.session_state["token_actual"], st.session_state["puntos_acumulados"], 1)

                cols_memo = st.columns(5)
                for i in range(10):
                    col_idx = i % 5
                    with cols_memo[col_idx]:
                        val_tarjeta, id_par = st.session_state["memo_tablero"][i]
                        if id_par in st.session_state["memo_resueltas"]:
                            label = f"✅ {val_tarjeta}"
                            deshabilitado = True
                        elif i in st.session_state["memo_reveladas"]:
                            label = f"👀 {val_tarjeta}"
                            deshabilitado = True
                        else:
                            label = "⚛️ Revelar"
                            deshabilitado = False
                        if st.button(label, key=f"btn_memo_{i}", use_container_width=True, disabled=deshabilitado):
                            st.session_state["memo_reveladas"].append(i)
                            st.rerun()

                st.markdown("<br>", unsafe_allow_html=True)
                c_reset, _ = st.columns([1, 3])
                with c_reset:
                    if st.button("🔄 Reiniciar Memorama", use_container_width=True):
                        st.session_state["memo_tablero"] = mezclar_memorama()
                        st.session_state["memo_reveladas"] = []
                        st.session_state["memo_resueltas"] = []
                        if not st.session_state["memo_completado"]:
                            st.session_state["racha_consecutiva"] = 0
                        st.rerun()

                if st.session_state["memo_completado"]:
                    st.markdown(f"<div class='card-success'>🏆 <b>¡Afinidad Atómica Consolidada!</b> Avance sellado de forma permanente en el servidor. Tu balance global actual es de: <b>{st.session_state['puntos_acumulados']} PTS</b>.</div>", unsafe_allow_html=True)

            # ----------------------------------------------------
            # ESTACIÓN B: FUERZAS DEL AGUA Y SOLUBILIDAD
            # ----------------------------------------------------
            elif "Estación B" in estacion_actual:
                st.markdown("### Fuerzas Intermoleculares y Solubilidad")
                st.info("""
                **Puentes de Hidrógeno e Interacciones de Van der Waals (Temas 1.3 y 1.6)**
                * **Fuerzas Cohesivas:** El enlace por puente de hidrógeno es una fuerza dipolo-dipolo extrema que une las moléculas de agua, dotándola de su alto calor específico.
                * **Fuerzas de Van der Waals:** Incluyen las fuerzas de dispersión de London (dipolos inducidos transitorios) y dipolo-dipolo inducido, esenciales para la estabilización interna de proteínas y membranas.
                * **Interacciones Hidrofóbicas:** Explicación termodinámica de cómo el agua repele las cadenas hidrocarbonadas apolares, forzando la autoorganización de los lípidos en micelas y bicapas lipídicas celulares.
                """)
                
                st.markdown("#### 🧪 Calculadora de Disoluciones Molares (Tema 1.7)")
                st.write("Simula la preparación de soluciones de reactivos variando la masa del soluto y el volumen de solvente.")
                g_soluto = st.number_input("Masa de Soluto (g):", min_value=1.0, value=18.0)
                vol_l = st.slider("Volumen de la Disolución (L):", 0.1, 5.0, 1.0, 0.1)
                pm_glucosa = 180.15 # Peso molecular de referencia
                molaridad = (g_soluto / pm_glucosa) / vol_l
                st.success(f"Concentración Calculada: **{molaridad:.3f} M** (Mol/L) considerando Glucosa como soluto patrón.")

            # ----------------------------------------------------
            # ESTACIÓN C: UNIVERSO DE GRUPOS FUNCIONALES
            # ----------------------------------------------------
            elif "Estación C" in estacion_actual:
                st.markdown("### Estructura de los Grupos Funcionales y Estereoquímica (Temas 1.4 y 1.5)")
                st.write("Selecciona cualquier grupo funcional constituyente de las macromoléculas animales para desplegar su relevancia biológica en medicina veterinaria:")
                
                grupo = st.selectbox("Grupo Funcional a Inspeccionar:", [
                    "Carbonilo (C=O)", "Metilo (CH3)", "Hidroxilo (-OH)", "Éster (-COOR)", 
                    "Amino (-NH2)", "Carboxilo (-COOH)", "Tiol / Disulfuro (-SH / -S-S-)", "Fosforilo (-PO3 2-)"
                ])
                
                if "Carbonilo" in group:
                    st.warning("**Carbonilo:** Presente en aldehídos y cetonas. Eje reactivo en los azúcares reductores que se estudian en el metabolismo energético.")
                elif "Metilo" in grupo:
                    st.warning("**Metilo:** Grupo apolar. Crítico en las modificaciones epigenéticas del ADN celular (metilación) y en la hidrofobicidad proteica.")
                elif "Hidroxilo" in grupo:
                    st.warning("**Hidroxilo:** Confiere solubilidad extrema en agua a través de puentes de hidrógeno. Abundante en alcoholes y carbohidratos.")
                elif "Tiol" in grupo:
                    st.warning("**Tiol y Disulfuro:** Los puentes de disulfuro entre residuos de Cisteína aportan rigidez estructural tridimensional masiva a las proteínas extracelulares como la queratina (pelo, cuernos, pezuñas).")
                elif "Fosforilo" in grupo:
                    st.warning("**Fosforilo:** Enlace de alta energía química. Moneda de intercambio de energía universal en el organismo animal (ATP) y pilar en los ácidos nucleicos.")
                else:
                    st.warning("Grupo funcional de alta frecuencia en aminoácidos y metabolitos primarios de la homeostasis orgánica.")
                
                st.markdown("---")
                st.markdown("#### 🧬 Breviario de Estereoquímica (Tema 1.5)")
                st.write("La orientación espacial define la vida: Los aminoácidos naturales en los mamíferos domésticos pertenecen exclusivamente a la serie **L**, mientras que los carbohidratos asimilables corresponden a la serie **D**. La alteración tridimensional de un fármaco quiral puede volverlo ineficaz o tóxico.")

            # ----------------------------------------------------
            # ESTACIÓN D: PH Y SISTEMAS AMORTIGUADORES RESPIRATORIOS
            # ----------------------------------------------------
            else:
                st.markdown("### Autoionización del Agua, Escala de pH y Amortiguadores (Temas 1.8, 1.9 y 1.10)")
                st.write("El control del pH es una constante biológica inalterable para las enzimas del plasma animal.")
                
                solucion = st.radio("Cámara de Perfusión Sanguínea:", ["Plasma con Amortiguador Bicarbonato (pH 7.4)", "Agua Destilada Pura (pH 7.0)"])
                if st.button("Inyectar 10 mL de Ácido Clorhídrico (HCl)", use_container_width=True):
                    if "Agua" in solucion:
                        if not st.session_state.advertencia_ph:
                            st.markdown("<div class='card-hint'>💡 <b>SISTEMA DE ASISTENCIA:</b> El agua carece de amortiguadores. Si continúas, causarás un colapso por acidosis masiva. Vuelve a presionar para confirmar la acción.</div>", unsafe_allow_html=True)
                            st.session_state.advertencia_ph = True
                        else:
                            st.markdown("<div class='card-error'>🩸 <b>CHOQUE DE ACIDOSIS:</b> El pH del agua cayó a 2.0. Desnaturalización masiva de proteínas. <b>-1 Vida.</b></div>", unsafe_allow_html=True)
                            st.session_state.vidas -= 1
                            st.session_state.advertencia_ph = False
                    else:
                        st.markdown("<div class='card-success'>🛡️ <b>TAMPONAMIENTO EXITOSO:</b> El sistema amortiguador fisiológico contuvo el impacto. El exceso de protones reaccionó con el Bicarbonato ($HCO_3^-$) formando Ácido Carbónico ($H_2CO_3$), eliminable como $CO_2$ en los pulmones.</div>", unsafe_allow_html=True)
                        st.session_state.advertencia_ph = False

        # ========================================================
        # MÓDULO 2: ELECTRONEGATIVIDAD
        # ========================================================
        with tabs[1]:
            st.markdown("<h2 style='color:#00e5ff; margin-top:0;'>Módulo 2: Electronegatividad (Estira y Afloja)</h2>", unsafe_allow_html=True)
            fuerza = st.slider("Fuerza de Atracción (Escala Pauling):", 0.7, 4.0, 2.2, 0.1)
            st.components.v1.html(generar_svg_tira_afloja(fuerza), height=120, scrolling=False)
            if fuerza >= 3.0: st.markdown("<div class='card-error'><b>🔥 Átomo Altamente Electronegativo:</b> Secuestra la densidad electrónica.</div>", unsafe_allow_html=True)
            else: st.markdown("<div class='card-success'><b>🤝 Átomo Equilibrado:</b> Comparte electrones de forma justa.</div>", unsafe_allow_html=True)

        # ========================================================
        # MÓDULO 3: REACTORES DE ENLACE BIOQUÍMICO
        # ========================================================
        with tabs[2]:
            st.markdown("<h2 style='color:#00e5ff; margin-top:0;'>Módulo 3: Reactores de Enlace Bioquímico</h2>", unsafe_allow_html=True)
            col_a1, col_a2 = st.columns(2)
            atom1 = col_a1.selectbox("Átomo Central (A):", list(ELEMENTOS.keys()))
            atom2 = col_a2.selectbox("Átomo de Reacción (B):", list(ELEMENTOS.keys()))
            if st.button("Ensamblar y Analizar Enlace", use_container_width=True):
                a1, a2 = ELEMENTOS[atom1], ELEMENTOS[atom2]
                st.components.v1.html(generar_svg_enlace(a1['sym'], a1['fuerza'], a1['color'], a2['sym'], a2['fuerza'], a2['color']), height=140, scrolling=False)
                diff = abs(a1['fuerza'] - a2['fuerza'])
                if diff == 0: st.markdown(f"<div class='card-success'>... Enlace Covalente No Polar Puro (Diferencia = 0.0).</div>", unsafe_allow_html=True)
                elif diff <= 0.4: st.markdown(f"<div class='card-success'>... Enlace Covalente No Polar.</div>", unsafe_allow_html=True)
                elif diff <= 1.7: st.markdown(f"<div class='card-success' style='border-left-color:#ffb142;'>⚡ Enlace Covalente Polar (Dipolo activo).</div>", unsafe_allow_html=True)
                else: st.markdown("<div class='card-error'>⚠️ Tensión Iónica Crítica.</div>", unsafe_allow_html=True)

        # ========================================================
        # MÓDULO 4: EQUILIBRIO ÁCIDO-BASE Y PH
        # ========================================================
        with tabs[3]:
            st.markdown("<h2 style='color:#00e5ff; margin-top:0;'>Módulo 4: Equilibrio Ácido-Base y pH</h2>", unsafe_allow_html=True)
            solucion_tab4 = st.radio("Cámara de Perfusión Secundaria:", ["Medio A: Plasma con Buffer Bicarbonato", "Medio B: Agua Destilada Pura"])
            if st.button("Inyectar 10 mL de HCl (Módulo 4)", use_container_width=True):
                if "Agua" in solucion_tab4:
                    st.markdown("<div class='card-error'>🩸 pH colapsado instantáneamente en el Módulo 4.</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='card-success'>🛡️ Tamponamiento exitoso.</div>", unsafe_allow_html=True)

        # ========================================================
        # MÓDULO 5: GLUCÓMICA E ISOMERISMO
        # ========================================================
        with tabs[4]:
            st.markdown("<h2 style='color:#00e5ff; margin-top:0;'>Módulo 5: Glucómica e Isomerismo</h2>", unsafe_allow_html=True)
            col_g1, col_g2 = st.columns(2)
            azu1 = col_g1.selectbox("Monosacárido 1:", ["Alfa-D-Glucosa", "Beta-D-Galactosa"])
            azu2 = col_g2.selectbox("Monosacárido 2:", ["Alfa-D-Glucosa", "Beta-D-Fructosa (Cetosa)"])
            if st.button("Polimerizar Enlace Glucosídico", use_container_width=True):
                if azu1 == "Alfa-D-Glucosa" and azu2 == "Alfa-D-Glucosa": st.markdown("<div class='card-success'>🌾 <b>MALTOSA SINTETIZADA:</b> Enlace Alfa(1→4).</div>", unsafe_allow_html=True)
                elif azu1 == "Beta-D-Galactosa" and azu2 == "Alfa-D-Glucosa": st.markdown("<div class='card-success'>🥛 <b>LACTOSA SINTETIZADA:</b> Enlace Beta(1→4).</div>", unsafe_allow_html=True)
                elif azu1 == "Alfa-D-Glucosa" and azu2 == "Beta-D-Fructosa (Cetosa)": st.markdown("<div class='card-success'>🎋 <b>SACAROSA SINTETIZADA:</b> Enlace Alfa(1) ↔ Beta(2). Non-reducing.</div>", unsafe_allow_html=True)
                else: st.markdown("<div class='card-error'>⚠️ Ensamblaje de baja prioridad metabólica.</div>", unsafe_allow_html=True)

        # ========================================================
        # MÓDULO 6: EVALUACIÓN FINAL
        # ========================================================
        with tabs[5]:
            st.markdown("<h2 style='color:#00e5ff; margin-top:0;'>Módulo 6: Evaluación Final</h2>", unsafe_allow_html=True)
            Q1 = st.radio("1. ¿Por qué la evolución optó por la D-Glucosa sobre la L-Glucosa?", ["A) Desvía la luz a la derecha.", "B) Modelo 'llave y cerradura' en los sitios activos enzimáticos.", "C) Carece de enlaces O-Glucosídicos."], index=None)
            Q2 = st.radio("2. Glucosa y Galactosa difieren estructuralmente en un solo carbono asimétrico (C4), son:", ["A) Isótopos", "B) Epímeros", "C) Enantiómeros"], index=None)
            if st.button("Evaluar Bitácora de Laboratorio", use_container_width=True):
                errores = 0
                if Q1 and "B)" not in Q1: errores += 1
                if Q2 and "B)" not in Q2: errores += 1
                if not Q1 or not Q2: st.warning("Responde todas las interrogantes.")
                elif errores == 0:
                    st.balloons()
                    st.success("🏆 **¡RÉCORD PERFECTO!** Dominio total de la materia.")
                else:
                    st.session_state.errores_quiz += 1
                    if st.session_state.errores_quiz == 1: st.markdown(f"<div class='card-hint'>💡 Tienes {errores} error(es). La variación en un único carbono define a un epímero. Corrige sin penalización.</div>", unsafe_allow_html=True)
                    else:
                        st.session_state.vidas -= 1
                        st.error("❌ Fallo Crítico. Se ha restado 1 Vida.")
                        st.session_state.errores_quiz = 0

if __name__ == "__main__":
    main()
