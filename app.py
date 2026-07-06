import streamlit as st
import time

# 1. CONFIGURACIÓN DEL ENTORNO DE SIMULACIÓN NATIVA
st.set_page_config(page_title="ChonpsLab Pro", page_icon="⚛️", layout="wide")

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
    {"id": 1, "pregunta": "1. [LÍPIDOS] Las cadenas de ácidos grasos (C-H) tienen diferencia < 0.4. ¿Propiedad resultante?", "opciones": ["Polares", "Apolares/Hidrofóbicos"], "correcta": "Apolares/Hidrofóbicos", "retro_ok": "¡Correcto! Al no haber dipolos significativos, las colas interactúan por fuerzas de Van der Waals, ideal para formar el núcleo hidrofóbico de las membranas celulares.", "retro_error": "Pista: Piensa en la simetría de la distribución electrónica. Si la diferencia es casi nula, ¿habrá afinidad por el agua?"},
    {"id": 2, "pregunta": "2. [PROTEÍNAS] Enlace Peptídico (C-N). ¿Cómo se distribuye la densidad electrónica?", "opciones": ["Polar (Dipolo)", "Apolar"], "correcta": "Polar (Dipolo)", "retro_ok": "Excelente. El nitrógeno atrae con mayor fuerza los electrones, generando un dipolo crucial para la formación de puentes de hidrógeno secundarios.", "retro_error": "Pista: Compara los valores de electronegatividad del Carbono y el Nitrógeno en tu Reactor. Uno de ellos atrae con más fuerza."},
    {"id": 3, "pregunta": "3. [ADN] Enlaces Fósforo-Oxígeno (Diff 1.25). ¿Característica?", "opciones": ["Polares/Alta Energía", "Apolares"], "correcta": "Polares/Alta Energía", "retro_ok": "Correcto. La fuerte polarización genera una tensión de repulsión ideal para el almacenamiento e intercambio energético en el ATP.", "retro_error": "Pista: Una diferencia de 1.25 es sumamente alta. Esto desplaza los electrones drásticamente hacia el elemento más fuerte."},
    {"id": 4, "pregunta": "4. [CARBOHIDRATOS] ¿Por qué la glucosa es soluble en agua?", "opciones": ["Por enlaces O-H polares", "Por ser apolar"], "correcta": "Por enlaces O-H polares", "retro_ok": "¡Exacto! Los múltiples grupos hidroxilo (-OH) permiten interactuar directamente con la red de puentes de hidrógeno del agua.", "retro_error": "Pista: Recuerda la regla universal de solubilidad: 'Lo semejante disuelve a lo semejante'. El agua es un solvente altamente polar."},
    {"id": 5, "pregunta": "5. [PROTEÍNAS] Puentes Disulfuro (S-S). ¿Estatus?", "opciones": ["Covalente No Polar", "Iónico"], "correcta": "Covalente No Polar", "retro_ok": "Brillante. Al ser dos átomos idénticos, la diferencia es 0.0 exacta. Esto otorga una estabilidad covalente óptima para la estructura terciaria.", "retro_error": "Pista: Ambos átomos pertenecen al mismo elemento (Azufre). ¿Puede un átomo quitarle electrones a su propio gemelo?"}
]

# --- INICIALIZACIÓN DEL SISTEMA DE PERSISTENCIA (STATE MANAGER) ---
if "auth" not in st.session_state: 
    st.session_state.auth = False
if "puntos" not in st.session_state: 
    st.session_state.puntos = 0
if "vidas" not in st.session_state: 
    st.session_state.vidas = 3
if "completados" not in st.session_state: 
    st.session_state.completados = set()
if "examen_terminado" not in st.session_state:
    st.session_state.examen_terminado = False

def registrar_acierto(modulo_id, puntos_modulo):
    if modulo_id not in st.session_state.completados:
        st.session_state.completados.add(modulo_id)
        st.session_state.puntos += puntos_modulo

def registrar_fallo():
    if st.session_state.vidas > 0:
        st.session_state.vidas -= 1

def reiniciar_simulador():
    st.session_state.puntos = 0
    st.session_state.vidas = 3
    st.session_state.completados = set()
    st.session_state.examen_terminado = False
    st.rerun()

