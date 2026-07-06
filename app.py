import streamlit as st
import time

# 1. CONFIGURACIÓN DEL ENTORNO DE SIMULACIÓN NATIVA
st.set_page_config(page_title="ChonpsLab Pro", page_icon="⚛️", layout="centered")

# --- BANCO DE DATOS MAESTRO (PROPIEDADES BIOLÓGICAS DE CHONPS) ---
ELEMENTOS = {
    "Oxígeno (O)": {"fuerza": 3.44, "color": "#ff5252", "desc": "Altamente ambicioso. Induce polaridad e hidrofilia celular."},
    "Nitrógeno (N)": {"fuerza": 3.04, "color": "#33d9b2", "desc": "Clave en aminoácidos y bases nitrogenadas. Genera dipolos fuertes."},
    "Azufre (S)": {"fuerza": 2.58, "color": "#ffda79", "desc": "Estabilizador proteico mediante puentes disulfuro moleculares."},
    "Carbono (C)": {"fuerza": 2.55, "color": "#ffb142", "desc": "El esqueleto de la materia viva. Enlaces estables y versátiles."},
    "Hidrógeno (H)": {"fuerza": 2.20, "color": "#00e5ff", "desc": "Donador universal de protones y estabilizador de puentes hídricos."},
    "Fósforo (P)": {"fuerza": 2.19, "color": "#dm12ff", "desc": "Esencial para los enlaces de alta energía (ATP) y ácidos nucleicos."}
}

PREGUNTAS_DESAFIO = [
    {
        "id": 1,
        "pregunta": "1. Al unir Nitrógeno (3.04) con Carbono (2.55) para formar el enlace peptídico de una proteína, ¿qué sucede con los electrones?",
        "opciones": ["Se comparten de forma idéntica y simétrica (Apolar)", "Se desplazan con mayor densidad hacia el Nitrógeno debido a su mayor fuerza (Polar)"],
        "correcta": "Se desplazan con mayor densidad hacia el Nitrógeno debido a su mayor fuerza (Polar)"
    },
    {
        "id": 2,
        "pregunta": "2. En los puentes disulfuro que estabilizan la estructura de la insulina, se enlazan dos átomos de Azufre (2.58 - 2.58 = 0). ¿Qué tipo de enlace resulta?",
        "opciones": ["Enlace Covalente No Polar (Simétrico)", "Enlace Covalente Polar (Asimétrico)"],
        "correcta": "Enlace Covalente No Polar (Simétrico)"
    },
    {
        "id": 3,
        "pregunta": "3. Los enlaces de alta energía del ATP involucran uniones Fósforo-Oxígeno. Con una diferencia de fuerza de 1.25 ($3.44 - 2.19$), este enlace es:",
        "opciones": ["Fuertemente Polar, acumulando tensiones de carga", "Totalmente Apolar, liberando calor espontáneo"],
        "correcta": "Fuertemente Polar, acumulando tensiones de carga"
    },
    {
        "id": 4,
        "pregunta": "4. ¿Cuál de los 6 bioelementos del ecosistema CHONPS tiene la mayor capacidad para romper la neutralidad de una molécula orgánica e inducir hidrofilia?",
        "opciones": ["El Carbono (C)", "El Oxígeno (O)"],
        "correcta": "El Oxígeno (O)"
    },
    {
        "id": 5,
        "pregunta": "5. Si un par de átomos tiene una diferencia de electronegatividad menor a 0.4 en la escala de Pauling, ¿cuál es la consecuencia biofísica de la molécula?",
        "opciones": ["Se vuelve hidrofóbica e insoluble en agua (Apolar)", "Se disocia inmediatamente liberando protones de pH"],
        "correcta": "Se vuelve hidrofóbica e insoluble en agua (Apolar)"
    }
]

# --- MOTOR DE GRÁFICOS VECTORIALES DINÁMICOS (OPTIMIZADO EN RAM) ---
def generar_svg_enlace(nombre1, fuerza1, color1, nombre2, fuerza2, color2):
    diff = abs(fuerza1 - fuerza2)
    sym = "O" if "Oxígeno" in nombre1 else ("N" if "Nitrógeno" in nombre1 else ("S" if "Azufre" in nombre1 else ("C" if "Carbono" in nombre1 else ("P" if "Fósforo" in nombre1 else "H"))))
    sym2 = "O" if "Oxígeno" in nombre2 else ("N" if "Nitrógeno" in nombre2 else ("S" if "Azufre" in nombre2 else ("C" if "Carbono" in nombre2 else ("P" if "Fósforo" in nombre2 else "H"))))
    
    # Parámetros visuales reactivos según la diferencia de fuerza
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

