import streamlit as st
import time

# 1. CONFIGURACIÓN DEL ENTORNO DE SIMULACIÓN NATIVA (CHASIS ULTRAVELOZ)
st.set_page_config(page_title="ChonpsLab Pro", page_icon="⚛️", layout="centered")

# --- BANCO DE DATOS MAESTRO REORDENADO EN SECUENCIA ESTRICTA C-H-O-N-P-S ---
ELEMENTOS = {
    "Carbono (C)": {"fuerza": 2.55, "color": "#ffb142", "symbol": "C", "desc": "El esqueleto covalente universal de la materia viva. Forma uniones estables en el 100% de las macromoléculas (Carbohidratos, Lípidos, Proteínas y Ácidos Nucleicos)."},
    "Hidrógeno (H)": {"fuerza": 2.20, "color": "#00e5ff", "symbol": "H", "desc": "Saturador de cadenas hidrofóbicas en Lípidos y estabilizador conformacional de hélices y puentes hídricos inter-moleculares."},
    "Oxígeno (O)": {"fuerza": 3.44, "color": "#ff5252", "symbol": "O", "desc": "Altamente electronegativo y ambicioso. Induce la polaridad espacial, dipolos eléctricos y puentes de hidrógeno clave para la hidrofilia celular."},
    "Nitrógeno (N)": {"fuerza": 3.04, "color": "#33d9b2", "symbol": "N", "desc": "Estructurador de grupos amino en aminoácidos y bases nitrogenadas. Define la identidad química estructural de Proteínas y Ácidos Nucleicos."},
    "Fósforo (P)": {"fuerza": 2.19, "color": "#ff7ff5", "symbol": "P", "desc": "Elemento pilar para los enlaces fosfodiéster de alta energía (ATP) y la columna vertebral estructural del ADN y ARN."},
    "Azufre (S)": {"fuerza": 2.58, "color": "#ffda79", "symbol": "S", "desc": "Elemento de soporte estructural y rigidez molecular tridimensional. Presente en aminoácidos azufrados formadores de puentes disulfuro proteicos."}
}