# --- MOTOR GRÁFICO (CON ENFOQUE EN EXPERIMENTACIÓN ACTIVA) ---
def generar_svg_tira_afloja(fuerza):
    if fuerza >= 3.0:
        return """<div style='display:flex; justify-content:center; align-items:center; width:100%; height:110px;'>
            <svg viewBox="0 0 240 100" width="100%" height="100%">
                <circle cx="60" cy="50" r="26" fill="#ff5252" opacity="0.95"/>
                <text x="44" y="54" fill="white" font-weight="bold" font-family="sans-serif" font-size="12">Fuerte</text>
                <circle cx="95" cy="50" r="5" fill="#00e5ff"/>
                <ellipse cx="105" cy="50" rx="65" ry="28" fill="none" stroke="#ff5252" stroke-width="2" stroke-dasharray="4 2"/>
                <circle cx="180" cy="50" r="12" fill="#00e5ff" opacity="0.5"/>
            </svg>
        </div>"""
    else:
        return """<div style='display:flex; justify-content:center; align-items:center; width:100%; height:110px;'>
            <svg viewBox="0 0 240 100" width="100%" height="100%">
                <circle cx="60" cy="50" r="18" fill="#90a4ae" opacity="0.8"/>
                <text x="42" y="54" fill="white" font-family="sans-serif" font-size="11">Balance</text>
                <circle cx="120" cy="50" r="5" fill="#ffffff"/>
                <circle cx="120" cy="50" r="8" fill="none" stroke="#00e5ff" stroke-width="1.5"/>
                <circle cx="180" cy="50" r="18" fill="#90a4ae" opacity="0.8"/>
                <ellipse cx="120" cy="50" rx="65" ry="22" fill="none" stroke="#b0bec5" stroke-width="1.2" stroke-dasharray="2 2"/>
            </svg>
        </div>"""

def generar_svg_enlace(sym1, f1, c1, sym2, f2, c2):
    diff = abs(f1 - f2)
    # Corrección robusta mediante asignación directa por tuplas estructuradas autónomas
    if diff == 0:
        (cx1, cx2, ex, ew, sc, sd) = (113, 127, 120, 65, "#ffffff", "2 2")
    elif diff > 0.4:
        if f1 > f2:
            (cx1, cx2, ex, ew, sc, sd) = (85, 95, 100, 70, c1, "4 2")
        else:
            (cx1, cx2, ex, ew, sc, sd) = (145, 155, 140, 70, c2, "4 2")
    else:
        (cx1, cx2, ex, ew, sc, sd) = (105, 135, 120, 68, "#b0bec5", "3 3")
        
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

# --- INYECCIÓN DE INTERFAZ CÓSMICA PREMIUM ---
st.markdown("""
<style>
    .stApp {
        background-color: #05050a;
        background-image: radial-gradient(#111126 1px, transparent 20px);
    }
    div[data-testid="stMetricValue"] {
        color: #00e5ff !important;
        font-family: 'Courier New', monospace;
    }
    .stTabs [data-baseweb="tab"] {
        color: #b0bec5 !important;
        font-weight: bold;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #00e5ff !important;
        border-bottom-color: #00e5ff !important;
    }
</style>
""", unsafe_allow_html=True)

# --- PANTALLA DE AUTENTICACIÓN ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; color:#fff; font-family:sans-serif;'>⚛️ ChonpsLab Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#888;'>Simulador Avanzado de Bioquímica - FMVZ UNAM</p>", unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns([1,2,1])
    with col_b:
        pwd = st.text_input("Ingresa el token de acceso:", type="password")
        if st.button("Inicializar Laboratorio", use_container_width=True):
            if pwd == "CHONPS":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Token incorrecto. Verifica tus credenciales de la facultad.")
