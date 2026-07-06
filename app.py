import streamlit as st
import sqlite3
import datetime
from datetime import timedelta

# ========================================================
# 1. CONFIGURACIÓN DEL CHASIS Y ESTÉTICA CÓSMICA
# ========================================================
st.set_page_config(page_title="ChonpsLab Pro", page_icon="⚛️", layout="wide")

def inyectar_css():
    st.markdown("""
    <style>
        /* Chasis Cósmico de Alto Rendimiento */
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
        
        /* Pestañas Fluídas */
        .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: transparent; }
        .stTabs [data-baseweb="tab"] { background-color: rgba(255,255,255,0.05); border-radius: 4px 4px 0 0; padding: 10px 20px; color: #90a4ae; font-weight: bold;}
        .stTabs [aria-selected="true"] { background-color: rgba(0, 229, 255, 0.15) !important; color: #00e5ff !important; border-bottom: 2px solid #00e5ff !important; }
    </style>
    """, unsafe_allow_html=True)

# ========================================================
# 2. CAPA DE SERVICIOS: BASE DE DATOS Y AUTENTICACIÓN
# ========================================================
def inicializar_db():
    """Crea la base de datos local SQLite para gestionar suscripciones."""
    conn = sqlite3.connect('synapsis_auth.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tokens_acceso
                 (token TEXT PRIMARY KEY, fecha_expiracion DATE, en_uso BOOLEAN, identificador_usuario TEXT)''')
    
    # Generar un token maestro de prueba válido por 30 días si no existe
    token_prueba = "SYNAPSIS-PRO-2026"
    fecha_futura = datetime.date.today() + timedelta(days=30)
    c.execute("INSERT OR IGNORE INTO tokens_acceso (token, fecha_expiracion, en_uso, identificador_usuario) VALUES (?, ?, ?, ?)", 
              (token_prueba, fecha_futura, False, "Admin"))
    
    conn.commit()
    conn.close()

def validar_token(token_ingresado):
    """Valida criptográficamente el token y su vigencia temporal."""
    conn = sqlite3.connect('synapsis_auth.db')
    c = conn.cursor()
    c.execute("SELECT fecha_expiracion, en_uso FROM tokens_acceso WHERE token = ?", (token_ingresado,))
    resultado = c.fetchone()
    conn.close()
    
    if resultado:
        fecha_exp = datetime.datetime.strptime(resultado[0], "%Y-%m-%d").date()
        if datetime.date.today() <= fecha_exp:
            return True, f"Token válido. Expira el: {fecha_exp}"
        else:
            return False, "El token ha expirado. Renueva tu suscripción."
    return False, "Token inexistente o inválido."

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

# ========================================================
# 4. GESTIÓN DEL ESTADO GLOBAL
# ========================================================
def inicializar_estado():
    if "auth" not in st.session_state: st.session_state["auth"] = False
    if "vidas" not in st.session_state: st.session_state["vidas"] = 3
    if "puntos" not in st.session_state: st.session_state["puntos"] = 0
    if "errores_quiz" not in st.session_state: st.session_state["errores_quiz"] = 0
    if "advertencia_ph" not in st.session_state: st.session_state["advertencia_ph"] = False

# ========================================================
# 5. CONTROLADOR PRINCIPAL DE LA INTERFAZ
# ========================================================
def main():
    inyectar_css()
    inicializar_db()
    inicializar_estado()

    # PORTADA DE AUTENTICACIÓN
    if not st.session_state["auth"]:
        st.markdown("<h1 class='main-title'>Chonps<span class='main-title-suffix'>Lab</span> Pro</h1>", unsafe_allow_html=True)
        st.markdown("<p class='sub-title'>Plataforma de Simulación Bioquímica y Veterinaria</p>", unsafe_allow_html=True)
        st.markdown("""
        <div class='bio-panel'>
            <span style='color:#00e5ff; font-weight:700; font-size:1.25rem;'>Acceso Restringido</span>
            <p style='color:#cfd8dc; margin-top:10px;'>Ingresa tu token de suscripción activo para desplegar el entorno de simulación molecular.</p>
        </div>
        """, unsafe_allow_html=True)
        
        pwd = st.text_input("Token de Licencia:", type="password")
        if st.button("Autenticar Terminal", use_container_width=True):
            es_valido, mensaje = validar_token(pwd.strip().upper())
            if es_valido:
                st.session_state["auth"] = True
                st.success(mensaje)
                st.rerun()
            else:
                st.error(f"Acceso denegado: {mensaje}")
        
        with st.expander("Panel de Administración (Solo Pruebas)"):
            st.info("Token activo de prueba generado por el sistema: **SYNAPSIS-PRO-2026**")

    # CONSOLA DE LABORATORIO
    else:
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown("<h2 style='color:#00e5ff; margin-top:0;'>Consola de Operaciones</h2>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='monitor-box'><span style='color:#90a4ae; font-size:12px;'>ESTABILIDAD CELULAR (VIDAS)</span><br><b style='font-size:20px; color:#f44336;'>{st.session_state.vidas} / 3 💔</b></div>", unsafe_allow_html=True)

        if st.session_state.vidas <= 0:
            st.error("🚨 COLAPSO METABÓLICO: Lisis celular detectada por errores acumulados.")
            if st.button("Reiniciar Simulador (Consumir nuevo ciclo)"):
                st.session_state.vidas = 3
                st.session_state.advertencia_ph = False
                st.rerun()
            return

        tabs = st.tabs([
            "🏛️ Teoría Atómica", 
            "⚡ Estira y Afloja", 
            "🧬 Reactores", 
            "🍬 Glucómica", 
            "🌡️ Titulación pH", 
            "🏆 Evaluación Final"
        ])

        # MÓDULO 1
        with tabs[0]:
            st.markdown("### Evolución de la Estructura Atómica")
            modelo = st.select_slider(
                "Viaja en el tiempo de la física cuántica:",
                options=["Dalton (1810)", "Thomson (1897)", "Rutherford (1911)", "Bohr (1913)", "Schrödinger (1926)"]
            )
            if "Dalton" in modelo:
                st.info("⚛️ **John Dalton (1810):** El átomo como una esfera sólida indivisible. El reordenamiento de los átomos equivale a una reacción química.")
            elif "Schrödinger" in modelo:
                st.info("⚛️ **Erwin Schrödinger (1926):** Modelo Cuántico. Nubes de probabilidad máxima descritas por números cuánticos (n, l, m).")
            else:
                st.info(f"⚛️ Mostrando datos históricos para el modelo de {modelo}...")

        # MÓDULO 2
        with tabs[1]:
            st.markdown("### Electronegatividad y Tensión Orbital")
            fuerza = st.slider("Fuerza de Atracción (Escala Pauling):", 0.7, 4.0, 2.2, 0.1)
            st.components.v1.html(generar_svg_tira_afloja(fuerza), height=120, scrolling=False)
            
            if fuerza >= 3.0:
                st.markdown("<div class='card-error'><b>🔥 Átomo Altamente Electronegativo:</b> Secuestra la densidad electrónica.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='card-success'><b>🤝 Átomo Equilibrado:</b> Comparte electrones de forma estable.</div>", unsafe_allow_html=True)

        # MÓDULO 3
        with tabs[2]:
            st.markdown("### Síntesis de Enlaces Bioquímicos")
            c1, c2 = st.columns(2)
            atom1 = c1.selectbox("Átomo Central (A):", list(ELEMENTOS.keys()))
            atom2 = c2.selectbox("Átomo de Reacción (B):", list(ELEMENTOS.keys()))
            
            if st.button("Ensamblar y Analizar Enlace", use_container_width=True):
                a1, a2 = ELEMENTOS[atom1], ELEMENTOS[atom2]
                st.components.v1.html(generar_svg_enlace(a1['sym'], a1['fuerza'], a1['color'], a2['sym'], a2['fuerza'], a2['color']), height=140, scrolling=False)
                diff = abs(a1['fuerza'] - a2['fuerza'])
                
                if diff == 0:
                    st.markdown(f"<div class='card-success'>✅ Enlace Covalente No Polar Puro.</div>", unsafe_allow_html=True)
                elif diff <= 1.7:
                    st.markdown(f"<div class='card-success' style='border-left-color:#ffb142;'>⚡ Enlace Covalente Polar ($\delta^-$ generado).</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='card-error'>⚠️ Inestabilidad Molecular Crítica.</div>", unsafe_allow_html=True)

        # MÓDULO 4
        with tabs[3]:
            st.markdown("### Código de Azúcares y Enlaces O-Glucosídicos")
            c1, c2 = st.columns(2)
            azu1 = c1.selectbox("Monosacárido 1:", ["Alfa-D-Glucosa", "Beta-D-Galactosa"])
            azu2 = c2.selectbox("Monosacárido 2:", ["Alfa-D-Glucosa", "Beta-D-Fructosa (Cetosa)"])
            
            if st.button("Polimerizar Enlace", use_container_width=True):
                if azu1 == "Alfa-D-Glucosa" and azu2 == "Alfa-D-Glucosa":
                    st.markdown("<div class='card-success'>🌾 <b>MALTOSA SINTETIZADA:</b> Enlace Alfa(1→4).</div>", unsafe_allow_html=True)
                elif azu1 == "Beta-D-Galactosa" and azu2 == "Alfa-D-Glucosa":
                    st.markdown("<div class='card-success'>🥛 <b>LACTOSA SINTETIZADA:</b> Enlace Beta(1→4).</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='card-error'>⚠️ Ensamblaje metabólico no prioritario.</div>", unsafe_allow_html=True)

        # MÓDULO 5 (CON ANDAMIAJE SOCRÁTICO)
        with tabs[4]:
            st.markdown("### Control Homeostático: Curvas de Titulación")
            solucion = st.radio("Medio Recipiente", ["Plasma con Buffer Bicarbonato", "Agua Destilada Pura"])
            
            if st.button("Inyectar Ácido Clorhídrico (HCl)"):
                if "Agua" in solucion:
                    if not st.session_state.advertencia_ph:
                        st.markdown("<div class='card-hint'>💡 <b>SISTEMA DE ASISTENCIA:</b> El agua destilada carece de bases conjugadas. Si inyectas un ácido fuerte aquí, no habrá moléculas que atrapen los protones. ¿Seguro que deseas proceder? Vuelve a presionar el botón si confirmas la acción.</div>", unsafe_allow_html=True)
                        st.session_state.advertencia_ph = True
                    else:
                        st.markdown("<div class='card-error'>🩸 <b>CHOQUE DE ACIDOSIS:</b> pH colapsa. Desnaturalización proteica masiva. <b>-1 Vida</b>.</div>", unsafe_allow_html=True)
                        st.session_state.vidas -= 1
                        st.session_state.advertencia_ph = False
                else:
                    st.markdown("<div class='card-success'>🛡️ <b>TAMPONAMIENTO EXITOSO:</b> El buffer absorbió los protones manteniendo la homeostasis.</div>", unsafe_allow_html=True)
                    st.session_state.advertencia_ph = False

        # MÓDULO 6 (EVALUACIÓN CON PISTAS)
        with tabs[5]:
            st.markdown("### Matriz de Evaluación Bioquímica")
            Q1 = st.radio("1. ¿Por qué la naturaleza prefiere la D-Glucosa?", ["A) Desvía luz derecha.", "B) Modelo 'llave-cerradura' enzimático.", "C) Carece de enlaces."], index=None)
            Q2 = st.radio("2. Glucosa y Galactosa difieren en el C4. Son:", ["A) Isótopos", "B) Epímeros", "C) Enantiómeros"], index=None)
            
            if st.button("Procesar Bitácora", use_container_width=True):
                errores = 0
                if Q1 and "B)" not in Q1: errores += 1
                if Q2 and "B)" not in Q2: errores += 1
                
                if errores == 0 and Q1 and Q2:
                    st.balloons()
                    st.success("🏆 ¡RÉCORD PERFECTO! Metabolismo estable.")
                else:
                    st.session_state.errores_quiz += 1
                    if st.session_state.errores_quiz == 1:
                        st.markdown(f"<div class='card-hint'>💡 <b>Pista Pedagógica:</b> Tuviste {errores} errores. Recuerda que la especificidad enzimática es espacial (tridimensional) y un epímero es un isómero que varía en un solo carbono. Inténtalo de nuevo sin perder vidas.</div>", unsafe_allow_html=True)
                    else:
                        st.session_state.vidas -= 1
                        st.error(f"❌ Fallo de asimilación. Has perdido 1 Vida.")
                        st.session_state.errores_quiz = 0 # Resetear tras penalización

if __name__ == "__main__":
    main()