PREGUNTAS_DESAFIO = [
    {
        "id": 1,
        "pregunta": "1. [JERARQUÍA: LÍPIDOS] Las cadenas de los ácidos grasos están formadas casi exclusivamente por Carbono (2.55) e Hidrógeno (2.20). Al experimentar en el reactor, vemos que su diferencia es menor a 0.4. ¿Cuál es la propiedad resultante en los lípidos celulares?",
        "opciones": ["Son altamente polares e hidrofílicos, disolviéndose de forma libre en el plasma.", "Son apolares e hidrofóbicos, ideales para formar membranas celulares aislantes."],
        "correcta": "Son apolares e hidrofóbicos, ideales para formar membranas celulares aislantes.",
        "retro": "Correcto. Al tener fuerzas similares (diferencia de 0.35), comparten electrones equitativamente de forma no polar, lo que repele el medio acuoso."
    },
    {
        "id": 2,
        "pregunta": "2. [JERARQUÍA: PROTEÍNAS] El enlace peptídico une covalentemente un Carbono (2.55) con un Nitrógeno (3.04). Al analizar el Espectrómetro, ¿cómo se distribuye la densidad electrónica en este pilar proteico?",
        "opciones": ["Se genera un dipolo local (Polar) debido a que el Nitrógeno atrae con mayor fuerza los electrones.", "Se comparte de forma 100% idéntica (Apolar) porque las fuerzas se cancelan en el espacio geométrico."],
        "correcta": "Se genera un dipolo local (Polar) debido a que el Nitrógeno atrae con mayor fuerza los electrones.",
        "retro": "Correcto. El Nitrógeno es más electronegativo (3.04) que el Carbono (2.55), por lo que jala los electrones compartidos hacia su núcleo creando una amida polar rígida."
    },
    {
        "id": 3,
        "pregunta": "3. [JERARQUÍA: ÁCIDOS NUCLEICOS] La columna vertebral del ADN requiere enlaces Fósforo-Oxígeno. Con una diferencia de fuerza crítica de 1.25 ($3.44 - 2.19$), estos enlaces se caracterizan por:",
        "opciones": ["Ser enlaces fuertemente polares, acumulando tensiones de carga ideales para la transferencia de energía.", "Ser enlaces apolares e inertes, lo que impide mecánicamente la duplicación celular."],
        "correcta": "Ser enlaces fuertemente polares, acumulando tensiones de carga ideales para la transferencia de energía.",
        "retro": "Correcto. Esta asimetría masiva genera la inestabilidad reactiva controlada de los grupos fosfato indispensables para el ATP y el esqueleto de ácidos nucleicos."
    },
    {
        "id": 4,
        "pregunta": "4. [JERARQUÍA: CARBOHIDRATOS] Los azúcares como la glucosa poseen múltiples grupos oxhidrilo (-OH) donde el Oxígeno (3.44) se une al Hidrógeno (2.20). ¿Por qué la glucosa es el combustible rápido soluble del plasma sanguíneo?",
        "opciones": ["Porque el enlace O-H es altamente polar, permitiendo que el agua del plasma la disuelva mediante puentes de hidrógeno de inmediato.", "Porque la geometría simétrica neutra del O-H repele el agua, forzando a la glucosa a precipitar."],
        "correcta": "Porque el enlace O-H es altamente polar, permitiendo que el agua del plasma la disuelva mediante puentes de hidrógeno de inmediato.",
        "retro": "Correcto. El enlace O-H es polar por excelencia, lo que permite que interactúe perfectamente con las cargas parciales del solvente universal (agua)."
    },
    {
        "id": 5,
        "pregunta": "5. [JERARQUÍA: PROTEÍNAS AVANZADAS] Para estabilizar tridimensionalmente la insulina, se requiere unir dos átomos del mismo elemento: Azufre (2.58) con Azufre (2.58). ¿Qué estatus arrojará el reactor para este puente disulfuro?",
        "opciones": ["Enlace Covalente Homogéneo No Polar (Diferencia = 0.0), mecánicamente rígido y simétrico.", "Enlace Iónico Crítico por transferencia neta con colapso de dipolos estables."],
        "correcta": "Enlace Covalente Homogéneo No Polar (Diferencia = 0.0), mecánicamente rígido y simétrico.",
        "retro": "Correcto. Al unirse átomos del mismo elemento, la diferencia de electronegatividad es cero, generando un enlace covalente perfectamente balanceado y fuerte."
    }
]

