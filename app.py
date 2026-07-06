import streamlit as st
import time

# ========================================================
# 1. CONFIGURACIÓN DEL CHASIS Y ESTÉTICA CÓSMICA PREMIUM
# ========================================================
st.set_page_config(page_title="ChonpsLab Pro", page_icon="⚛️", layout="wide")

st.markdown("""
<style>
    /* Universo Oscuro Absoluto */
    .stApp {
        background-color: #0b0f19 !important;
        background-image: 
            radial-gradient(rgba(255,255,255,0.15) 1px, transparent 20px),
            radial-gradient(rgba(255,255,255,0.1) 1px, transparent 30px);
        background-size: 350px 350px, 200px 200px;
        background-position: 0 0, 40px 60px;
        font-family: 'Segoe UI', -apple-system, sans-serif;
    }
    
    /* Tipografía y Títulos */
    .main-title { text-align: center; color: #ffffff; font-size: 4rem; font-weight: 900; margin-bottom: 0px; letter-spacing: 2px;}
    .main-title-suffix { color: #00e5ff; font-weight: 300; }
    .sub-title { text-align: center; font-style: italic; color: #90a4ae; font-size: 1.1rem; margin-top: 0px; margin-bottom: 30px; letter-spacing: 1px;}
    
    /* Paneles Glassmorphism (Translúcidos) */
    .bio-panel { 
        background: rgba(30, 41, 59, 0.65); 
        border-left: 5px solid #00e5ff; 
        border-radius: 8px; 
        padding: 25px; 
        margin-bottom: 25px; 
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
    }
    
    /* Tarjetas de Diagnóstico del Espectrómetro */
    .card-success { background: linear-gradient(90deg, rgba(76,175,80,0.15) 0%, rgba(0,0,0,0) 100%); border-left: 5px solid #4caf50; padding: 20px; border-radius: 6px; margin-top: 15px; border-bottom: 1px solid rgba(76,175,80,0.2);}
    .card-polar { background: linear-gradient(90deg, rgba(255,177,66,0.15) 0%, rgba(0,0,0,0) 100%); border-left: 5px solid #ffb142; padding: 20px; border-radius: 6px; margin-top: 15px; border-bottom: 1px solid rgba(255,177,66,0.2);}
    .card-error { background: linear-gradient(90deg, rgba(244,67,54,0.15) 0%, rgba(0,0,0,0) 100%); border-left: 5px solid #f44336; padding: 20px; border-radius: 6px; margin-top: 15px; border-bottom: 1px solid rgba(244,67,54,0.2);}
    
    /* Monitores Laterales */
    .monitor-box { background-color: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 15px; box-shadow: inset 0 0 20px rgba(0,0,0,0.5);}
    
    /* Navegación Hitech (Tabs) */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: transparent; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 5px;}
    .stTabs [data-baseweb="tab"] { background-color: rgba(30, 41, 59, 0.4); border-radius: 6px 6px 0 0; padding: 12px 24px; color: #90a4ae; font-weight: 600; font-size: 0.95rem; border: 1px solid transparent; border-bottom: none;}
    .stTabs [aria-selected="true"] { background-color: rgba(0, 229, 255, 0.1) !important; color: #00e5ff !important; border: 1px solid rgba(0, 229, 255, 0.3) !important; border-bottom: none !important; box-shadow: 0 -4px 15px rgba(0,229,255,0.05);}
</style>
""", unsafe_allow_html=True)

# ========================================================
# 2. BASE DE DATOS Y MOTOR DE CONTEXTO BIOLÓGICO (RESTAURADO)
# ========================================================
ELEMENTOS = {
    "Carbono (C)": {"fuerza": 2.55, "color": "#ffb142", "sym": "C"},
    "Hidrógeno (H)": {"fuerza": 2.20, "color": "#00e5ff", "sym": "H"},
    "Oxígeno (O)": {"fuerza": 3.44, "color": "#ff5252", "sym": "O"},
    "Nitrógeno (N)": {"fuerza": 3.04, "color": "#33d9b2", "sym": "N"},
    "Fósforo (P)": {"fuerza": 2.19, "color": "#ff7ff5", "sym": "P"},
    "Azufre (S)": {"fuerza": 2.58, "color": "#ffda79", "sym": "S"}
}