# --- INYECCIÓN DE ESTILOS CSS AVANZADOS (UNIVERSO NEGRO ABSOLUTO) ---
st.markdown("""
<style>
    .stApp { background-color: #000000 !important; }
    .main-title { text-align: center; color: #ffffff; font-size: 3.2rem; font-weight: 800; font-family: 'Segoe UI', sans-serif; margin-bottom: 0px; }
    .main-title-suffix { color: #00e5ff; font-weight: 300; }
    .sub-title { text-align: center; font-style: italic; color: #90a4ae; font-size: 1.05rem; margin-top: 5px; margin-bottom: 25px; }
    .bio-panel { background-color: rgba(30, 41, 59, 0.5); border: 1px solid rgba(0, 229, 255, 0.2); border-left: 5px solid #00e5ff; padding: 20px; border-radius: 8px; margin-bottom: 25px; }
    .spectrometer-card-success { background-color: rgba(76, 175, 80, 0.08); border: 1px solid rgba(76, 175, 80, 0.25); border-left: 6px solid #4caf50; padding: 18px; border-radius: 6px; margin-top: 15px; }
    .spectrometer-card-error { background-color: rgba(244, 67, 54, 0.08); border: 1px solid rgba(244, 67, 54, 0.25); border-left: 6px solid #f44336; padding: 18px; border-radius: 6px; margin-top: 15px; }
    .sidebar-monitor { background-color: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); padding: 12px; border-radius: 4px; margin-bottom: 10px; text-align: center; }
</style>
""", unsafe_allow_html=True)

# CONTROL DEL MOTOR DE ESTADOS COMPARTIDOS
CODIGOS_VIGENTES = ["SYNAPSIS-PRO", "VET-BIOQUIMICA-2026", "MED-ELITE-30DAYS"]
if "autenticado" not in st.session_state: st.session_state["autenticado"] = False
if "vidas" not in st.session_state: st.session_state["vidas"] = 3
if "puntos" not in st.session_state: st.session_state["puntos"] = 0
if "bloque_actual" not in st.session_state: st.session_state["bloque_actual"] = 0  # 0:Inducción, 1:Simulador CHONPS, 2:Desafío de las 5 Preguntas
if "sim_ejecutada" not in st.session_state: st.session_state["sim_ejecutada"] = False
if "sim_html" not in st.session_state: st.session_state["sim_html"] = ""
if "sim_status" not in st.session_state: st.session_state["sim_status"] = ""
if "sim_output" not in st.session_state: st.session_state["sim_output"] = ""
if "sim_error" not in st.session_state: st.session_state["sim_error"] = False

