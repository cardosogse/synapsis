import streamlit as st
import time

# 1. CONFIGURACIÓN DEL ENTORNO DE SIMULACIÓN NATIVA
st.set_page_config(page_title="ChonpsLab Pro", page_icon="⚛️", layout="centered")

# --- BANCO DE DATOS MAESTRO (PROPIEDADES BIOLÓGICAS DE CHONPS) ---
ELEMENTOS = {
    "Oxígeno (O)": {"fuerza": 3.44, "color": "#ff5252", "desc": "Altamente ambicioso. Induce polaridad, dipolos y puentes de hidrógeno. Esencial en Carbohidratos, Proteínas y Ácidos Nucleicos."},
    "Nitrógeno (N)": {"fuerza": 3.04, "color": "#33d9b2", "desc": "Estructurador de aminoácidos y bases nitrogenadas. Define la identidad de Proteínas y Ácidos Nucleicos."},
    "Azufre (S)": {"fuerza": 2.58, "color": "#ffda79", "desc": "Elemento de soporte y rigidez tridimensional. Exclusivo de Proteínas (Puentes disulfuro)."},
    "Carbono (C)": {"fuerza": 2.55, "color": "#ffb142", "desc": "El esqueleto covalente universal. Presente en el 100% de Carbohidratos, Lípidos, Proteínas y Ácidos Nucleicos."},
    "Hidrógeno (H)": {"fuerza": 2.20, "color": "#00e5ff", "desc": "Saturador de cadenas hidrofóbicas en Lípidos y estabilizador conformacional de hélices orgánicas."},
    "Fósforo (P)": {"fuerza": 2.19, "color": "#ff7ff5", "desc": "Almacenador de alta energía (ATP) y esqueleto estructural de los Ácidos Nucleicos (ADN/ARN)."}
}

PREGUNTAS_DESAFIO = [
    {
        "id": 1,
        "pregunta": "1. [JERARQUÍA: LÍPIDOS] Las cadenas de los ácidos grasos están formadas casi exclusivamente por Carbono (2.55) e Hidrógeno (2.20). Al experimentar en el reactor, vemos que su diferencia es menor a 0.4. ¿Cuál es la propiedad resultante en los lípidos celulares?",
        "opciones": ["Son altamente polares e hidrofílicos, disolviéndose en el plasma.", "Son apolares e hidrofóbicos, ideales para formar membranas celulares aislantes."],
        "correcta": "Son apolares e hidrofóbicos, ideales para formar membranas celulares aislantes."
    },
    {
        "id": 2,
        "pregunta": "2. [JERARQUÍA: PROTEÍNAS] El enlace peptídico une covalentemente un Carbono (2.55) con un Nitrógeno (3.04). Al analizar el Espectrómetro, ¿cómo se distribuye la densidad electrónica en este pilar proteico?",
        "opciones": ["Se genera un dipolo local (Polar) debido a que el Nitrógeno atrae con mayor fuerza los electrones.", "Se comparte de forma 100% idéntica (Apolar) porque las fuerzas se cancelan en el espacio."],
        "correcta": "Se genera un dipolo local (Polar) debido a que el Nitrógeno atrae con mayor fuerza los electrones."
    },
    {
        "id": 3,
        "pregunta": "3. [JERARQUÍA: ÁCIDOS NUCLEICOS] La columna vertebral del ADN requiere enlaces de alta energía Fósforo-Oxígeno. Con una diferencia de fuerza crítica de 1.25 ($3.44 - 2.19$), estos enlaces se caracterizan por:",
        "opciones": ["Ser fuertemente polares, acumulando tensiones de carga ideales para la transferencia de energía.", "Ser enlaces apolares e inertes, lo que impide la duplicación del material genético."],
        "correcta": "Ser fuertemente polares, acumulando tensiones de carga ideales para la transferencia de energía."
    },
    {
        "id": 4,
        "pregunta": "4. [JERARQUÍA: CARBOHIDRATOS] Los azúcares como la glucosa poseen múltiples grupos oxhidrilo (-OH) donde el Oxígeno (3.44) se une al Hidrógeno (2.20). ¿Por qué la glucosa es el combustible rápido del plasma sanguíneo?",
        "opciones": ["Porque el enlace O-H es altamente polar, permitiendo que el agua del plasma la disuelva de inmediato.", "Porque la geometría simétrica del O-H repele el agua, obligando a la glucosa a precipitar."],
        "correcta": "Porque el enlace O-H es altamente polar, permitiendo que el agua del plasma la disuelva de inmediato."
    },
    {
        "id": 5,
        "pregunta": "5. [JERARQUÍA: PROTEÍNAS AVANZADAS] Para estabilizar la insulina, se requiere unir dos átomos del mismo elemento: Azufre (2.58) con Azufre (2.58). ¿Qué estatus arrojará el reactor para este puente disulfuro?",
        "opciones": ["Enlace Covalente Homogéneo No Polar (Diferencia = 0.0), mecánicamente rígido y simétrico.", "Enlace Iónico Crítico con colapso de dipolos estables."],
        "correcta": "Enlace Covalente Homogéneo No Polar (Diferencia = 0.0), mecánicamente rígido y simétrico."
    }
]