def obtener_contexto_biologico(sym1, sym2):
    """Mapeo avanzado celular basado en las combinaciones atómicas"""
    combo = "".join(sorted([sym1, sym2]))
    mapeo = {
        "CC": ("Carbohidratos y Lípidos", "Esqueleto hidrocarbonado basal. Covalente puro 100% apolar."),
        "CH": ("Lípidos celulares (Cadenas Hidrofóbicas)", "Forman las colas de ácidos grasos repelentes al agua."),
        "CO": ("Carbohidratos (Aldosas/Cetonas)", "Grupo carbonilo altamente reactivo, define familias de azúcares."),
        "CN": ("Proteínas (Enlace Peptídico)", "Unión rígida tipo amida estructural entre aminoácidos."),
        "HO": ("Agua (Puentes de Hidrógeno)", "Solvente universal dipolar celular."),
        "HN": ("ADN y Aminoácidos", "Grupos amino polares en bases nitrogenadas."),
        "OP": ("Ácidos Nucleicos y ATP", "Enlaces fosfodiéster de altísima energía celular."),
        "SS": ("Proteínas (Puente Disulfuro)", "Estabiliza la estructura 3D de proteínas complejas como la Insulina.")
    }
    return mapeo.get(combo, ("Ecosistema CHONPS", "Interacción atómica en el entorno metabólico intracelular."))

PREGUNTAS_UNAM = [
    {"q": "Si el pH de una solución cambia de 6 a 5, ¿qué magnitud de cambio de concentración de protones representa?", "opciones": ["Aumenta 1 vez", "Aumenta 10 veces", "Disminuye a la mitad"], "a": "Aumenta 10 veces", "retro": "La escala de pH es logarítmica base 10. Un descenso de 1 unidad significa un incremento exponencial de 10x en la acidez ($H^+$)."},
    {"q": "¿Qué grupo funcional define la unión estructural fundamental entre dos aminoácidos (Enlace Peptídico)?", "opciones": ["Grupo Éster", "Grupo Amida", "Grupo Éter"], "a": "Grupo Amida", "retro": "El enlace peptídico une un grupo carboxilo y un grupo amino, formando una Amida y liberando una molécula de agua en el proceso de traducción."},
    {"q": "En el isomerismo de carbohidratos, ¿por qué la naturaleza optó por las formas 'D' (D-Glucosa) sobre las 'L'?", "opciones": ["Porque las formas L son tóxicas", "Por la alta especificidad de las enzimas celulares que solo reconocen formas D", "Porque desvían la luz a la izquierda"], "a": "Por la alta especificidad de las enzimas celulares que solo reconocen formas D", "retro": "Las enzimas funcionan bajo el modelo 'llave-cerradura'; la arquitectura tridimensional de sus sitios activos solo encaja perfectamente con las D-aldosas."},
    {"q": "¿Cómo se clasifica el enlace de la Sacarosa (Glucosa + Fructosa) que le impide tener poder reductor?", "opciones": ["O-Glucosídico Dicarbonílico (Alfa 1 - Beta 2)", "N-Glucosídico", "Puente Disulfuro"], "a": "O-Glucosídico Dicarbonílico (Alfa 1 - Beta 2)", "retro": "Al comprometer ambos carbonos anoméricos en el enlace, la molécula se 'cierra' y no le quedan grupos hidroxilo libres para reducir otras moléculas en el plasma."},
    {"q": "Un Buffer o Amortiguador fisiológico celular está compuesto químicamente por:", "opciones": ["Un ácido fuerte y una base fuerte", "Un ácido débil y su base conjugada", "Agua destilada y sales"], "a": "Un ácido débil y su base conjugada", "retro": "El ácido débil (ej. Ácido Acético) y su base conjugada (Acetato) absorben impactos homeostáticos donando o capturando protones libres del medio."}
]