# --- MOTOR DE MAPEO BIOLÓGICO DINÁMICO (INTEGRACIÓN DE LA CÁTEDRA UNAM) ---
def obtener_contexto_biologico(sym1, sym2):
    combo = "".join(sorted([sym1, sym2]))
    mapeo = {
        "CC": ("Carbohidratos y Cadenas Orgánicas", "Estructura basal de esqueletos hidrocarbonados lineales o cíclicos (como las piranosas de la glucosa o furanosas de la fructosa). Unión 100% apolar y mecánicamente estable."),
        "CH": ("Lípidos (Cadenas Hidrofóbicas)", "Constituyente de los ácidos grasos. Al tener una diferencia de electronegatividad insignificante (0.35), la nube electrónica es perfectamente simétrica, repeliendo el agua y aislando membranas celulares."),
        "CO": ("Carbohidratos (Grupos Carbonilo)", "Configuración presente en los carbonilos de aldosas (grupo aldehído al principio de la cadena) y cetosas (grupo cetona en el centro o seno de la molécula). Enlace polar reactivo."),
        "CN": ("Proteínas (Enlace Peptídico / Amidas)", "Unión covalente entre el grupo carboxilo y el grupo amino de los aminoácidos. Estructura tipo amida rígida que estabiliza las cadenas polipeptídicas de las proteínas celulares."),
        "CP": ("Metabolitos Fosforados Orgánicos", "Configuración presente en intermediarios metabólicos de transición energética intracelular."),
        "CS": ("Aminoácidos Azufrados", "Estructurador basal presente en aminoácidos esenciales como la Metionina, cruciales para el inicio de la traducción de proteínas."),
        "HH": ("Gas Hidrógeno / Estado Reducido", "Unión molecular diatómica simétrica homonuclear elemental."),
        "HO": ("Agua / Grupos Oxhidrilo (-OH)", "Estructura dipolar por excelencia. El Oxígeno desplaza la nube electrónica creando cargas parciales negativas ($\delta^-$) y positivas ($\delta^+$) en los Hidrógenos, facilitando la hidrofilia del plasma."),
        "HN": ("Grupos Amino (Proteínas y ADN)", "Presente en los grupos amina ($NH_2$) de los aminoácidos y en las bases nitrogenadas (Adenina, Guanina, Citocina, Timina, Uracilo) unidas al azúcar mediante enlaces N-glucosídicos."),
        "HP": ("Fosfatos e Hidruros Libres", "Interacciones químicas basales de regulación y amortiguación en el citoplasma celular."),
        "HS": ("Grupos Tiol (-SH)", "Presente en la Cisteína. El grupo funcional tiol es altamente reactivo y es el responsable directo de la formación de puentes moleculares cruzados."),
        "OO": ("Oxígeno Molecular ($O_2$)", "Gas diatómico con un enlace doble simétrico neutro. No genera dipolo y es indispensable para la respiración aeróbica mitocondrial celular."),
        "NO": ("Grupos Nitro y Amidas Modificadas", "Uniones con fuerte gradiente electrónico presentes en hormonas glicoproteicas complejas (como la LH y FSH) y lectinas celulares."),
        "OP": ("Ácidos Nucleicos y ATP (Enlaces Fosfodiéster)", "Tensión dipolar crítica. Da origen a los enlaces fosfodiéster de alta energía que encadenan los nucleótidos del ADN/ARN y permiten la transferencia energética masiva mediante el ATP."),
        "OS": ("Grupos Sulfato (Glucosaminoglucanos)", "Configuración ácida fuerte que le da la consistencia gelatinosa al Condroitín Sulfato o Queratan Sulfato de la matriz extracelular articular animal."),
        "NN": ("Gas Nitrógeno Homonuclear ($N_2$)", "Unión molecular triple simétrica neutra inerte."),
        "NP": ("Complejos Fósforo-Nitrógeno", "Interacciones polares presentes en los anillos de nucleótidos celulares avanzados."),
        "NS": ("Centros Enzimáticos Azufrados", "Configuraciones coordinadas presentes en los sitios activos de enzimas metabólicas de óxido-reducción."),
        "PP": ("Fósforo Elemental Resonante", "Unión molecular simétrica homonuclear de control energético."),
        "PS": ("Sulfuros de Fósforo Intermediarios", "Enlaces de transición molecular en rutas de síntesis avanzadas."),
        "SS": ("Proteínas (Puentes Disulfuro)", "Enlace covalente homonuclear (Diferencia = 0.0) entre dos Azufres de Cisteínas. Es el responsable de consolidar la rigidez de la estructura terciaria de proteínas tridimensionales complejas como la Insulina.")
    }
    return mapeo.get(combo, ("Ecosistema Bioquímico", "Interacción de bioelementos primarios complementarios en el entorno celular."))