# --- MOTOR DE GRÁFICOS VECTORIALES DINÁMICOS ---
def generar_svg_enlace(nombre1, fuerza1, color1, nombre2, fuerza2, color2):
    diff = abs(fuerza1 - fuerza2)
    sym = "O" if "Oxígeno" in nombre1 else ("N" if "Nitrógeno" in nombre1 else ("S" if "Azufre" in nombre1 else ("C" if "Carbono" in nombre1 else ("P" if "Fósforo" in nombre1 else "H"))))
    sym2 = "O" if "Oxígeno" in nombre2 else ("N" if "Nitrógeno" in nombre2 else ("S" if "Azufre" in nombre2 else ("C" if "Carbono" in nombre2 else ("P" if "Fósforo" in nombre2 else "H"))))
    
    if diff == 0:
        cx_e1, cx_e2 = 113, 127
        ellipse_x, ellipse_w = 120, 65
        stroke_color = "#ffffff"
        stroke_dash = "2 2"
    elif diff > 0.8:
        cx_e1, cx_e2 = 85, 95 if fuerza1 > fuerza2 else 145, 155
        ellipse_x, ellipse_w = 100 if fuerza1 > fuerza2 else 140, 70
        stroke_color = color1 if fuerza1 > fuerza2 else color2
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
            <text x="64" y="65" fill="black" font-weight="bold" font-family="sans-serif" font-size="14">{sym}</text>
            <circle cx="170" cy="60" r="18" fill="{color2}" opacity="0.85"/>
            <text x="164" y="64" fill="black" font-weight="bold" font-family="sans-serif" font-size="12">{sym2}</text>
            <ellipse cx="{ellipse_x}" cy="60" rx="{ellipse_w}" ry="32" fill="none" stroke="{stroke_color}" stroke-width="1.5" stroke-dasharray="{stroke_dash}"/>
            <circle cx="{cx_e1}" cy="60" r="4" fill="#ffffff"/>
            <circle cx="{cx_e2}" cy="60" r="4" fill="#ffffff"/>
        </svg>
    </div>
    """

def generar_svg_induccion(fuerza_fase0):
    if fuerza_fase0 >= 3.0:
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
    else:
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

# --- INYECCIÓN DE ESTILOS CSS (EL UNIVERSO CÓSMICO PREMIUM) ---
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

# CONTROL DEL MOTOR DE ESTADOS COMPARTIDOS
CODIGOS_VIGENTES = ["SYNAPSIS-PRO", "VET-BIOQUIMICA-2026", "MED-ELITE-30DAYS"]
if "autenticado" not in st.session_state: st.session_state["autenticado"] = False
if "vidas" not in st.session_state: st.session_state["vidas"] = 3
if "puntos" not in st.session_state: st.session_state["puntos"] = 0
if "bloque_actual" not in st.session_state: st.session_state["bloque_actual"] = 0 
if "sim_ejecutada" not in st.session_state: st.session_state["sim_ejecutada"] = False
if "sim_html" not in st.session_state: st.session_state["sim_html"] = ""
if "sim_status" not in st.session_state: st.session_state["sim_status"] = ""
if "sim_output" not in st.session_state: st.session_state["sim_output"] = ""
if "sim_error" not in st.session_state: st.session_state["sim_error"] = False

# ========================================================
# --- ACCESO AL LABORATORIO PÚBLICO ---
# ========================================================
if not st.session_state["autenticado"]:
    st.markdown("<h1 class='main-title'>Chonps<span class='main-title-suffix'>Lab Pro</span></h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Simulador Avanzado de Bioquímica e Interacción Atómica</p>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='bio-panel'>
        <span class='panel-hook'>El Alfabeto de la Vida: Ecosistema CHONPS</span>
        <p class='panel-text'>
            Carbono (C), Hidrógeno (H), Oxígeno (O), Nitrógeno (N), Fósforo (P) y Azufre (S). Estos seis elementos construyen el 99% de la materia viva en el planeta. Sincroniza tu entorno analítico para regular sus fuerzas de enlace y comprender cómo estructuran la jerarquía molecular.
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
# --- CONSOLA PRIVADA DE SIMULACIÓN ---
# ========================================================
else:
    st.markdown("""
    <div class='console-header'>
        <h2 style='margin:0; color: #00e5ff; font-weight: 700;'>ChonpsLab: Consola Analítica Profesional</h2>
        <span style='color: #90a4ae; font-size: 0.85rem;'>Ecosistema de Ciencias de la Salud Protegido</span>
    </div>
    """, unsafe_allow_html=True)
    
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
            <div class='spectrometer-title' style='color:#f44336;'>Falla de Memoria Homeostática</div>
            Reactor bloqueado debido a colapso conceptual clínico en el medio interno.
        </div>
        """, unsafe_allow_html=True)
        if st.button("Reiniciar Sistema y Reactivos", use_container_width=True):
            st.session_state.vidas = 3
            st.session_state.puntos = 0
            st.session_state.bloque_actual = 0
            st.session_state.sim_ejecutada = False
            st.rerun()
    else:
        # --------------------------------------------------------
        # --- FASE 0: CALENTAMIENTO E INTUICIÓN DE CHONPS ---
        # --------------------------------------------------------
        if st.session_state.bloque_actual == 0:
            st.subheader("Fase 0: Inducción a los 6 Elementos Vitales")
            st.write("Mueve el control deslizante para comprender de forma física la **Electronegatividad (Fuerza de atracción)** en la escala de Pauling.")
            
            fuerza_fase0 = st.slider("Ajustar Fuerza de Atracción Electrónica:", 0.7, 4.0, 2.2, step=0.1)
            if fuerza_fase0 >= 3.0:
                st.info("⚡ **Átomo de Alta Fuerza (Ej: Oxígeno: 3.44 o Nitrógeno: 3.04).** Rompe la simetría molecular, induce polaridad y es el imán que permite la hidrofilia celular.")
            else:
                st.success("🤝 **Átomo de Fuerza Balanceada/Baja (Ej: Carbono: 2.55, Azufre: 2.58, Hidrógeno: 2.20, Fósforo: 2.19).** Comparte electrones equitativamente.")
            
            st.components.v1.html(generar_svg_induccion(fuerza_fase0), height=110, scrolling=False)
            
            st.write("---")
            st.markdown("### El Mapa de Identidad de los Ladrillos de la Vida")
            for el, info in ELEMENTOS.items():
                st.markdown(f"**<span style='color:{info['color']};'>{el}</span> (Fuerza: {info['fuerza']}):** {info['desc']}", unsafe_allow_html=True)
            
            st.write("---")
            st.write("**Reto de Nivelación:** Si unes Carbono (2.55) e Hidrógeno (2.20) para formar el esqueleto de un Lípido, sus fuerzas están muy balanceadas. ¿Cómo será la nube electrónica?")
            resp_f0 = st.radio("Elige tu hipótesis académica:", ["Será simétrica y No Polar, repeliendo el agua", "Será asimétrica y Polar, disolviéndose al instante"])
            
            if st.button("Validar Entrada al Laboratorio", use_container_width=True):
                if "No Polar" in resp_f0:
                    st.balloons()
                    st.session_state.puntos += 50
                    st.session_state.bloque_actual = 1
                    st.rerun()
                else:
                    st.error("Error de inducción. Fuerzas similares equivalen a un reparto justo (No Polar). Revisa el mapa de calor.")

        # --------------------------------------------------------
        # --- FASE 1: SIMULADOR MACRO CHONPS AVANZADO ---
        # --------------------------------------------------------
        elif st.session_state.bloque_actual == 1:
            st.subheader("Fase 1: Reactor de Macromoléculas Orgánicas")
            st.write("Combina libremente cualquiera de los 6 elementos biológicos esenciales para analizar la física de sus uniones.")
            
            col1, col2 = st.columns(2)
            with col1:
                e1 = st.selectbox("Átomo Central (Núcleo A):", list(ELEMENTOS.keys()))
            with col2:
                e2 = st.selectbox("Átomo de Reacción (Núcleo B):", list(ELEMENTOS.keys()))
                
            if st.button("Sintetizar Enlace Molecular", use_container_width=True):
                st.session_state.sim_ejecutada = True
                f1, fill1 = ELEMENTOS[e1]["fuerza"], ELEMENTOS[e1]["color"]
                f2, fill2 = ELEMENTOS[e2]["fuerza"], ELEMENTOS[e2]["color"]
                diff = abs(f1 - f2)
                
                st.session_state.sim_html = generar_svg_enlace(e1, f1, fill1, e2, f2, fill2)
                
                if diff == 0:
                    st.session_state.sim_status = "Enlace Covalente Homogéneo No Polar (Simetría Total)"
                    st.session_state.sim_output = f"Unión molecular estable entre elementos idénticos. La diferencia de fuerza es 0.0. Los electrones rotan exactamente en medio de ambos núcleos. Estructura uniones homonocleares como el enlace Azufre-Azufre de los puentes disulfuro proteicos esenciales."
                    st.session_state.sim_error = False
                    st.session_state.puntos += 100
                elif diff <= 0.4:
                    st.session_state.sim_status = "Enlace Covalente No Polar (Hidrofóbico)"
                    st.session_state.sim_output = f"Estabilidad electroquímica óptima. La diferencia de fuerza es de {diff:.2f} (menor a 0.4). Los átomos comparten electrones equitativamente. Configuración clave para formar estructuras insolubles en agua, como las cadenas de ácidos grasos en Lípidos."
                    st.session_state.sim_error = False
                    st.session_state.puntos += 100
                elif diff < 1.7:
                    st.session_state.sim_status = "Enlace Covalente Polar (Dipolo Activo - Hidrófilo)"
                    st.session_state.sim_output = f"Asimetría orbital detectada. La diferencia de fuerza es de {diff:.2f}. El elemento con mayor electronegatividad jala el par electrónico hacia su zona, induciendo una carga parcial negativa y dejando una carga parcial positiva en el opuesto. Esto genera la solubilidad en Carbohidratos y puentes hídricos."
                    st.session_state.sim_error = False
                    st.session_state.puntos += 120
                else:
                    st.session_state.sim_status = "Tensión Iónica / Ruptura de Estabilidad"
                    st.session_state.sim_output = f"Diferencia de atracción crítica ({diff:.2f}). Genera un estrés de dipolos extremos, común en grupos fosfato altamente inestables y reactivos, pilar de los enlaces fosfodiéster en Ácidos Nucleicos y transferencia energética en el ATP."
                    st.session_state.sim_error = True
                    st.session_state.vidas -= 1
                st.rerun()
                
            if st.session_state.sim_ejecutada:
                st.write("---")
                card_class = "spectrometer-card-error" if st.session_state.sim_error else "spectrometer-card-success"
                title_color = "#ff5252" if st.session_state.sim_error else "#69f0ae"
                
                st.markdown(f"""
                <div class='{card_class}'>
                    <div class='spectrometer-title' style='color:{title_color};'>Lectura del Espectrómetro Cuántico</div>
                    <strong style='font-size:1.15rem; color:#ffffff;'>Estatus del Sistema: {st.session_state.sim_status}</strong><br><br>
                    <p style='color:#cfd8dc; margin:0;'>{st.session_state.sim_output}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.components.v1.html(st.session_state.sim_html, height=135, scrolling=False)
                if st.button("Limpiar Cámara de Reacción", use_container_width=True):
                    st.session_state.sim_ejecutada = False
                    st.rerun()

        # --------------------------------------------------------
        # --- FASE 2: EXAMEN DE DESAFÍO BASADO EN JERARQUÍAS ---
        # --------------------------------------------------------
        elif st.session_state.bloque_actual == 2:
            st.subheader("Fase 2: Desafío de Validación de Macromoléculas")
            st.write("Responde correctamente a este cuestionario de alta exigencia académica basado en la jerarquía bioquímica celular. ¡Equivocarse cuesta una vida!")
            
            with st.form("banco_preguntas_chonps"):
                respuestas_usuario = {}
                for item in PREGUNTAS_DESAFIO:
                    st.markdown(f"<p style='font-weight:600; color:#ffffff; margin-bottom:5px;'>{item['pregunta']}</p>", unsafe_allow_html=True)
                    respuestas_usuario[item["id"]] = st.radio(f"Opciones para pregunta {item['id']}:", item["opciones"], label_visibility="collapsed")
                    st.write("")
                
                boton_evaluar = st.form_submit_button("Enviar Hoja de Respuestas Científica", use_container_width=True)
                
                if boton_evaluar:
                    errores = 0
                    for item in PREGUNTAS_DESAFIO:
                        if respuestas_usuario[item["id"]] != item["correcta"]:
                            errores += 1
                    
                    if errores == 0:
                        st.balloons()
                        st.success("🏆 ¡EXAMEN PERFECTO! Has dominado el ecosistema CHONPS y la jerarquía de las macromoléculas con rigor de experto. El software está validado.")
                        st.session_state.puntos += 500
                    else:
                        st.session_state.vidas -= 1
                        st.error(f"❌ Examen reprobado con {errores} error(es) analítico(s). Has perdido 1 Vida debido a inestabilidad conceptual. Estudia las interacciones atómicas.")
                        time.sleep(1.5)
                        st.rerun()