# ========================================================
# 3. MOTOR VECTORIAL SVG (PRECISIÓN ABSOLUTA)
# ========================================================
@st.cache_data
def generar_svg_tira_afloja(fuerza):
    if fuerza >= 3.0:
        return """
        <div style='display:flex; justify-content:center; align-items:center; width:100%; height:110px;'>
            <svg viewBox="0 0 240 100" width="100%" height="100%">
                <circle cx="60" cy="50" r="26" fill="#ff5252" opacity="0.9" filter="drop-shadow(0px 0px 5px rgba(255,82,82,0.5))"/>
                <text x="44" y="54" fill="white" font-weight="bold" font-family="sans-serif" font-size="12">FUERTE</text>
                <circle cx="95" cy="50" r="5" fill="#00e5ff"/>
                <ellipse cx="105" cy="50" rx="65" ry="28" fill="none" stroke="#ff5252" stroke-width="2" stroke-dasharray="5 3"/>
                <circle cx="180" cy="50" r="14" fill="#00e5ff" opacity="0.4"/>
            </svg>
        </div>
        """
    else:
        return """
        <div style='display:flex; justify-content:center; align-items:center; width:100%; height:110px;'>
            <svg viewBox="0 0 240 100" width="100%" height="100%">
                <circle cx="60" cy="50" r="18" fill="#90a4ae" opacity="0.8"/>
                <text x="44" y="54" fill="white" font-weight="bold" font-family="sans-serif" font-size="11">ÁTOMO A</text>
                <circle cx="120" cy="50" r="5" fill="#ffffff"/>
                <circle cx="120" cy="50" r="8" fill="none" stroke="#00e5ff" stroke-width="1.5"/>
                <circle cx="180" cy="50" r="18" fill="#90a4ae" opacity="0.8"/>
                <text x="164" y="54" fill="white" font-weight="bold" font-family="sans-serif" font-size="11">ÁTOMO B</text>
                <ellipse cx="120" cy="50" rx="65" ry="24" fill="none" stroke="#b0bec5" stroke-width="1.5" stroke-dasharray="3 3"/>
            </svg>
        </div>
        """

@st.cache_data
def generar_svg_enlace(sym1, f1, c1, sym2, f2, c2):
    diff = abs(f1 - f2)
    # Extracción explícita para evitar errores de tupla en Python
    if diff == 0:
        cx_e1, cx_e2 = 113, 127
        ellipse_x, ellipse_w = 120, 65
        stroke_color = "#ffffff"
        stroke_dash = "2 2"
    elif diff > 0.4:
        # Lógica ternaria segura
        if f1 > f2:
            cx_e1, cx_e2, ellipse_x, ellipse_w, stroke_color = 85, 95, 100, 70, c1
        else:
            cx_e1, cx_e2, ellipse_x, ellipse_w, stroke_color = 145, 155, 140, 70, c2
        stroke_dash = "4 2"
    else:
        cx_e1, cx_e2 = 105, 135
        ellipse_x, ellipse_w = 120, 68
        stroke_color = "#b0bec5"
        stroke_dash = "3 3"

    return f"""
    <div style='display:flex; justify-content:center; align-items:center; width:100%; height:130px;'>
        <svg viewBox="0 0 240 120" width="100%" height="100%">
            <circle cx="70" cy="60" r="24" fill="{c1}" opacity="0.85"/>
            <text x="64" y="65" fill="black" font-weight="bold" font-family="sans-serif" font-size="16">{sym1}</text>
            <circle cx="170" cy="60" r="20" fill="{c2}" opacity="0.85"/>
            <text x="164" y="65" fill="black" font-weight="bold" font-family="sans-serif" font-size="14">{sym2}</text>
            <ellipse cx="{ellipse_x}" cy="60" rx="{ellipse_w}" ry="35" fill="none" stroke="{stroke_color}" stroke-width="2" stroke-dasharray="{stroke_dash}"/>
            <circle cx="{cx_e1}" cy="60" r="4" fill="#ffffff"/>
            <circle cx="{cx_e2}" cy="60" r="4" fill="#ffffff"/>
        </svg>
    </div>
    """

# ========================================================
# 4. INICIALIZACIÓN DE ESTADOS
# ========================================================
if "auth" not in st.session_state: st.session_state["auth"] = False
if "vidas" not in st.session_state: st.session_state["vidas"] = 3
if "puntos" not in st.session_state: st.session_state["puntos"] = 0
if "quiz_evaluado" not in st.session_state: st.session_state["quiz_evaluado"] = False
if "quiz_respuestas" not in st.session_state: st.session_state["quiz_respuestas"] = {}