# --- MOTOR DE GRÁFICOS VECTORIALES DINÁMICOS CORREGIDO (SVG SEGURO EN CACHÉ) ---
@st.cache_data
def obtener_diagrama_vectorial(tipo_evento, color1="#ffffff", color2="#ffffff", sym1="A", sym2="B", diff=0.0):
    """
    Renderizador vectorial optimizado. Resuelve el bug de strings al encapsular 
    los SVG de forma matemática e independiente.
    """
    if tipo_evento == "estira_afloja_fuerte":
        return """
        <div style='display: flex; justify-content: center; align-items: center; width: 100%; height: 110px;'>
            <svg viewBox="0 0 240 100" width="100%" height="100%">
                <circle cx="60" cy="50" r="24" fill="#ff5252" opacity="0.9"/>
                <text x="48" y="54" fill="white" font-weight="bold" font-family="sans-serif" font-size="12">Fuerte</text>
                <circle cx="95" cy="50" r="5" fill="#00e5ff"/>
                <ellipse cx="105" cy="50" rx="65" ry="28" fill="none" stroke="#ff5252" stroke-width="1.5" stroke-dasharray="4 2"/>
                <circle cx="180" cy="50" r="12" fill="#00e5ff" opacity="0.5"/>
            </svg>
        </div>
        """
    elif tipo_evento == "estira_afloja_debil":
        return """
        <div style='display: flex; justify-content: center; align-items: center; width: 100%; height: 110px;'>
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
    
    # Renderizador dinámico para el Macro-Reactor de la Fase 1
    if diff == 0:
        cx_e1, cx_e2 = 113, 127
        ellipse_x, ellipse_w = 120, 65
        stroke_color = "#ffffff"
        stroke_dash = "2 2"
    elif diff > 0.4:
        cx_e1, cx_e2 = 85, 95
        ellipse_x, ellipse_w = 100, 70
        stroke_color = color1
        stroke_dash = "4 2"
    else:
        cx_e1, cx_e2 = 105, 135
        ellipse_x, ellipse_w = 120, 68
        stroke_color = "#b0bec5"
        stroke_dash = "3 3"

    return f"""
    <div style='display: flex; justify-content: center; align-items: center; width: 100%; height: 130px;'>
        <svg viewBox="0 0 240 120" width="100%" height="100%" style="background: transparent;">
            <circle cx="70" cy="60" r="22" fill="{color1}" opacity="0.85"/>
            <text x="64" y="65" fill="black" font-weight="bold" font-family="sans-serif" font-size="14">{sym1}</text>
            <circle cx="170" cy="60" r="18" fill="{color2}" opacity="0.85"/>
            <text x="164" y="64" fill="black" font-weight="bold" font-family="sans-serif" font-size="12">{sym2}</text>
            <ellipse cx="{ellipse_x}" cy="60" rx="{ellipse_w}" ry="32" fill="none" stroke="{stroke_color}" stroke-width="1.5" stroke-dasharray="{stroke_dash}"/>
            <circle cx="{cx_e1}" cy="60" r="4" fill="#ffffff"/>
            <circle cx="{cx_e2}" cy="60" r="4" fill="#ffffff"/>
        </svg>
    </div>
    """

# --- INYECCIÓN DE ESTILOS CSS RECONSTRUIDOS (UNIVERSO OSCURO E INTERFACES TRANSLÚCIDAS) ---
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
    .main-title { text-align: center; color: #ffffff; font-size: 3.4rem; font-weight: 800; font-family: 'Segoe UI', sans-serif; margin-bottom: 0px; }
    .main-title-suffix { color: #00e5ff; font-weight: 300; }
    .sub-title { text-align: center; font-style: italic; color: #90a4ae; font-size: 1.1rem; margin-top: 5px; margin-bottom: 25px; }
    .bio-panel { background-color: rgba(30, 41, 59, 0.5); border: 1px solid rgba(0, 229, 255, 0.2); border-left: 5px solid #00e5ff; padding: 24px; border-radius: 8px; margin-bottom: 30px; }
    .panel-hook { color: #00e5ff; font-weight: 700; font-size: 1.25rem; display: block; margin-bottom: 8px; }
    .panel-text { color: #cfd8dc; font-size: 0.95rem; margin: 0; line-height: 1.5; }
    .console-header { background-color: rgba(30, 41, 59, 0.4); border-left: 5px solid #0288d1; padding: 15px; border-radius: 4px; margin-bottom: 20px; }
    .spectrometer-card-success { background-color: rgba(76, 175, 80, 0.08); border: 1px solid rgba(76, 175, 80, 0.25); border-left: 6px solid #4caf50; padding: 20px; border-radius: 6px; margin-top: 15px; }
    .spectrometer-card-error { background-color: rgba(244, 67, 54, 0.08); border: 1px solid rgba(244, 67, 54, 0.25); border-left: 6px solid #f44336; padding: 20px; border-radius: 6px; margin-top: 15px; }
    .spectrometer-title { color: #b0bec5; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; margin-bottom: 8px; }
    .sidebar-monitor { background-color: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); padding: 12px; border-radius: 4px; margin-bottom: 10px; text-align: center; }
</style>
""", unsafe_allow_html=True)

# CONTROL DEL MOTOR DE ESTADOS COMPARTIDOS Y PERSISTENCIA NATIVA
CODIGOS_VIGENTES = ["SYNAPSIS-PRO", "VET-BIOQUIMICA-2026", "MED-ELITE-30DAYS"]
if "autenticado" not in st.session_state: st.session_state["autenticado"] = False
if "vidas" not in st.session_state: st.session_state["vidas"] = 3
if "puntos" not in st.session_state: st.session_state["puntos"] = 0
if "bloque_actual" not in st.session_state: st.session_state["bloque_actual"] = 0 
if "sim_ejecutada" not in st.session_state: st.session_state["sim_ejecutada"] = False
if "sim_html" not in st.session_state: st.session_state["sim_html"] = ""
if "sim_status" not in st.session_state: st.session_state["sim_status"] = ""
if "sim_output" not in st.session_state: st.session_state["sim_output"] = ""
if "sim_macro" not in st.session_state: st.session_state["sim_macro"] = ""
if "sim_error" not in st.session_state: st.session_state["sim_error"] = False