# ========================================================
# --- AUTENTICACIÓN PÚBLICA ---
# ========================================================
if not st.session_state["autenticado"]:
    st.markdown("<h1 class='main-title'>Chonps<span class='main-title-suffix'>Lab Pro</span></h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Simulador Avanzado de Bioquímica e Interacción Atómica</p>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='bio-panel'>
        <span style='color:#00e5ff; font-weight:700; font-size:1.2rem; display:block; margin-bottom:5px;'>Ecosistema de Bioelementos Expandido</span>
        <p style='color:#cfd8dc; margin:0; font-size:0.95rem; line-height:1.5;'>
            Bienvenido al entorno analítico optimizado. Esta versión integra la totalidad de las macromoléculas biológicas (CHONPS), permitiendo modelar desde enlaces de agua hasta puentes disulfuro y esqueletos de nucleótidos.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    codigo_input = st.text_input("Licencia de Acceso Digital (Token Único):", type="password", placeholder="Introduce tu clave premium...")
    if st.button("Encender Reactores Computacionales", use_container_width=True):
        if codigo_input.strip().upper() in CODIGOS_VIGENTES:
            st.session_state["autenticado"] = True
            st.rerun()
        else:
            st.error("Token inválido. Verifica tu suscripción.")

# ========================================================
# --- ENTORNO PRIVADO DE APRENDIZAJE ---
# ========================================================
else:
    st.markdown("<h2 style='color:#00e5ff; font-weight:700; margin-bottom:20px;'>ChonpsLab: Consola Analítica Profesional</h2>", unsafe_allow_html=True)
    
    # Barra Lateral Estructural
    with st.sidebar:
        st.markdown("<h3 style='font-weight:600;'>Monitor de Progreso</h3>", unsafe_allow_html=True)
        st.markdown(f"<div class='sidebar-monitor'><span style='color:#90a4ae; font-size:0.8rem;'>Estabilidad de Vidas</span><br><b style='font-size:1.5rem; color:#f44336;'>{st.session_state.vidas} / 3</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='sidebar-monitor'><span style='color:#90a4ae; font-size:0.8rem;'>Puntaje Acumulado</span><br><b style='font-size:1.5rem; color:#00e5ff;'>{st.session_state.puntos} pts</b></div>", unsafe_allow_html=True)
        
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
        if st.button("Fase 2: El Examen de las 5 Preguntas", use_container_width=True):
            st.session_state.bloque_actual = 2
            st.rerun()
            
        st.write("---")
        if st.button("Desconectar Laboratorio", use_container_width=True):
            st.session_state["autenticado"] = False
            st.rerun()

    if st.session_state.vidas <= 0:
        st.markdown("<div class='spectrometer-card-error'><strong style='color:#f44336;'>Falla de Memoria Homeostática:</strong> Reactor bloqueado por colapso metabólico clínico.</div>", unsafe_allow_html=True)
        if st.button("Reiniciar Sistema y Reactivos", use_container_width=True):
            st.session_state.vidas = 3
            st.session_state.puntos = 0
            st.session_state.bloque_actual = 0
            st.session_state.sim_ejecutada = False
            st.rerun()
    else:
        # --------------------------------------------------------
        # --- FASE 0: CALENTAMIENTO E INTUICIÓN ---
        # --------------------------------------------------------
        if st.session_state.bloque_actual == 0:
            st.subheader("Fase 0: Inducción Electronegativa")
            st.write("Mueve el control deslizante para comprender cómo la fuerza atómica (Electronegatividad) jala las nubes de electrones.")
            
            fuerza_fase0 = st.slider("Ajustar Fuerza (Escala Pauling):", 0.7, 4.0, 2.2, step=0.1)
            if fuerza_fase0 >= 3.0:
                st.info("⚡ **Átomo Ambicioso (Ej: Oxígeno o Nitrógeno).** Deforma la geometría molecular y atrae las cargas hacia sí.")
            else:
                st.success("🤝 **Átomo Equilibrado (Ej: Carbono o Hidrógeno).** Distribuye y comparte los electrones con justicia orbital.")
            
            st.write("---")
            st.write("**Reto de Nivelación:** Si el Carbono (2.55) y el Azufre (2.58) se unen, sus fuerzas están prácticamente empatadas. ¿Cómo se comportará su enlace?")
            resp_f0 = st.radio("Elige tu hipótesis:", ["Será un enlace simétrico y No Polar", "Será un enlace asimétrico altamente Polar"])
            
            if st.button("Validar Entrada al Laboratorio", use_container_width=True):
                if "No Polar" in resp_f0:
                    st.balloons()
                    st.session_state.puntos += 50
                    st.session_state.bloque_actual = 1
                    st.rerun()
                else:
                    st.error("Error analítico. Fuerzas similares equivalen a un reparto justo (No Polar). Revisa el concepto.")

        # --------------------------------------------------------
        # --- FASE 1: SIMULADOR MACRO CHONPS AVANZADO ---
        # --------------------------------------------------------
        elif st.session_state.bloque_actual == 1:
            st.subheader("Fase 1: Reactor de Macromoléculas Orgánicas")
            st.write("Combina libremente cualquiera de los 6 elementos biológicos esenciales para analizar la física cuántica de sus enlaces.")
            
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
                    st.session_state.sim_output = f"Unión molecular estable entre elementos idénticos. La diferencia de fuerza es 0.0. Los electrones rotan exactamente en medio de ambos núcleos. Estructura el gas respiratorio o uniones homonucleares (como el enlace Azufre-Azufre de los puentes disulfuro)."
                    st.session_state.sim_error = False
                    st.session_state.puntos += 100
                elif diff <= 0.4:
                    st.session_state.sim_status = "Enlace Covalente No Polar (Hidrofóbico)"
                    st.session_state.sim_output = f"Estabilidad electroquímica óptima. La diferencia de fuerza es de {diff:.2f} (menor a 0.4). Los átomos comparten electrones equitativamente. Configuración clave para formar estructuras insolubles en agua, como los anillos de carbono y cadenas de ácidos grasos."
                    st.session_state.sim_error = False
                    st.session_state.puntos += 100
                elif diff < 1.7:
                    st.session_state.sim_status = "Enlace Covalente Polar (Dipolo Activo - Hidrófilo)"
                    st.session_state.sim_output = f"Asimetría orbital detectada. La diferencia de fuerza es de {diff:.2f}. El elemento con mayor electronegatividad jala el par electrónico hacia su zona, induciendo una carga parcial negativa ($\delta^-$) y dejando una carga parcial positiva ($\delta^+$) en el opuesto. Esto genera la solubilidad y los puentes de hidrógeno indispensables para la vida."
                    st.session_state.sim_error = False
                    st.session_state.puntos += 120
                else:
                    st.session_state.sim_status = "Tensión Iónica / Ruptura de Estabilidad"
                    st.session_state.sim_output = f"Diferencia de atracción crítica ({diff:.2f}). Aunque sigue considerándose covalente en el marco orgánico, la distribución es tan desigual que genera un estrés de dipolos extremos, común en grupos fosfato altamente inestables y reactivos (esencia de la transferencia energética en el ATP)."
                    st.session_state.sim_error = True
                    st.session_state.vidas -= 1
                st.rerun()
                
            # Renderizado del resultado de simulación retenido en el estado
            if st.session_state.sim_ejecutada:
                st.write("---")
                card_class = "spectrometer-card-error" if st.session_state.sim_error else "spectrometer-card-success"
                st.markdown(f"""
                <div class='{card_class}'>
                    <div style='font-size:0.85rem; text-transform:uppercase; font-weight:700; color:#b0bec5; letter-spacing:0.5px;'>Lectura del Espectrómetro Cuántico</div>
                    <strong style='font-size:1.15rem;'>Estatus del Sistema: {st.session_state.sim_status}</strong><br><br>
                    {st.session_state.sim_output}
                </div>
                """, unsafe_allow_html=True)
                
                st.components.v1.html(st.session_state.sim_html, height=135, scrolling=False)
                if st.button("Limpiar Cámara de Reacción"):
                    st.session_state.sim_ejecutada = False
                    st.rerun()

        # --------------------------------------------------------
        # --- FASE 2: EXAMEN DE DESAFÍO DE 5 PREGUNTAS ---
        # --------------------------------------------------------
        elif st.session_state.bloque_actual == 2:
            st.subheader("Fase 2: Desafío de Validación Científica")
            st.write("Responde correctamente a este cuestionario de alta exigencia académica basado en las lecturas analíticas que has aprendido en el laboratorio. ¡Equivocarse cuesta una vida!")
            
            with st.form("banco_preguntas_chonps"):
                respuestas_usuario = {}
                for item in PREGUNTAS_DESAFIO:
                    st.markdown(f"<p style='font-weight:600; color:#ffffff; margin-bottom:5px;'>{item['pregunta']}</p>", unsafe_allow_html=True)
                    respuestas_usuario[item["id"]] = st.radio(f"Opciones para pregunta {item['id']}:", item["opciones"], label_visibility="collapsed")
                    st.write("")
                
                boton_evaluar = st.form_submit_with_rows_choices = st.form_submit_button("Enviar Hoja de Respuestas Científica", use_container_width=True)
                
                if boton_evaluar:
                    errores = 0
                    for item in PREGUNTAS_DESAFIO:
                        if respuestas_usuario[item["id"]] != item["correcta"]:
                            errores += 1
                    
                    if errores == 0:
                        st.balloons()
                        st.success("🏆 ¡EXAMEN PERFECTO! Has dominado el ecosistema CHONPS con rigor de experto. Tus conocimientos están listos para la validación de mercado.")
                        st.session_state.puntos += 500
                    else:
                        st.session_state.vidas -= 1
                        st.error(f"❌ Examen reprobado con {errores} error(es) analítico(s). Has perdido 1 Vida debido a inestabilidad conceptual. El conocimiento requiere precisión.")
                        time.sleep(1.5)
                        st.rerun()
