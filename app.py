import streamlit as st
import time

# ========================================================
# 1. CONFIGURACIÓN DEL CHASIS Y ESTÉTICA CÓSMICA
# ========================================================
st.set_page_config(page_title="ChonpsLab", page_icon="⚛️", layout="wide")

st.markdown("""
<style>
    /* Chasis Cósmico de Alto Rendimiento (Negro Puro) */
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
    .monitor-box { background-color: rgba(255,255,255,0.05); padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 10px;}
    
    /* Personalización de los Tabs para que parezcan una consola de control */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] { background-color: rgba(255,255,255,0.05); border-radius: 4px 4px 0 0; padding: 10px 20px; color: #90a4ae; font-weight: bold;}
    .stTabs [aria-selected="true"] { background-color: rgba(0, 229, 255, 0.15) !important; color: #00e5ff !important; border-bottom: 2px solid #00e5ff !important; }
</style>
""", unsafe_allow_html=True)

# ========================================================
# 2. BASE DE DATOS MAESTRA CHONPS
# ========================================================
ELEMENTOS = {
    "Carbono (C)": {"fuerza": 2.55, "color": "#ffb142", "sym": "C"},
    "Hidrógeno (H)": {"fuerza": 2.20, "color": "#00e5ff", "sym": "H"},
    "Oxígeno (O)": {"fuerza": 3.44, "color": "#ff5252", "sym": "O"},
    "Nitrógeno (N)": {"fuerza": 3.04, "color": "#33d9b2", "sym": "N"},
    "Fósforo (P)": {"fuerza": 2.19, "color": "#ff7ff5", "sym": "P"},
    "Azufre (S)": {"fuerza": 2.58, "color": "#ffda79", "sym": "S"}
}

# ========================================================
# 3. MOTOR VECTORIAL SVG (LIBRE DE BUGS Y OPTIMIZADO)
# ========================================================
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
    # BUG DE DESEMPAQUETADO SOLUCIONADO (Paréntesis en tuplas)
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
# 4. GESTIÓN DE ESTADOS
# ========================================================
if "auth" not in st.session_state: st.session_state["auth"] = False
if "vidas" not in st.session_state: st.session_state["vidas"] = 3
if "puntos" not in st.session_state: st.session_state["puntos"] = 0

# ========================================================
# 5. PORTADA PRINCIPAL (MARCA PERSONAL RECUPERADA)
# ========================================================
if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>Chonps<span class='main-title-suffix'>Lab</span></h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Tu Laboratorio Digital de Ciencias de la Vida y Biología Molecular</p>", unsafe_allow_html=True)
    st.markdown("""
    <div class='bio-panel'>
        <span style='color:#00e5ff; font-weight:700; font-size:1.25rem;'>Bienvenido a tu suite analítica</span>
        <p style='color:#cfd8dc; margin-top:10px;'>Sincroniza tus credenciales para acceder a la estación de trabajo. Modela la teoría atómica, comprueba las fuerzas electronegativas, interactúa con monosacáridos (epímeros) y estabiliza el pH celular en un solo panel de control integrado.</p>
    </div>
    """, unsafe_allow_html=True)
    
    pwd = st.text_input("Licencia de Acceso (Token Único):", type="password")
    if st.button("Activar Panel Central", use_container_width=True):
        if pwd.strip().upper() in ["SYNAPSIS", "LAB-2026", "CHONPS"]:
            st.session_state["auth"] = True
            st.rerun()
        else:
            st.error("Acceso denegado. Token inválido.")