else:
    # --- DASHBOARD GLOBAL DE RENDIMIENTO (SIDEBAR PERSISTENTE) ---
    with st.sidebar:
        st.markdown("<h2 style='color:#fff; text-align:center;'>ChonpsLab Status</h2>", unsafe_allow_html=True)
        st.write("---")
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric(label="Score Total", value=f"{st.session_state.puntos} pts")
        with c2:
            # Alerta visual si las vidas bajan de 2
            corazones = "❤️" * st.session_state.vidas if st.session_state.vidas > 0 else "💀"
            st.metric(label="Estado Vital", value=corazones)
            
        st.write("---")
        st.markdown("### Progreso de Módulos")
        for idx, nombre in enumerate(["Atómica", "Estira/Afloja", "Reactor Enlaces", "Glucómica", "pH/Buffers", "Metabolismo"]):
            completado = "✅ Realizado" if idx in st.session_state.completados else "⏳ Pendiente"
            st.caption(f"**{nombre}**: {completado}")
            
        st.write("---")
        if st.button("Reiniciar Simulador", type="secondary", use_container_width=True):
            reiniciar_simulador()

    # --- CHASIS PRINCIPAL DE NAVEGACIÓN ---
    st.markdown("<h1 style='color:#fff; margin-bottom:0;'>ChonpsLab Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#00e5ff; margin-top:0;'>Entorno de Experimentación y Modelado Bioquímico</p>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏛️ Teoría Atómica", 
        "⚡ Estira y Afloja", 
        "🧬 Reactor de Enlaces", 
        "🍬 Glucómica Estructural", 
        "🌡️ Titulación y Buffers", 
        "🔥 Escalado Metabólico"
    ])
    
    # MÓDULO 1: TEORÍA ATÓMICA
    with tab1:
        st.subheader("Modelado Mecano-Cuántico de Bioelementos")
        st.write("Explora la configuración y los orbitales estables de los átomos que componen la materia viva.")
        
        elem_sel = st.selectbox("Selecciona un Bioelemento para analizar:", list(ELEMENTOS.keys()))
        datos = ELEMENTOS[elem_sel]
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Símbolo químico:** {datos['sym']}\n\n**Electronegatividad de Pauling:** {datos['fuerza']}")
        with col2:
            st.write("Presiona el botón para mapear el comportamiento cuántico:")
            if st.button("Calcular Configuración Electrónica", key="b_atom"):
                st.success("Configuración optimizada en caché de simulación.")
                registrar_acierto(0, 10)
                st.rerun()

    # MÓDULO 2: ESTIRA Y AFLOJA (CHONPS)
    with tab2:
        st.subheader("Simulador de Desplazamiento Electrónico")
        st.write("Modifica la electronegatividad teórica para observar cómo un átomo de gran fuerza deforma la nube electrónica de un átomo débil.")
        
        fuerza_simulada = st.slider("Fuerza del átomo central (Pauling):", 1.0, 4.0, 2.5, step=0.1)
        
        st.components.v1.html(generar_svg_tira_afloja(fuerza_simulada), height=120)
        
        if fuerza_simulada >= 3.4:
            st.warning("Zona de alta polaridad detectada: Este átomo central generará un fuerte dipolo permanente.")
            registrar_acierto(1, 15)

    # MÓDULO 3: REACTOR DE ENLACES
    with tab3:
        st.subheader("Reactor Simbiosis Electrónica")
        st.write("Ensambla dos bioelementos para evaluar instantáneamente la diferencia de electronegatividad y caracterizar el enlace resultante.")
        
        col_sel1, col_sel2 = st.columns(2)
        with col_sel1:
            e1 = st.selectbox("Átomo Nucleófilo (1):", list(ELEMENTOS.keys()), index=0)
        with col_sel2:
            e2 = st.selectbox("Átomo Electrofilo (2):", list(ELEMENTOS.keys()), index=1)
            
        dat1, dat2 = ELEMENTOS[e1], ELEMENTOS[e2]
        st.components.v1.html(generar_svg_enlace(dat1['sym'], dat1['fuerza'], dat1['color'], dat2['sym'], dat2['fuerza'], dat2['color']), height=140)
        
        diff_calc = abs(dat1['fuerza'] - dat2['fuerza'])
        st.metric("Diferencia de Electronegatividad (Δχ)", value=f"{diff_calc:.2f}")
        
        # Clasificación pedagógica automatizada
        if diff_calc == 0:
            st.success("Enlace Covalente No Polar Puro (Simetría perfecta en la distribución de carga).")
        elif diff_calc < 0.4:
            st.success("Enlace Covalente Apolar (Comportamiento hidrofóbico estable).")
        elif diff_calc < 1.7:
            st.info("Enlace Covalente Polar (Generación de dipolos interactivos y solubilidad).")
        else:
            st.error("Enlace con alta translocación / Carácter Iónico predominante.")
        registrar_acierto(2, 20)

    # MÓDULO 4: GLUCÓMICA (EPÍMEROS)
    with tab4:
        st.subheader("Isomería Estructural en Carbohidratos")
        st.write("Modifica la orientación espacial de los carbonos quirales para diferenciar la D-Glucosa de sus epímeros fisiológicos.")
        
        c4_orientacion = st.radio("Orientación del Grupo Hidroxilo (-OH) en el Carbono 4:", ["Derecha (Glucosa)", "Izquierda (Galactosa)"])
        
        if c4_orientacion == "Izquierda (Galactosa)":
            st.info("🧬 **Cambio Estructural:** Has transformado la molécula en D-Galactosa (Epímero en C-4). Crucial para la síntesis de lactosa en la glándula mamaria.")
            registrar_acierto(3, 25)
        else:
            st.success("Molécula base configurada como D-Glucosa estándar.")

    # MÓDULO 5: TITULACIÓN DE pH (BUFFERS)
    with tab5:
        st.subheader("Simulador de Amortiguación Homeostática")
        st.write("Añade equivalentes de ácido o base a un sistema buffer para calcular la respuesta del sistema según la ecuación de Henderson-Hasselbalch.")
        
        pk_buffer = st.number_input("pKa del sistema buffer (Ej. Amortiguador Fosfato):", value=6.86, step=0.01)
        ratio_sal_acido = st.slider("Relación [Aceptar de Protones] / [Donador de Protones]:", 0.1, 10.0, 1.0, step=0.1)
        
        import math
        ph_calculado = pk_buffer + math.log10(ratio_sal_acido)
        
        st.metric("pH Resultante del Sistema", value=f"{ph_calculado:.2f}")
        if abs(ph_calculado - pk_buffer) <= 1.0:
            st.success("El buffer se encuentra dentro de su rango de máxima eficiencia homeostática (±1 unidad de pH).")
            registrar_acierto(4, 30)
        else:
            st.warning("Capacidad amortiguadora agotada. El sistema corre riesgo de variaciones críticas de pH.")

    # MÓDULO 6: ESCALADO METABÓLICO (LÍPIDOS, PROTEÍNAS Y EXAMEN)
    with tab6:
        st.subheader("Laboratorio Avanzado de Macromoléculas y Evaluación")
        
        if st.session_state.vidas <= 0:
            st.error("❌ Has agotado tus vidas de laboratorio. Revisa los fundamentos teóricos y reinicia el simulador para volver a intentar.")
        elif st.session_state.examen_terminado:
            st.balloons()
            st.success(f"🏆 ¡Felicitaciones! Has completado el circuito de bioquímica aplicada con {st.session_state.puntos} puntos totales.")
        else:
            # Renderizado dinámico de la pregunta actual según el estado vital
            preg_actual_idx = len(st.session_state.completados) - 5
            if preg_actual_idx < 0: 
                preg_actual_idx = 0
            if preg_actual_idx >= len(PREGUNTAS_DESAFIO):
                preg_actual_idx = len(PREGUNTAS_DESAFIO) - 1
                
            item = PREGUNTAS_DESAFIO[preg_actual_idx]
            
            st.markdown(f"#### Desafío Activo: {item['pregunta']}")
            opcion_elegida = st.radio("Selecciona tu hipótesis científica:", item['opciones'], key=f"p_{item['id']}")
            
            if st.button("Emitir Dictamen de Laboratorio", key=f"btn_{item['id']}"):
                if opcion_elegida == item['correcta']:
                    st.success(item['retro_ok'])
                    registrar_acierto(5 + item['id'], 20)
                    time.sleep(1.5)
                    if preg_actual_idx == len(PREGUNTAS_DESAFIO) - 1:
                        st.session_state.examen_terminado = True
                    st.rerun()
                else:
                    st.error(item['retro_error'])
                    registrar_fallo()
                    time.sleep(1.5)
                    st.rerun()