# Estados de control para la evaluación detallada de la Fase 2
if "quiz_enviado" not in st.session_state: st.session_state["quiz_enviado"] = False
if "errores_quiz" not in st.session_state: st.session_state["errores_quiz"] = []
if "respuestas_guardadas" not in st.session_state: st.session_state["respuestas_guardadas"] = {}

# ========================================================
# --- ACCESO AL LABORATORIO PÚBLICO ---
# ========================================================
if not st.session_state["autenticado"]:
    st.markdown("<h1 class='main-title'>Chonps<span class='main-title-suffix'>Lab Pro</span></h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Simulador Avanzado de Bioquímica e Interacción Atómica</p>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='outline-container bio-panel'>
        <span class='panel-hook'>El Alfabeto de la Vida: Ecosistema CHONPS</span>
        <p class='panel-text'>
            Carbono (C), Hidrógeno (H), Oxígeno (O), Nitrógeno (N), Fósforo (P) y Azufre (S). Estos seis elementos construyen el 99% de la materia viva en el planeta. Sincroniza tu entorno analítico para regular sus fuerzas de enlace y comprender cómo estructuran la jerarquía molecular celular.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='font-weight: 600; margin-top: 10px; color: #ffffff;'>Sincronización del Entorno Analítico</h3>", unsafe_allow_html=True)
    codigo_input = st.text_input("Licencia de Acceso Digital (Token Único):", type="password", placeholder="Introduce tu clave premium de 30 días...")
    if st.button("Encender Reactores Computacionales", use_container_width=True):
        if codigo_input.strip().upper() in CODIGOS_VIGENTES:
            st.session_state["autenticado"] = True
            st.rerun()
        else:
            st.error("Token inválido o expirado. Verifica tu suscripción.")

# ========================================================
# --- CONSOLA PRIVADA DE SIMULACIÓN (CHONPSLAB) ---
# ========================================================
else:
    st.markdown("""
    <div class='console-header'>
        <h2 style='margin:0; color: #00e5ff; font-weight: 700;'>ChonpsLab: Consola Analítica Profesional</h2>
        <span style='color: #90a4ae; font-size: 0.85rem;'>Ecosistema de Ciencias de la Salud Protegido (Basado en la Cátedra UNAM)</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Barra Lateral Rediseñada con Estilo Oscuro Hitech
    with st.sidebar:
        st.markdown("<h3 style='font-weight:600; margin-bottom:15px;'>Monitor de Progreso</h3>", unsafe_allow_html=True)
        st.markdown(f"<div class='sidebar-monitor'><span style='color:#90a4ae; font-size:0.8rem; text-transform:uppercase;'>Estabilidad de Vidas</span><br><b style='font-size:1.5rem; color:#f44336;'>{st.session_state.vidas} / 3</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='sidebar-monitor'><span style='color:#90a4ae; font-size:0.8rem; text-transform:uppercase;'>Puntaje Acumulado</span><br><b style='font-size:1.5rem; color:#00e5ff;'>{st.session_state.puntos} pts</b></div>", unsafe_allow_html=True)
        
        st.write("---")
        st.markdown("<h4 style='font-weight:600;'>Navegación del Módulo</h4>", unsafe_allow_html=True)
        if st.button("Fase 0: El Estira y Afloja", use_container_width=True):
            st.session_state.bloque_actual = 0
            st.session_state.sim_ejecutada = False
            st.rerun()
        if st.button("Fase 1: Macro-Reactor CHONPS", use_container_width=True):
            st.session_state.bloque_actual = 1
            st.session_state.sim_ejecutada = False
            st.rerun()
        if st.button("Fase 2: El Examen de Desafío", use_container_width=True):
            st.session_state.bloque_actual = 2
            st.rerun()
            
        st.write("---")
        if st.button("Desconectar Laboratorio", use_container_width=True):
            st.session_state["autenticado"] = False
            st.rerun()

    if st.session_state.vidas <= 0:
        st.markdown("""
        <div class='spectrometer-card-error'>
            <div class='spectrometer-title' style='color:#f44336;'>Falla de Memoria Homeostática Crítica</div>
            Reactor bloqueado debido a colapso conceptual clínico en el medio interno.
        </div>
        """, unsafe_allow_html=True)
        if st.button("Reiniciar Sistema y Reactivos", use_container_width=True):
            st.session_state.vidas = 3
            st.session_state.puntos = 0
            st.session_state.bloque_actual = 0
            st.session_state.sim_ejecutada = False
            st.session_state.quiz_enviado = False
            st.session_state.errores_quiz = []
            st.rerun()
    else:
        # --------------------------------------------------------
        # --- FASE 0: CALENTAMIENTO E INTUICIÒN COMPLETA ---
        # --------------------------------------------------------
        if st.session_state.bloque_actual == 0:
            st.subheader("Fase 0: Inducción Electronegativa")
            st.write("Mueve el control deslizante para comprender de forma física cómo la fuerza atómica (**Electronegatividad en la Escala de Pauling**) jala y deforma las nubes de electrones orbitales.")
            
            fuerza_fase0 = st.slider("Ajustar Fuerza de Atracción (Escala Pauling):", 0.7, 4.0, 2.2, step=0.1)
            if fuerza_fase0 >= 3.0:
                st.info("⚡ **Átomo Fuerte / Ambicioso (Ej: Oxígeno: 3.44 o Nitrógeno: 3.04).** Deforma la geometría molecular y atrae las cargas de electrones hacia sí.")
                svg_induccion = obtener_diagrama_vectorial("estira_afloja_fuerte")
            else:
                st.success("🤝 **Átomo Equilibrado / Débil (Ej: Carbono: 2.55 o Hidrógeno: 2.20).** Distribuye y comparte los electrones con justicia orbital.")
                svg_induccion = obtener_diagrama_vectorial("estira_afloja_debil")
            
            st.components.v1.html(svg_induccion, height=110, scrolling=False)
            
            st.write("---")
            st.markdown("<h4>El Mapa de Calor Quántico de CHONPS</h4>", unsafe_allow_html=True)
            st.write("Analiza las identidades cuánticas de los componentes oficiales de la vida según su jerarquía molecular:")
            
            for key, val in ELEMENTOS.items():
                st.markdown(f"<span style='color:{val['color']}; font-weight:bold;'>{key} (Fuerza: {val['fuerza']}):</span> <span style='color:#cfd8dc;'>{val['desc']}</span>", unsafe_allow_html=True)
            
            st.write("")
            st.write("**Reto de Nivelación:** Si el Carbono (2.55) y el Azufre (2.58) se unen, sus fuerzas están prácticamente empatadas en la escala de Pauling. ¿Cómo se comportará su enlace espacial?")
            resp_f0 = st.radio("Elige tu hipótesis de laboratorio:", ["Será un enlace simétrico y No Polar (reparto equitativo)", "Será un enlace asimétrico altamente Polar (un núcleo domina)"])
            
            if st.button("Validar Entrada al Laboratorio", use_container_width=True):
                if "No Polar" in resp_f0:
                    st.balloons()
                    st.session_state.puntos += 50
                    st.session_state.bloque_actual = 1
                    st.rerun()
                else:
                    st.error("Error analítico. Fuerzas similares equivalen a un reparto justo (No Polar). Revisa el mapa de calor de Pauling.")

        # --------------------------------------------------------
        # --- FASE 1: SIMULADOR MACRO CHONPS AVANZADO CON CONTEXTO ---
        # --------------------------------------------------------
        elif st.session_state.bloque_actual == 1:
            st.subheader("Fase 1: Macro-Reactor de Macromoléculas Orgánicas")
            st.write("Combina libremente cualquiera de los 6 bioelementos fundamentales para analizar la física cuántica de sus enlaces y descubrir su rol en la jerarquía biológica.")
            
            col1, col2 = st.columns(2)
            with col1:
                e1 = st.selectbox("Átomo Central (Núcleo A):", list(ELEMENTOS.keys()))
            with col2:
                e2 = st.selectbox("Átomo de Reacción (Núcleo B):", list(ELEMENTOS.keys()))
                
            if st.button("Sintetizar Enlace Molecular", use_container_width=True):
                st.session_state.sim_ejecutada = True
                verificar_bloqueo_pirateria()
                
                f1, fill1, sym1 = ELEMENTOS[e1]["fuerza"], ELEMENTOS[e1]["color"], ELEMENTOS[e1]["symbol"]
                f2, fill2, sym2 = ELEMENTOS[e2]["fuerza"], ELEMENTOS[e2]["color"], ELEMENTOS[e2]["symbol"]
                diff = abs(f1 - f2)
                
                # Mapeo biológico dinámico unificado
                macro, contexto = obtener_contexto_biologico(sym1, sym2)
                st.session_state.sim_macro = f"🧬 **Macromolécula Asociada:** {macro}<br>🔬 **Importancia Biológica:** {contexto}"
                st.session_state.sim_html = obtener_diagrama_vectorial("dinamico", fill1, fill2, sym1, sym2, diff)
                
                if diff == 0:
                    st.session_state.estado_sistema = "Enlace Covalente Homonúcleo Neutro"
                    st.session_state.resultado_texto = f"Configuración balanceada pura. Ambos núcleos tienen una fuerza idéntica de {f1}. Los electrones orbitan de manera perfectamente geométrica en el centro del enlace, sin indicios de asimetría o polos eléctricos."
                    st.session_state.sim_error = False
                    st.session_state.puntos += 100
                elif diff <= 0.4:
                    st.session_state.estado_sistema = "Enlace Covalente No Polar Simétrico"
                    st.session_state.resultado_texto = f"Alineación estable. La diferencia de electronegatividad es de apenas {diff:.2f}. Los átomos comparten los electrones de forma equitativa, resultando en una estructura eléctricamente neutra e hidrofóbica."
                    st.session_state.sim_error = False
                    st.session_state.puntos += 100
                elif diff <= 1.7:
                    st.session_state.estado_sistema = "Enlace Covalente Polar (Dipolo Eléctrico Activo)"
                    st.session_state.resultado_texto = f"Análisis molecular completado. La diferencia de fuerza de {diff:.2f} genera que el elemento más electronegativo desplace la nube electrónica hacia su eje, induciendo una carga parcial negativa ($\delta^-$) sobre sí y una carga parcial positiva ($\delta^+$) sobre el elemento más débil."
                    st.session_state.sim_error = False
                    st.session_state.puntos += 120
                else:
                    st.session_state.estado_sistema = "Inestabilidad de Fluidos / Conflicto de Afinidad"
                    st.session_state.resultado_texto = f"Anomalía en el reactor celular por incompatibilidad de variables metabólicas intermedias. La fuerza crítica altera el balance homeostático del buffer celular."
                    st.session_state.sim_error = True
                    st.session_state.vidas -= 1
                st.rerun()

            # RENDER DE RESULTADOS DEL ESPECTRÓMETRO EN FASE 1
            if st.session_state.sim_ejecutada:
                st.write("---")
                if st.session_state.sim_error:
                    st.markdown(f"""
                    <div class='spectrometer-card-error'>
                        <div class='spectrometer-title' style='color:#ff5252;'>Lectura del Espectrómetro: Anomalía del Medio</div>
                        <strong style='font-size:1.1rem; color:#ff8a80;'>Estatus: {st.session_state.estado_sistema}</strong><br>
                        <p style='margin-top:10px; color:#cfd8dc;'>{st.session_state.resultado_texto}</p>
                        <p style='margin-top:5px; color:#ff8a80;'>{st.session_state.sim_macro}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='spectrometer-card-success'>
                        <div class='spectrometer-title' style='color:#69f0ae;'>Lectura del Espectrómetro: Estabilidad Óptima</div>
                        <strong style='font-size:1.1rem; color:#b9f6ca;'>Estatus: {st.session_state.estado_sistema}</strong><br>
                        <p style='margin-top:10px; color:#cfd8dc;'>{st.session_state.resultado_texto}</p>
                        <p style='margin-top:5px; color:#69f0ae;'>{st.session_state.sim_macro}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Despliegue seguro del SVG sin romper la interfaz del celular
                if st.session_state.sim_html:
                    st.write("")
                    st.components.v1.html(st.session_state.sim_html, height=130, scrolling=False)
                    
                st.write("")
                if st.button("Limpiar Cámara de Inyección", use_container_width=True):
                    st.session_state.sim_ejecutada = False
                    st.session_state.sim_html = ""
                    st.rerun()

        # ========================================================
        # --- FASE 2: MÓDULO DE DESAFÍOS CON RETROALIMENTACIÓN DETALLADA ---
        # ========================================================
        elif st.session_state.bloque_actual == 2:
            st.subheader("Fase 2: El Examen de Desafío de ChonpsLab")
            st.write("Demuestra tu dominio de la jerarquía molecular. Responde este cuestionario basado en la simulación y las conferencias bioquímicas de la UNAM.")
            
            # Formulario robusto para evitar recargas accidentales
            respuestas_formulario = {}
            for item in PREGUNTAS_DESAFIO:
                st.markdown(f"<p style='font-weight:600; margin-bottom:5px; color:#ffffff;'>{item['pregunta']}</p>", unsafe_allow_html=True)
                
                # Mantener la persistencia visual de la selección
                idx_previo = 0
                if item['id'] in st.session_state.respuestas_guardadas:
                    if st.session_state.respuestas_guardadas[item['id']] in item['opciones']:
                        idx_previo = item['opciones'].index(st.session_state.respuestas_guardadas[item['id']])
                
                respuestas_formulario[item['id']] = st.radio(
                    f"Selección para reactivo {item['id']}:", 
                    item['opciones'], 
                    index=idx_previo,
                    key=f"radio_quiz_{item['id']}", 
                    label_visibility="collapsed"
                )
                st.write("")
            
            if st.button("Evaluar Respuestas de la Suite", use_container_width=True):
                st.session_state.quiz_enviado = True
                st.session_state.respuestas_guardadas = respuestas_formulario
                st.session_state.errores_quiz = []
                
                for item in PREGUNTAS_DESAFIO:
                    if respuestas_formulario[item['id']] != item['correcta']:
                        st.session_state.errores_quiz.append(item['id'])
                
                if len(st.session_state.errores_quiz) == 0:
                    st.session_state.puntos += 500
                else:
                    st.session_state.vidas -= 1
                st.rerun()

            # SECCIÓN DE CORRECCIÓN QUIRÚRGICA DETALLADA (ELIMINA LAGUNAS)
            if st.session_state.quiz_enviado:
                st.write("---")
                st.markdown("<h3>🎯 Reporte de Desempeño y Retroalimentación</h3>", unsafe_allow_html=True)
                
                if len(st.session_state.errores_quiz) == 0:
                    st.balloons()
                    st.success("🏆 ¡CALIFICACIÓN EXQUISITA: 10 de 10! Has respondido todos los desafíos de forma perfecta. Se han abonado 500 puntos a tu matrícula.")
                else:
                    st.error(f"⚠️ REVISIÓN DEL RECTOR: Se detectaron {len(st.session_state.errores_quiz)} lagunas conceptuales. Has perdido 1 vida. Analiza la corrección detallada abajo:")
                
                for item in PREGUNTAS_DESAFIO:
                    fue_error = item['id'] in st.session_state.errores_quiz
                    eleccion = st.session_state.respuestas_guardadas.get(item['id'], "Ninguna")
                    
                    with st.expander(f"Análisis del Reactivo {item['id']} — {'❌ INCORRECTO' if fue_error else '✅ CORRECTO'}", expanded=fue_error):
                        st.markdown(f"**Tu selección:** *{eleccion}*")
                        st.markdown(f"**Respuesta correcta:** *{item['correcta']}*")
                        if fue_error:
                            st.markdown(f"<p style='color:#ff8a80; font-weight:600;'>{item['retro']}</p>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<p style='color:#b9f6ca; font-weight:600;'>{item['retro']}</p>", unsafe_allow_html=True)
                
                if st.button("Re-inicializar Cámara de Evaluación"):
                    st.session_state.quiz_enviado = False
                    st.session_state.errores_quiz = []
                    st.session_state.respuestas_guardadas = {}
                    st.rerun()

    st.write("---")
    if st.button("Sincronizar Canales de Red"):
        st.rerun()