# ========================================================
# 5. PORTADA DE ACCESO (MARCA PERSONAL)
# ========================================================
if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>Chonps<span class='main-title-suffix'>Lab</span></h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Plataforma Interactiva de Ciencias de la Vida y Biología Celular</p>", unsafe_allow_html=True)
    st.markdown("""
    <div class='bio-panel' style='max-width: 800px; margin: 0 auto 30px auto;'>
        <span style='color:#00e5ff; font-weight:700; font-size:1.3rem; margin-bottom:10px; display:block;'>Sincronización del Entorno Analítico</span>
        <p style='color:#cfd8dc; line-height: 1.6;'>Valida tus credenciales para acceder a la estación de trabajo. Este simulador integra modelado de teoría atómica, espectrometría de fuerzas electronegativas, reacciones de monosacáridos y curvas de estabilización de pH en un ecosistema de grado clínico.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        pwd = st.text_input("Licencia de Acceso (Token Único):", type="password", placeholder="Ingresa SYNAPSIS o LAB-2026")
        if st.button("Activar Panel Central", use_container_width=True):
            if pwd.strip().upper() in ["SYNAPSIS", "LAB-2026", "CHONPS"]:
                st.session_state["auth"] = True
                st.rerun()
            else:
                st.error("Acceso denegado. Token de matrícula inválido.")

# ========================================================
# 6. CONSOLA DE LABORATORIO (TABS DE ALTO RENDIMIENTO)
# ========================================================
else:
    # Encabezado Central Clínico
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown("<h2 style='color:#00e5ff; margin-top:0; font-weight:800;'>Consola de Operaciones: ChonpsLab</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:#90a4ae; font-style:italic;'>Monitoreo de Variables Bioquímicas en Tiempo Real</p>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='monitor-box'><span style='color:#90a4ae; font-size:11px; letter-spacing:1px;'>ESTABILIDAD (VIDAS)</span><br><b style='font-size:24px; color:#f44336;'>{st.session_state.vidas} / 3 💔</b></div>", unsafe_allow_html=True)

    if st.session_state.vidas <= 0:
        st.markdown("<div class='card-error' style='text-align:center;'><h3>🚨 COLAPSO METABÓLICO</h3><p>Te has quedado sin vidas por acumulación de errores analíticos. El laboratorio se ha bloqueado preventivamente.</p></div>", unsafe_allow_html=True)
        if st.button("Restaurar Parámetros Base", use_container_width=True):
            st.session_state.vidas = 3
            st.session_state.quiz_evaluado = False
            st.rerun()
    else:
        # Navegación Fluida
        tabs = st.tabs([
            "🏛️ 1. Teoría Atómica", 
            "⚡ 2. Escala Pauling", 
            "🧬 3. Reactor de Enlace", 
            "🍬 4. Glucómica", 
            "🌡️ 5. Amortiguadores", 
            "🏆 6. Matriz Final"
        ])

        # ----------------------------------------------------
        # MÓDULO 1: TEORÍA ATÓMICA
        # ----------------------------------------------------
        with tabs[0]:
            st.markdown("### Evolución de la Estructura de la Materia")
            st.write("Para entender la bioquímica celular, primero debemos comprender cómo los científicos definieron el ladrillo básico del universo: el átomo.")
            
            modelo = st.select_slider(
                "Viaja en la línea temporal de la física cuántica:",
                options=["Dalton (1810)", "Thomson (1897)", "Rutherford (1911)", "Bohr (1913)", "Schrödinger (1926)"]
            )
            
            st.write("")
            if "Dalton" in modelo:
                st.markdown("<div class='bio-panel'><b>⚛️ Modelo de John Dalton (1810):</b><br>Define el átomo como una esfera sólida indivisible. Postuló que los átomos del mismo elemento tienen igual masa y propiedades, y que el reordenamiento de estos equivale a una reacción química básica.</div>", unsafe_allow_html=True)
            elif "Thomson" in modelo:
                st.markdown("<div class='bio-panel'><b>⚛️ Modelo de J.J. Thomson (1897):</b><br>Conocido como el 'Pudin de pasas'. Incorpora por primera vez los electrones, describiéndolos como cargas negativas incrustadas dentro de una gran esfera de electricidad positiva.</div>", unsafe_allow_html=True)
            elif "Rutherford" in modelo:
                st.markdown("<div class='bio-panel'><b>⚛️ Modelo de Ernest Rutherford (1911):</b><br>Demostró mediante experimentación que los átomos están mayormente huecos. Propuso un núcleo central extremadamente denso y pesado, alrededor del cual orbitan los electrones.</div>", unsafe_allow_html=True)
            elif "Bohr" in modelo:
                st.markdown("<div class='bio-panel'><b>⚛️ Modelo de Niels Bohr (1913):</b><br>Introdujo los niveles cuantizados de energía. El electrón ya no gira libremente, sino en órbitas circulares definidas; el salto entre estas órbitas emite o absorbe energía específica (fotones).</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='bio-panel'><b>⚛️ Modelo de Erwin Schrödinger (1926):</b><br>El salto al Modelo Cuántico actual. Los electrones no tienen trayectorias exactas, habitan en 'orbitales': regiones tridimensionales de probabilidad matemática definidas por los números cuánticos (n, l, m).</div>", unsafe_allow_html=True)

        # ----------------------------------------------------
        # MÓDULO 2: ESCALA PAULING (CHONPS)
        # ----------------------------------------------------
        with tabs[1]:
            st.markdown("### El Estira y Afloja Atómico (Electronegatividad)")
            st.write("La fuerza con la que un núcleo arranca o retiene los electrones de un enlace. Ajusta el control para simular la tensión molecular.")
            
            fuerza = st.slider("Ajuste de Electronegatividad:", 0.7, 4.0, 2.2, 0.1)
            
            st.components.v1.html(generar_svg_tira_afloja(fuerza), height=130, scrolling=False)
            
            if fuerza >= 3.0:
                st.markdown("<div class='card-error'><b>🔥 Átomo Ambicioso (Ej: O, N):</b> Su inmensa atracción deforma la nube, polarizando la molécula y definiendo los puentes de hidrógeno.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='card-success'><b>🤝 Átomo Equilibrado (Ej: C, H, S):</b> Comparte de forma simétrica. Crea esqueletos no polares esenciales para la vida (grasas, membranas).</div>", unsafe_allow_html=True)
                
            st.write("---")
            st.markdown("<h4 style='color:#00e5ff;'>Identidad de los Ladrillos CHONPS</h4>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            keys = list(ELEMENTOS.keys())
            for i, col in enumerate([c1, c2, c3]):
                with col:
                    k1, k2 = keys[i*2], keys[i*2+1]
                    st.markdown(f"<div style='background:rgba(255,255,255,0.05); padding:10px; border-radius:5px; border-left:3px solid {ELEMENTOS[k1]['color']}; margin-bottom:10px;'><b>{k1}</b><br><small>Fuerza: {ELEMENTOS[k1]['fuerza']}</small></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='background:rgba(255,255,255,0.05); padding:10px; border-radius:5px; border-left:3px solid {ELEMENTOS[k2]['color']}; margin-bottom:10px;'><b>{k2}</b><br><small>Fuerza: {ELEMENTOS[k2]['fuerza']}</small></div>", unsafe_allow_html=True)

        # ----------------------------------------------------
        # MÓDULO 3: REACTOR DE ENLACES (CON MOTOR BIOLÓGICO)
        # ----------------------------------------------------
        with tabs[2]:
            st.markdown("### Espectrometría de Enlaces Covalentes")
            st.write("Funde dos elementos biológicos. El sistema calculará la polaridad vectorial y determinará en qué macromolécula orgánica encaja esta unión.")
            
            c1, c2 = st.columns(2)
            atom1 = c1.selectbox("Elemento Primario (A):", list(ELEMENTOS.keys()))
            atom2 = c2.selectbox("Elemento Secundario (B):", list(ELEMENTOS.keys()))
            
            if st.button("Activar Reactor Molecular", use_container_width=True):
                a1, a2 = ELEMENTOS[atom1], ELEMENTOS[atom2]
                st.components.v1.html(generar_svg_enlace(a1['sym'], a1['fuerza'], a1['color'], a2['sym'], a2['fuerza'], a2['color']), height=140, scrolling=False)
                
                diff = abs(a1['fuerza'] - a2['fuerza'])
                macro_tit, macro_desc = obtener_contexto_biologico(a1['sym'], a2['sym'])
                
                if diff == 0:
                    css_card = "card-success"
                    tit = f"✅ Enlace No Polar Homonúcleo (Diferencia = 0.0)"
                elif diff <= 0.4:
                    css_card = "card-success"
                    tit = f"✅ Enlace Covalente No Polar (Diferencia = {diff:.2f})"
                elif diff <= 1.7:
                    css_card = "card-polar"
                    tit = f"⚡ Enlace Covalente Polar (Diferencia = {diff:.2f})"
                else:
                    css_card = "card-error"
                    tit = f"⚠️ Inestabilidad Iónica (Diferencia = {diff:.2f})"
                    st.session_state.vidas -= 1
                    
                st.markdown(f"""
                <div class='{css_card}'>
                    <h4 style='margin-top:0;'>{tit}</h4>
                    <p style='margin-bottom:10px;'><strong>🔬 Integración Biológica: {macro_tit}</strong><br>{macro_desc}</p>
                </div>
                """, unsafe_allow_html=True)

        # ----------------------------------------------------
        # MÓDULO 4: GLUCÓMICA Y CARBOHIDRATOS
        # ----------------------------------------------------
        with tabs[3]:
            st.markdown("### Glucómica: Isomerismo y Disacáridos")
            st.write("El orden de los átomos en el espacio dicta su función. Experimenta con la especificidad enzimática.")
            
            with st.expander("🔍 Análisis Estructural: Glucosa vs Galactosa (Epímeros)"):
                st.markdown("""
                **¿Qué son los epímeros?**
                Son isómeros que difieren en la configuración espacial de un único carbono asimétrico.
                * **D-Glucosa:** En el Carbono 4, el grupo Hidroxilo (-OH) se orienta a la derecha.
                * **D-Galactosa:** En el Carbono 4, el grupo Hidroxilo (-OH) se orienta a la izquierda.
                * *Impacto clínico:* Esta diminuta alteración obliga al organismo a utilizar rutas y enzimas completamente distintas para su metabolismo.
                """)
            
            st.markdown("#### Cámara de Síntesis O-Glucosídica")
            c1, c2 = st.columns(2)
            azu1 = c1.selectbox("Residuo Monosacárido 1:", ["Alfa-D-Glucosa", "Beta-D-Galactosa"])
            azu2 = c2.selectbox("Residuo Monosacárido 2:", ["Alfa-D-Glucosa", "Beta-D-Fructosa"])
            
            if st.button("Formar Enlace (Liberar $H_2O$)", use_container_width=True):
                if azu1 == "Alfa-D-Glucosa" and azu2 == "Alfa-D-Glucosa":
                    st.markdown("<div class='card-success'>🌾 <b>MALTOSA [Enlace Alfa 1→4]:</b> Azúcar de malta, reductor. Producto de la digestión del almidón.</div>", unsafe_allow_html=True)
                elif azu1 == "Beta-D-Galactosa" and azu2 == "Alfa-D-Glucosa":
                    st.markdown("<div class='card-success'>🥛 <b>LACTOSA [Enlace Beta 1→4]:</b> Azúcar de leche animal. Requiere enzima Lactasa para escindir el enlace 'Beta'.</div>", unsafe_allow_html=True)
                elif azu1 == "Alfa-D-Glucosa" and azu2 == "Beta-D-Fructosa":
                    st.markdown("<div class='card-success'>🎋 <b>SACAROSA [Enlace Alfa 1 ↔ Beta 2]:</b> Azúcar de caña. Dicarbonílico, bloquea los extremos reduciendo su reactividad.</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='card-error'>⚠️ <b>Mutación Estructural:</b> Ensamblaje incompatible con el metabolismo estándar de mamíferos.</div>", unsafe_allow_html=True)

        # ----------------------------------------------------
        # MÓDULO 5: TITULACIÓN Y BUFFERS
        # ----------------------------------------------------
        with tabs[4]:
            st.markdown("### Sistemas de Amortiguación Homeostática")
            st.write("La vida depende de un pH estable (7.35 - 7.45 en plasma). Simula una infusión agresiva de ácido fuerte.")
            
            solucion = st.radio("Escoge el fluido receptor:", ["Agua Destilada Pura (Sin capacidad de tamponamiento)", "Plasma Sanguíneo (Contiene Buffer Bicarbonato / Proteínas)"])
            
            if st.button("Infundir 10 mL de HCl (Ácido Clorhídrico)", use_container_width=True):
                if "Agua" in solucion:
                    st.progress(0.1) # Representación visual gráfica del pH desplomado
                    st.markdown("<div class='card-error'><b>🩸 CHOQUE DE ACIDOSIS (pH cae a 2.0):</b> El HCl libera libremente todos sus protones ($H^+$). Al no existir un ácido/base débil que los atrape, la acidez se dispara desnaturalizando la estructura 3D de las proteínas. <b>Pierdes 1 vida.</b></div>", unsafe_allow_html=True)
                    st.session_state.vidas -= 1
                else:
                    st.progress(0.7) # Representación visual del pH estable
                    st.markdown("<div class='card-success'><b>🛡️ TAMPONAMIENTO ESTABLE (pH se mantiene en ~7.4):</b> Las bases conjugadas del plasma secuestran el exceso de protones del HCl convirtiéndolos en componentes débiles. La concentración celular sobrevive en su <b>Región Amortiguadora</b>.</div>", unsafe_allow_html=True)

        # ----------------------------------------------------
        # MÓDULO 6: MATRIZ DE EVALUACIÓN CON FEEDBACK
        # ----------------------------------------------------
        with tabs[5]:
            st.markdown("### Validación Científica Rigurosa")
            st.write("Cierra tu práctica de laboratorio respondiendo el cuestionario. Obtendrás retroalimentación detallada tras enviar.")
            
            with st.form("exam_unam_pro"):
                for i, q in enumerate(PREGUNTAS_UNAM):
                    st.markdown(f"<span style='color:#00e5ff; font-weight:bold;'>{q['q']}</span>", unsafe_allow_html=True)
                    st.session_state.quiz_respuestas[i] = st.radio(f"R{i}", q['opciones'], key=f"q_{i}", label_visibility="collapsed")
                    st.write("")
                
                submitted = st.form_submit_button("Someter Bitácora a Evaluación", use_container_width=True)
                
            if submitted:
                st.session_state.quiz_evaluado = True
                errores = sum([1 for i, q in enumerate(PREGUNTAS_UNAM) if st.session_state.quiz_respuestas[i] != q['a']])
                
                if errores == 0:
                    st.balloons()
                    st.success("🏆 ¡CALIFICACIÓN PERFECTA! Cero lagunas conceptuales. Has dominado la física cuántica, biomoléculas y homeostasis celular.")
                else:
                    st.session_state.vidas -= 1
                    st.error(f"❌ Detectamos {errores} error(es) en tu análisis. Has perdido 1 vida. Revisa las correcciones detalladas abajo:")
                
                st.markdown("#### 📑 Reporte Clínico Detallado")
                for i, q in enumerate(PREGUNTAS_UNAM):
                    acierto = st.session_state.quiz_respuestas[i] == q['a']
                    estado = "✅ CORRECTO" if acierto else "❌ INCORRECTO"
                    with st.expander(f"Reactivo {i+1} — {estado}", expanded=not acierto):
                        st.write(f"**Tu respuesta:** {st.session_state.quiz_respuestas[i]}")
                        if not acierto:
                            st.write(f"**Respuesta esperada:** {q['a']}")
                        st.markdown(f"<div style='padding:10px; background:rgba(255,255,255,0.05); border-left:3px solid {'#4caf50' if acierto else '#ffb142'};'>{q['retro']}</div>", unsafe_allow_html=True)

    st.write("---")
    st.markdown("<p style='text-align:center; color:#90a4ae; font-size:12px;'>ChonpsLab Pro © 2026 | Sistema Paramétrico de Educación Interactiva</p>", unsafe_allow_html=True)
