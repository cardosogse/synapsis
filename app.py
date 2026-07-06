import streamlit as st
import time

# ========================================================
# 1. CONFIGURACIÓN DEL CHASIS Y ESTÉTICA CÓSMICA NEGRA
# ========================================================
st.set_page_config(page_title="ChonpsLab Pro", page_icon="⚛️", layout="wide" if st.sidebar else "centered")

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
    .main-title { text-align: center; color: #ffffff; font-size: 3.2rem; font-weight: 800; margin-bottom: 0px; }
    .main-title-suffix { color: #00e5ff; font-weight: 300; }
    .bio-panel { background-color: rgba(30, 41, 59, 0.6); border-left: 5px solid #00e5ff; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
    .card-success { background-color: rgba(76, 175, 80, 0.1); border-left: 5px solid #4caf50; padding: 15px; border-radius: 5px; margin-top: 10px; }
    .card-error { background-color: rgba(244, 67, 54, 0.1); border-left: 5px solid #f44336; padding: 15px; border-radius: 5px; margin-top: 10px; }
    .monitor-box { background-color: rgba(255,255,255,0.05); padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 10px;}
</style>
""", unsafe_allow_html=True)

# ========================================================
# 2. BASE DE DATOS MAESTRA (CÁTEDRA UNAM FMVZ)
# ========================================================
ELEMENTOS = {
    "Carbono (C)": {"fuerza": 2.55, "color": "#ffb142", "sym": "C"},
    "Hidrógeno (H)": {"fuerza": 2.20, "color": "#00e5ff", "sym": "H"},
    "Oxígeno (O)": {"fuerza": 3.44, "color": "#ff5252", "sym": "O"},
    "Nitrógeno (N)": {"fuerza": 3.04, "color": "#33d9b2", "sym": "N"},
    "Fósforo (P)": {"fuerza": 2.19, "color": "#ff7ff5", "sym": "P"},
    "Azufre (S)": {"fuerza": 2.58, "color": "#ffda79", "sym": "S"}
}

PREGUNTAS_UNAM = [
    {"q": "Si el pH de una solución cambia de 6 a 5, ¿qué magnitud de cambio de concentración de protones representa debido a su escala logarítmica?", "opciones": ["Aumenta 1 vez", "Aumenta 10 veces", "Disminuye a la mitad"], "a": "Aumenta 10 veces", "retro": "Correcto. La escala de pH es logarítmica base 10. Un cambio de 1 unidad significa un aumento de 10x en la acidez."},
    {"q": "¿Qué grupo funcional define la unión estructural fundamental entre dos aminoácidos (Enlace Peptídico)?", "opciones": ["Grupo Éster", "Grupo Amida", "Grupo Éter"], "a": "Grupo Amida", "retro": "Correcto. El enlace peptídico une un carboxilo y un amino, formando una Amida y liberando agua."},
    {"q": "En el isomerismo de carbohidratos, ¿por qué la naturaleza prefiere las formas 'D' (D-Glucosa) sobre las 'L'?", "opciones": ["Porque las formas L son tóxicas", "Por la alta especificidad de las enzimas celulares que solo reconocen formas D", "Porque desvían la luz a la izquierda"], "a": "Por la alta especificidad de las enzimas celulares que solo reconocen formas D", "retro": "Correcto. Las enzimas son como llaves y cerraduras; solo encajan con la arquitectura 3D de las D-aldosas."},
    {"q": "¿Cómo se clasifica el enlace de la Sacarosa (Glucosa + Fructosa) que impide que tenga poder reductor?", "opciones": ["O-Glucosídico Dicarbonílico (Alfa 1 - Beta 2)", "N-Glucosídico", "Puente Disulfuro"], "a": "O-Glucosídico Dicarbonílico (Alfa 1 - Beta 2)", "retro": "Correcto. Al comprometer ambos carbonos anoméricos, no quedan grupos libres para reducir otras moléculas."},
    {"q": "Un Buffer o Amortiguador fisiológico está compuesto químicamente por:", "opciones": ["Un ácido fuerte y una base fuerte", "Un ácido débil y su base conjugada", "Agua destilada y sales"], "a": "Un ácido débil y su base conjugada", "retro": "Correcto. Como el Ácido Acético y el Acetato, resisten cambios bruscos de pH donando o capturando protones."}
]

# ========================================================
# 3. MOTOR VECTORIAL SVG (BUG CORREGIDO Y OPTIMIZADO)
# ========================================================
def generar_svg_enlace(sym1, f1, c1, sym2, f2, c2):
    diff = abs(f1 - f2)
    # ¡AQUÍ ESTÁ EL BUG SOLUCIONADO CON PARÉNTESIS EN LAS TUPLAS!
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
# 4. GESTIÓN DE ESTADOS (STATE MANAGEMENT)
# ========================================================
if "auth" not in st.session_state: st.session_state["auth"] = False
if "vidas" not in st.session_state: st.session_state["vidas"] = 3
if "fase" not in st.session_state: st.session_state["fase"] = 1
if "sim_html" not in st.session_state: st.session_state["sim_html"] = ""

# ========================================================
# 5. PANTALLA PÚBLICA (LOGIN)
# ========================================================
if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>Chonps<span class='main-title-suffix'>Lab Pro</span></h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Plataforma Integral de Bioquímica (Módulos UNAM)</p>", unsafe_allow_html=True)
    st.markdown("<div class='bio-panel'>Integra los Fundamentos Químicos, el comportamiento del Agua y pH, y la estructura isomérica de los Carbohidratos en una sola consola.</div>", unsafe_allow_html=True)
    
    pwd = st.text_input("Licencia de Acceso:", type="password")
    if st.button("Activar Consola de Laboratorio", use_container_width=True):
        if pwd.strip().upper() in ["SYNAPSIS-PRO", "VET-UNAM"]:
            st.session_state["auth"] = True
            st.rerun()
        else:
            st.error("Acceso denegado.")

# ========================================================
# 6. CONSOLA PRIVADA (APLICACIÓN PRINCIPAL)
# ========================================================
else:
    with st.sidebar:
        st.markdown(f"<div class='monitor-box'><span style='color:#90a4ae;'>ESTABILIDAD (VIDAS)</span><br><b style='font-size:1.5rem;color:#f44336;'>{st.session_state.vidas}/3</b></div>", unsafe_allow_html=True)
        st.write("---")
        if st.button("Fase 1: Reactor CHONPS", use_container_width=True): st.session_state.fase = 1; st.rerun()
        if st.button("Fase 2: Agua y Buffers (pH)", use_container_width=True): st.session_state.fase = 2; st.rerun()
        if st.button("Fase 3: Grupos Funcionales", use_container_width=True): st.session_state.fase = 3; st.rerun()
        if st.button("Fase 4: Carbohidratos", use_container_width=True): st.session_state.fase = 4; st.rerun()
        if st.button("Fase 5: Examen UNAM", use_container_width=True): st.session_state.fase = 5; st.rerun()
        st.write("---")
        if st.button("Cerrar Sesión"): st.session_state.auth = False; st.rerun()

    if st.session_state.vidas <= 0:
        st.error("🚨 COLAPSO CELULAR: Te has quedado sin vidas. El laboratorio se ha reiniciado.")
        if st.button("Restaurar Laboratorio"):
            st.session_state.vidas = 3
            st.session_state.fase = 1
            st.rerun()
            
    else:
        # ----------------------------------------------------
        # FASE 1: REACTOR CHONPS (CORREGIDO)
        # ----------------------------------------------------
        if st.session_state.fase == 1:
            st.subheader("Fase 1: Reactor de Enlaces Moleculares")
            st.write("Combina elementos. El espectrómetro calculará vectorialmente la deformación de la nube según la Escala de Pauling.")
            
            c1, c2 = st.columns(2)
            atom1 = c1.selectbox("Átomo A:", list(ELEMENTOS.keys()))
            atom2 = c2.selectbox("Átomo B:", list(ELEMENTOS.keys()))
            
            if st.button("Sintetizar", use_container_width=True):
                a1, a2 = ELEMENTOS[atom1], ELEMENTOS[atom2]
                st.session_state.sim_html = generar_svg_enlace(a1['sym'], a1['fuerza'], a1['color'], a2['sym'], a2['fuerza'], a2['color'])
                
                diff = abs(a1['fuerza'] - a2['fuerza'])
                if diff == 0:
                    st.success("✅ **Enlace Covalente No Polar Puro (Diferencia = 0.0).** Simetría orbital perfecta. (Ej. Puente Disulfuro S-S).")
                elif diff <= 0.4:
                    st.success(f"✅ **Enlace Covalente No Polar (Diferencia = {diff:.2f}).** Reparto equitativo, moléculas hidrofóbicas (Ej. C-H en Lípidos).")
                elif diff <= 1.7:
                    st.info(f"⚡ **Enlace Covalente Polar (Diferencia = {diff:.2f}).** Formación de dipolos asimétricos, moléculas hidrofílicas solubles en agua.")
                else:
                    st.error(f"⚠️ **Tensión Iónica Crítica (Diferencia = {diff:.2f}).** Intercambio abrupto de electrones.")
                    st.session_state.vidas -= 1
            
            if st.session_state.sim_html:
                st.components.v1.html(st.session_state.sim_html, height=140, scrolling=False)

        # ----------------------------------------------------
        # FASE 2: LABORATORIO DE AGUA Y BUFFERS
        # ----------------------------------------------------
        elif st.session_state.fase == 2:
            st.subheader("Fase 2: Curvas de Titulación y Buffers Fisiológicos")
            st.write("Agrega Ácido Clorhídrico (HCl) al medio celular y observa cómo reacciona el pH. Identifica la Región Amortiguadora.")
            
            medio = st.selectbox("Selecciona el medio celular:", ["Agua Destilada (Sin buffer)", "Solución de Ácido Acético / Acetato (Buffer)"])
            
            if st.button("Inyectar Ácido (HCl)", use_container_width=True):
                if "Agua" in medio:
                    st.markdown("<div class='card-error'><b>❌ Acidosis Fulminante:</b> El HCl disocia $H^+$ libremente. El pH colapsa de inmediato a 2.0. Las proteínas se desnaturalizan. Pierdes 1 vida.</div>", unsafe_allow_html=True)
                    st.session_state.vidas -= 1
                else:
                    st.markdown("<div class='card-success'><b>✅ Estabilidad Tamponada:</b> La base conjugada (Acetato) captura los $H^+$ del HCl convirtiéndolos en Ácido Acético débil. El pH se mantiene estable alrededor de 4.7 (Zona Buffer).</div>", unsafe_allow_html=True)

        # ----------------------------------------------------
        # FASE 3: IDENTIFICADOR DE GRUPOS FUNCIONALES
        # ----------------------------------------------------
        elif st.session_state.fase == 3:
            st.subheader("Fase 3: Reconocimiento Biológico")
            st.write("Analiza la molécula y determina qué grupo funcional define su reactividad.")
            
            st.markdown("<h3 style='text-align:center; color:#ffb142;'>$R - C(=O) - OH$</h3>", unsafe_allow_html=True)
            ans = st.radio("¿Qué grupo funcional es este (característico de los ácidos grasos)?", ["Cetona (Ceto)", "Ácido Carboxílico (Carboxilo)", "Aldehído (Aldo)"])
            
            if st.button("Escanear Estructura"):
                if "Carboxilo" in ans:
                    st.success("✅ ¡Correcto! El grupo Carboxilo ($COOH$) define a los ácidos carboxílicos y ácidos grasos.")
                else:
                    st.error("❌ Incorrecto. Ese es el grupo Carboxilo. Pierdes 1 vida.")
                    st.session_state.vidas -= 1

        # ----------------------------------------------------
        # FASE 4: ENSAMBLADOR DE CARBOHIDRATOS (ISOMERISMO)
        # ----------------------------------------------------
        elif st.session_state.fase == 4:
            st.subheader("Fase 4: Síntesis de Glúcidos")
            st.write("Une dos monosacáridos mediante un enlace O-Glucosídico (liberando una molécula de agua $H_2O$) para formar un disacárido funcional.")
            
            c1, c2 = st.columns(2)
            azucar1 = c1.selectbox("Monosacárido 1:", ["Alfa-Glucosa", "Beta-Galactosa"])
            azucar2 = c2.selectbox("Monosacárido 2:", ["Alfa-Glucosa", "Beta-Fructosa"])
            
            if st.button("Formar Enlace O-Glucosídico", use_container_width=True):
                if azucar1 == "Alfa-Glucosa" and azucar2 == "Alfa-Glucosa":
                    st.success("✅ **MALTOSA SINTETIZADA:** Enlace Alfa(1->4). Es un azúcar reductor producto de la degradación del almidón.")
                elif azucar1 == "Beta-Galactosa" and azucar2 == "Alfa-Glucosa":
                    st.success("✅ **LACTOSA SINTETIZADA:** Enlace Beta(1->4). El azúcar de la leche animal.")
                elif azucar1 == "Alfa-Glucosa" and azucar2 == "Beta-Fructosa":
                    st.success("✅ **SACAROSA SINTETIZADA:** Enlace Alfa(1) - Beta(2). Dicarbonílico. Carece de poder reductor.")
                else:
                    st.warning("⚠️ Combinación atípica. Enzimáticamente inestable en mamíferos.")

        # ----------------------------------------------------
        # FASE 5: EXAMEN PROFESIONAL UNAM
        # ----------------------------------------------------
        elif st.session_state.fase == 5:
            st.subheader("Fase 5: Validación Curricular")
            st.write("Responde el test integral basado en los fundamentos químicos y estructura de carbohidratos.")
            
            with st.form("exam_unam"):
                respuestas = {}
                for i, q in enumerate(PREGUNTAS_UNAM):
                    st.markdown(f"**{q['q']}**")
                    respuestas[i] = st.radio(f"R{i}", q['opciones'], label_visibility="collapsed")
                    st.write("")
                
                if st.form_submit_button("Entregar Examen", use_container_width=True):
                    errores = 0
                    for i, q in enumerate(PREGUNTAS_UNAM):
                        if respuestas[i] != q['a']: errores += 1
                        else: st.success(f"**P{i+1} Correcta:** {q['retro']}")
                        
                    if errores > 0:
                        st.error(f"❌ Tuviste {errores} error(es). Pierdes 1 vida. Revisa tus apuntes.")
                        st.session_state.vidas -= 1
                    else:
                        st.balloons()
                        st.success("🏆 ¡EXCELENCIA ACADÉMICA! Aprobaste la matriz biológica.")