# ========================================================
# 6. CONSOLA DE LABORATORIO (DASHBOARD ÚNICO MEDIANTE TABS)
# ========================================================
else:
    # Encabezado Central
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown("<h2 style='color:#00e5ff; margin-top:0;'>Consola de Operaciones: ChonpsLab</h2>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='monitor-box'><span style='color:#90a4ae; font-size:12px;'>ESTABILIDAD DEL SISTEMA (VIDAS)</span><br><b style='font-size:20px; color:#f44336;'>{st.session_state.vidas} / 3 💔</b></div>", unsafe_allow_html=True)

    if st.session_state.vidas <= 0:
        st.error("🚨 COLAPSO METABÓLICO: Te has quedado sin vidas. El laboratorio se reiniciará para evitar daños estructurales.")
        if st.button("Restaurar Parámetros de Laboratorio"):
            st.session_state.vidas = 3
            st.session_state.puntos = 0
            st.rerun()
    else:
        # Sistema de Pestañas Fluidas
        tabs = st.tabs([
            "🏛️ Módulo 1: Teoría Atómica", 
            "⚡ Módulo 2: Estira y Afloja (CHONPS)", 
            "🧬 Módulo 3: Reactores de Enlace", 
            "🍬 Módulo 4: Glucómica y Epímeros", 
            "🌡️ Módulo 5: Titulación de pH", 
            "🏆 Desafío Final"
        ])

        # ----------------------------------------------------
        # MÓDULO 1: TEORÍA ATÓMICA
        # ----------------------------------------------------
        with tabs[0]:
            st.markdown("### El Origen de la Materia")
            st.write("Antes de ensamblar macromoléculas, analiza la evolución de la estructura atómica según los registros documentales de Bioquímica Básica.")
            
            modelo = st.select_slider(
                "Viaja en el tiempo de la física cuántica:",
                options=["Dalton (1810)", "Thomson (1897)", "Rutherford (1911)", "Bohr (1913)", "Schrödinger (1926)"]
            )
            
            if "Dalton" in modelo:
                st.info("⚛️ **John Dalton (1810):** El átomo como una esfera sólida indivisible. Los átomos del mismo elemento tienen igual masa. El reordenamiento de los átomos equivale a una reacción química.")
            elif "Thomson" in modelo:
                st.info("⚛️ **J.J. Thomson (1897):** Modelo del 'Pudin de pasas'. Incorpora electrones incrustados dentro de una esfera atómica cargada con electricidad positiva.")
            elif "Rutherford" in modelo:
                st.info("⚛️ **Ernest Rutherford (1911):** Demostró que los átomos están mayormente huecos, con un núcleo denso y muy pesado en el centro rodeado de electrones.")
            elif "Bohr" in modelo:
                st.info("⚛️ **Niels Bohr (1913):** Sugirió niveles cuantizados de energía. El electrón gira alrededor del núcleo en órbitas circulares definidas con una energía específica.")
            else:
                st.info("⚛️ **Erwin Schrödinger (1926):** Modelo Cuántico. Los electrones no tienen órbitas fijas, sino 'orbitales' que son nubes de probabilidad máxima descritas por los números cuánticos (n, l, m).")

        # ----------------------------------------------------
        # MÓDULO 2: ESTIRA Y AFLOJA
        # ----------------------------------------------------
        with tabs[1]:
            st.markdown("### Electronegatividad: El Estira y Afloja Atómico")
            st.write("La **Electronegatividad** es la fuerza con la que un núcleo atrae hacia sí los electrones compartidos en un enlace. Ajusta el control para simular la Escala de Linus Pauling.")
            
            fuerza = st.slider("Fuerza de Atracción (Escala Pauling):", 0.7, 4.0, 2.2, 0.1)
            
            st.components.v1.html(generar_svg_tira_afloja(fuerza), height=120, scrolling=False)
            
            if fuerza >= 3.0:
                st.markdown("<div class='card-error'><b>🔥 Átomo Ambicioso (Ej: Oxígeno, Nitrógeno):</b> Tiene el poder de deformar por completo la nube orbital, secuestrando la densidad electrónica hacia su propio núcleo.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='card-success'><b>🤝 Átomo Equilibrado (Ej: Carbono, Hidrógeno, Fósforo, Azufre):</b> Fuerza moderada. Comparte los electrones de forma justa y simétrica, sin romper el balance de cargas.</div>", unsafe_allow_html=True)
                
            st.write("---")
            st.markdown("#### Identidad de los Ladrillos de la Vida (CHONPS)")
            c1, c2, c3 = st.columns(3)
            keys = list(ELEMENTOS.keys())
            for i, col in enumerate([c1, c2, c3]):
                with col:
                    st.markdown(f"**<span style='color:{ELEMENTOS[keys[i*2]]['color']};'>{keys[i*2]}</span> (Fuerza: {ELEMENTOS[keys[i*2]]['fuerza']})**", unsafe_allow_html=True)
                    st.markdown(f"**<span style='color:{ELEMENTOS[keys[i*2+1]]['color']};'>{keys[i*2+1]}</span> (Fuerza: {ELEMENTOS[keys[i*2+1]]['fuerza']})**", unsafe_allow_html=True)

        # ----------------------------------------------------
        # MÓDULO 3: REACTOR DE ENLACES MOLECULARES
        # ----------------------------------------------------
        with tabs[2]:
            st.markdown("### Síntesis de Enlaces (Aplicación de Fuerzas)")
            st.write("Combina elementos del ecosistema CHONPS. El espectrómetro calculará vectorialmente la deformación de la nube.")
            
            c1, c2 = st.columns(2)
            atom1 = c1.selectbox("Átomo Central (A):", list(ELEMENTOS.keys()))
            atom2 = c2.selectbox("Átomo de Reacción (B):", list(ELEMENTOS.keys()))
            
            if st.button("Ensamblar y Analizar Enlace", use_container_width=True):
                a1, a2 = ELEMENTOS[atom1], ELEMENTOS[atom2]
                st.components.v1.html(generar_svg_enlace(a1['sym'], a1['fuerza'], a1['color'], a2['sym'], a2['fuerza'], a2['color']), height=140, scrolling=False)
                
                diff = abs(a1['fuerza'] - a2['fuerza'])
                if diff == 0:
                    st.markdown(f"<div class='card-success'><b>✅ Enlace Covalente No Polar Puro (Diferencia = 0.0):</b> Simetría orbital perfecta. Comparten electrones exactamente al centro. Característico de moléculas elementales gaseosas o Puentes Disulfuro (S-S).</div>", unsafe_allow_html=True)
                elif diff <= 0.4:
                    st.markdown(f"<div class='card-success'><b>✅ Enlace Covalente No Polar (Diferencia = {diff:.2f}):</b> Reparto altamente equitativo. Característico de los hidrocarburos (C-H) que forman las colas hidrofóbicas repeliendo el agua celular.</div>", unsafe_allow_html=True)
                elif diff <= 1.7:
                    st.markdown(f"<div class='card-success' style='border-left-color:#ffb142;'><b>⚡ Enlace Covalente Polar (Diferencia = {diff:.2f}):</b> Formación de dipolos activos. El átomo más fuerte genera una carga parcial negativa ($\delta^-$), induciendo solubilidad y puentes de hidrógeno.</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='card-error'><b>⚠️ Tensión Iónica / Inestabilidad (Diferencia = {diff:.2f}):</b> Transferencia abrupta de densidad electrónica. Genera radicales o estrés molecular alto, clásico en la energía del enlace fosfodiéster.</div>", unsafe_allow_html=True)

        # ----------------------------------------------------
        # MÓDULO 4: GLUCÓMICA Y EPÍMEROS (CARBOHIDRATOS)
        # ----------------------------------------------------
        with tabs[3]:
            st.markdown("### El Código de los Azúcares: Isomerismo y Enlaces O-Glucosídicos")
            st.write("Los monosacáridos son polihidroxi-aldehídos o polihidroxi-cetonas. Un pequeño giro en el espacio (isomerismo) cambia radicalmente cómo las enzimas leen la molécula.")
            
            with st.expander("🔬 Analizador de Epímeros: ¿Glucosa o Galactosa?"):
                st.markdown("La **Glucosa** y la **Galactosa** son **Epímeros en el Carbono 4**. Tienen exactamente la misma fórmula química ($C_6H_{12}O_6$), pero en el C4, el grupo Hidroxilo (-OH) de la glucosa mira hacia la derecha, mientras que en la galactosa mira hacia la izquierda. Las enzimas celulares son estrictas y leen estas formas de manera distinta.")
            
            st.markdown("#### Reactor de Disacáridos")
            st.write("Ensambla dos azúcares retirando una molécula de agua para formar un enlace O-Glucosídico.")
            
            c1, c2 = st.columns(2)
            azu1 = c1.selectbox("Monosacárido 1:", ["Alfa-D-Glucosa", "Beta-D-Galactosa"])
            azu2 = c2.selectbox("Monosacárido 2:", ["Alfa-D-Glucosa", "Beta-D-Fructosa (Cetosa)"])
            
            if st.button("Polimerizar Enlace Glucosídico", use_container_width=True):
                if azu1 == "Alfa-D-Glucosa" and azu2 == "Alfa-D-Glucosa":
                    st.markdown("<div class='card-success'>🌾 <b>MALTOSA SINTETIZADA:</b> Enlace <b>Alfa(1→4)</b>. Es el azúcar de malta, producto directo de la degradación del almidón. Contiene poder reductor por su extremo libre.</div>", unsafe_allow_html=True)
                elif azu1 == "Beta-D-Galactosa" and azu2 == "Alfa-D-Glucosa":
                    st.markdown("<div class='card-success'>🥛 <b>LACTOSA SINTETIZADA:</b> Enlace <b>Beta(1→4)</b>. El azúcar vital de la leche de los mamíferos. Requiere la enzima Lactasa para poder romper la estructura espacial 'Beta'.</div>", unsafe_allow_html=True)
                elif azu1 == "Alfa-D-Glucosa" and azu2 == "Beta-D-Fructosa (Cetosa)":
                    st.markdown("<div class='card-success'>🎋 <b>SACAROSA SINTETIZADA:</b> Enlace <b>Alfa(1) ↔ Beta(2)</b>. El azúcar de caña. Como compromete ambos carbonos anoméricos, <b>no es un azúcar reductor</b>.</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='card-error'>⚠️ <b>Ensamblaje Irregular:</b> La combinación de estos epímeros con estas conformaciones no es una ruta metabólica de alta prioridad fisiológica en mamíferos.</div>", unsafe_allow_html=True)

        # ----------------------------------------------------
        # MÓDULO 5: pH Y BUFFERS
        # ----------------------------------------------------
        with tabs[4]:
            st.markdown("### Control Homeostático: Curvas de Titulación")
            st.write("La vida existe en un rango de pH extremadamente estrecho. Observa cómo responden distintos fluidos ante la invasión agresiva de un ácido fuerte.")
            
            solucion = st.radio("Cámara de Perfusión: Selecciona el medio recipiente", ["Medio A: Agua Destilada Pura (Cero Solutos)", "Medio B: Plasma con Buffer de Bicarbonato / Ácido Acético"])
            
            if st.button("Inyectar 10 mL de Ácido Clorhídrico (HCl)", use_container_width=True):
                if "Agua" in solucion:
                    st.markdown("<div class='card-error'><b>🩸 CHOQUE DE ACIDOSIS:</b> Al no haber un sistema amortiguador, el HCl se disocia al 100% inundando el medio de protones libres ($H^+$). El pH colapsa de 7.0 a 2.0 instantáneamente, causando desnaturalización masiva de proteínas celulares. <b>Pierdes 1 vida.</b></div>", unsafe_allow_html=True)
                    st.session_state.vidas -= 1
                else:
                    st.markdown("<div class='card-success'><b>🛡️ TAMPONAMIENTO EXITOSO:</b> El medio contiene bases conjugadas que atrapan el exceso de protones del HCl, transformándose en ácidos débiles. Esto absorbe el impacto molecular y mantiene el pH en su <b>Región Amortiguadora</b>. La célula sobrevive.</div>", unsafe_allow_html=True)

        # ----------------------------------------------------
        # MÓDULO 6: RETO FINAL (EVALUACIÓN)
        # ----------------------------------------------------
        with tabs[5]:
            st.markdown("### Desafío Final: Matriz de Ciencias Bioquímicas")
            st.write("Demuestra tu dominio interactivo del laboratorio. Cada error desestabiliza tu metabolismo y te cuesta 1 vida.")
            
            Q1 = st.radio("1. Las enzimas son proteínas altamente específicas. ¿Por qué la naturaleza optó evolutivamente por la D-Glucosa sobre su enantiómero la L-Glucosa?", ["A) Porque la L-Glucosa desvía la luz a la derecha.", "B) Porque la configuración D encaja como 'llave y cerradura' en los sitios activos de nuestras enzimas.", "C) Porque las formas L no tienen enlaces O-Glucosídicos."], index=None)
            
            Q2 = st.radio("2. La Galactosa y la Glucosa tienen la misma fórmula, pero difieren en la posición del hidroxilo (-OH) en el carbono 4. Por lo tanto, se consideran:", ["A) Isótopos Atómicos", "B) Epímeros (Isómeros estructurales de 1 solo carbono)", "C) Enantiómeros Espejo"], index=None)
            
            Q3 = st.radio("3. Si el pH de la sangre desciende bruscamente, el cuerpo recurre a moléculas que resisten este cambio donando o aceptando protones. Esto es la definición de:", ["A) Una base pura", "B) Un Sistema Amortiguador o Buffer", "C) Un polímero"], index=None)
            
            Q4 = st.radio("4. Según el modelo cuántico de Schrödinger, ¿dónde habitan los electrones de los átomos del ecosistema CHONPS?", ["A) En órbitas circulares fijas (como planetas).", "B) Incrustados en el núcleo positivamente.", "C) En orbitales, que son zonas de máxima probabilidad matemática descritas por números cuánticos."], index=None)
            
            if st.button("Evaluar Bitácora de Laboratorio", use_container_width=True):
                errores = 0
                if Q1 != "B) Porque la configuración D encaja como 'llave y cerradura' en los sitios activos de nuestras enzimas.": errores += 1
                if Q2 != "B) Epímeros (Isómeros estructurales de 1 solo carbono)": errores += 1
                if Q3 != "B) Un Sistema Amortiguador o Buffer": errores += 1
                if Q4 != "C) En orbitales, que son zonas de máxima probabilidad matemática descritas por números cuánticos.": errores += 1
                
                if errores == 0:
                    st.balloons()
                    st.success("🏆 **¡RÉCORD PERFECTO!** Has dominado los modelos atómicos, el pH, los carbohidratos y el alfabeto CHONPS con rigor.")
                else:
                    st.session_state.vidas -= 1
                    st.error(f"❌ **Examen reprobado con {errores} error(es).** Has perdido 1 Vida. Repasa tus configuraciones.")
