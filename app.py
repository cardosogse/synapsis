import streamlit as st
import time

# 1. CONFIGURACIÓN DEL CHASIS DE NAVEGACIÓN NATIVA
st.set_page_config(page_title="ChonpsLab", page_icon="⚛️", layout="centered")

# --- INYECCIÓN DE ESTILOS CSS AVANZADOS (MODO OSCURO INTEGRADO) ---
st.markdown("""
<style>
    /* Estilos globales de la Portada Premium */
    .main-title {
        text-align: center; 
        color: #ffffff; 
        font-size: 3.4rem; 
        font-weight: 800; 
        font-family: 'Segoe UI', -apple-system, sans-serif;
        margin-bottom: 0px;
        letter-spacing: 1px;
    }
    .main-title-suffix {
        color: #00e5ff; 
        font-weight: 300;
        font-size: 2.8rem;
    }
    .sub-title {
        text-align: center; 
        font-style: italic; 
        color: #90a4ae; 
        font-size: 1.1rem; 
        margin-top: 5px; 
        margin-bottom: 25px;
        letter-spacing: 0.5px;
    }
    /* Panel de Marketing Translúcido (Adiós al cuadro blanco espantoso) */
    .bio-panel {
        background-color: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(0, 229, 255, 0.2);
        border-left: 5px solid #00e5ff;
        padding: 24px;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0, 229, 255, 0.05);
        margin-bottom: 30px;
        text-align: center;
    }
    .panel-hook {
        color: #00e5ff;
        font-weight: 700;
        font-size: 1.25rem;
        display: block;
        margin-bottom: 8px;
        letter-spacing: 0.3px;
    }
    .panel-text {
        color: #cfd8dc;
        font-size: 0.95rem;
        margin: 0;
        line-height: 1.5;
    }
    /* Estilos del Entorno Privado del Laboratorio */
    .console-header {
        background-color: rgba(30, 41, 59, 0.4);
        border-left: 5px solid #0288d1;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 20px;
    }
    .spectrometer-card-success {
        background-color: rgba(76, 175, 80, 0.1);
        border: 1px solid rgba(76, 175, 80, 0.3);
        border-left: 6px solid #4caf50;
        padding: 20px;
        border-radius: 6px;
        margin-top: 15px;
    }
    .spectrometer-card-error {
        background-color: rgba(244, 67, 54, 0.1);
        border: 1px solid rgba(244, 67, 54, 0.3);
        border-left: 6px solid #f44336;
        padding: 20px;
        border-radius: 6px;
        margin-top: 15px;
    }
    .spectrometer-title {
        color: #b0bec5;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .sidebar-monitor {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 12px;
        border-radius: 4px;
        margin-bottom: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- BITÁCORA GLOBAL COMPARTIDA (EL MURO DE ACERO ANTIPIRATERÍA) ---
@st.cache_resource
def obtener_base_datos_global():
    return {}

base_datos_global = obtener_base_datos_global()
CODIGOS_VIGENTES = ["SYNAPSIS-PRO", "VET-BIOQUIMICA-2026", "MED-ELITE-30DAYS"]

if "mi_session_id" not in st.session_state:
    st.session_state["mi_session_id"] = str(time.time_ns())

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
if "codigo_ingresado" not in st.session_state:
    st.session_state["codigo_ingresado"] = ""

# VARIABLES DE ESTADO LOCAL DEL LABORATORIO
if "vidas" not in st.session_state:
    st.session_state["vidas"] = 3
if "puntos" not in st.session_state:
    st.session_state["puntos"] = 0
if "bloque_actual" not in st.session_state:
    st.session_state["bloque_actual"] = 0  
if "simulacion_ejecutada" not in st.session_state:
    st.session_state["simulacion_ejecutada"] = False
if "resultado_texto" not in st.session_state:
    st.session_state["resultado_texto"] = ""
if "estado_sistema" not in st.session_state:
    st.session_state["estado_sistema"] = "En Espera"

# --- RADAR PASIVO DE PIRATERÍA ---
@st.fragment(run_every=5)
def radar_seguridad_pasivo():
    if st.session_state["autenticado"]:
        codigo = st.session_state["codigo_ingresado"]
        if codigo in base_datos_global and base_datos_global[codigo] != st.session_state["mi_session_id"]:
            st.rerun()

def verificar_bloqueo_pirateria():
    if st.session_state["autenticado"]:
        codigo = st.session_state["codigo_ingresado"]
        if codigo in base_datos_global:
            if base_datos_global[codigo] != st.session_state["mi_session_id"]:
                st.session_state["autenticado"] = False
                st.session_state["codigo_ingresado"] = ""
                st.error("🚨 SUSPENSIÓN POR PIRATERÍA: Acceso revocado debido a inicio de sesión duplicado.")
                st.stop()
        else:
            base_datos_global[codigo] = st.session_state["mi_session_id"]

# ========================================================
# --- FACHADA DE ACCESO PÚBLICA (MATRIZ BIOENERGÉTICA) ---
# ========================================================
if not st.session_state["autenticado"]:
    st.markdown("<h1 class='main-title'>chonps<span class='main-title-suffix'>lab</span></h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Aprende rápido. Rompe las barreras biológicas.</p>", unsafe_allow_html=True)
    
    # PANEL VISUAL SOFISTICADO: Integrado al fondo con bordes neón azul translúcido
    st.markdown("""
    <div class='bio-panel'>
        <span class='panel-hook'>¿Listo para aprender rápido con tu laboratorio digital?</span>
        <p class='panel-text'>
            Sincroniza tu entorno de tronco común. Regula las variables moleculares de la materia viva y observa las consecuencias homeostáticas en tiempo real.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    st.markdown("<h3 style='font-weight: 600; margin-top: 10px;'>Sincronización del Entorno Analítico</h3>", unsafe_allow_html=True)
    st.write("Introduce tu clave de acceso de 30 días para validar el estado de matrícula y encender los simuladores.")
    
    codigo_input = st.text_input("Licencia de Acceso Digital (Token Único):", type="password", placeholder="Introduce tu código aquí...")
    
    if st.button("Activar Reactores Moleculares", use_container_width=True):
        codigo_limpio = codigo_input.strip().upper()
        if codigo_limpio in CODIGOS_VIGENTES:
            base_datos_global[codigo_limpio] = st.session_state["mi_session_id"]
            st.session_state["autenticado"] = True
            st.session_state["codigo_ingresado"] = codigo_limpio
            st.success("Conexión establecida con éxito. Sincronizando interfaz...")
            time.sleep(0.5)
            st.rerun()
        else:
            st.error("Código de licencia inválido o expirado. Verifica tu suscripción mensual.")

# ========================================================
# --- CONSOLA PRIVADA DE ESTUDIANTES (ChonpsLab) ---
# ========================================================
else:
    radar_seguridad_pasivo()
    verificar_bloqueo_pirateria()

    st.markdown("""
    <div class='console-header'>
        <h2 style='margin:0; color: #00e5ff; font-weight: 700;'>ChonpsLab: Consola de Simulación Avanzada</h2>
        <span style='color: #90a4ae; font-size: 0.85rem;'>Ecosistema de Ciencias de la Salud Protegido</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Barra lateral — Monitor de Signos
    with st.sidebar:
        st.markdown("<h3 style='font-weight:600; margin-bottom:15px;'>Monitor de Estado</h3>", unsafe_allow_html=True)
        st.markdown("<div class='sidebar-monitor'><span style='font-size:0.8rem; color:#90a4ae; text-transform:uppercase;'>Estabilidad (Vidas)</span><br><b style='font-size:1.6rem; color:#f44336;'>{} / 3</b></div>".format(st.session_state.vidas), unsafe_allow_html=True)
        st.markdown("<div class='sidebar-monitor'><span style='font-size:0.8rem; color:#90a4ae; text-transform:uppercase;'>Rigor (Puntos)</span><br><b style='font-size:1.6rem; color:#00e5ff;'>{}</b></div>".format(st.session_state.puntos), unsafe_allow_html=True)
        
        st.write("---")
        st.markdown("<h4 style='font-weight:600;'>Navegación Curricular</h4>", unsafe_allow_html=True)
        if st.sidebar.button("Bloque 0: Fundamentos Químicos", use_container_width=True):
            st.session_state.bloque_actual = 0
            st.session_state.simulacion_ejecutada = False
            st.rerun()
        if st.sidebar.button("Bloque 1: Agua y Equilibrio del pH", use_container_width=True):
            st.session_state.bloque_actual = 1
            st.session_state.simulacion_ejecutada = False
            st.rerun()
            
        st.write("---")
        if st.button("Desconectar Sesión de Forma Segura", use_container_width=True):
            if st.session_state["codigo_ingresado"] in base_datos_global:
                if base_datos_global[st.session_state["codigo_ingresado"]] == st.session_state["mi_session_id"]:
                    del base_datos_global[st.session_state["codigo_ingresado"]]
            st.session_state["autenticado"] = False
            st.rerun()

    if st.session_state.vidas <= 0:
        st.markdown("""
        <div class='spectrometer-card-error'>
            <div class='spectrometer-title' style='color:#f44336;'>Falla Homeostática Crítica</div>
            El sistema ha entrado en inestabilidad irreversible. El reactor ChonpsLab se ha bloqueado.
        </div>
        """, unsafe_allow_html=True)
        if st.button("Inyectar Nuevos Reactores y Reiniciar", use_container_width=True):
            st.session_state.vidas = 3
            st.session_state.puntos = 0
            st.session_state.simulacion_ejecutada = False
            st.session_state.estado_sistema = "En Espera"
            st.rerun()
    else:
        # CONTENIDO BLOQUE 0
        if st.session_state.bloque_actual == 0:
            st.subheader("Ficha de Protocolo 0: Enlaces y Electronegatividad")
            with st.expander("Ver Sustento Teórico del Enlace Bioquímico", expanded=True):
                st.markdown("""
                Los sistemas vivos están estructurados a partir del ensamblaje de los bioelementos primarios (**CHONPS**). 
                La interacción espacial de estos átomos depende estrictamente de su **Electronegatividad**.
                """)

            st.write("---")
            st.markdown("<h3>Reactor de Enlaces Moleculares</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                atomo_1 = st.selectbox("Elemento Primario del Núcleo:", ["Oxígeno (Fuerza: 3.44)", "Carbono (Fuerza: 2.55)"])
            with col2:
                atomo_2 = st.selectbox("Elemento de Interacción Orbital:", ["Hidrógeno (Fuerza: 2.20)", "Oxígeno (Fuerza: 3.44)"])
                
            if st.button("Disparar Reacción Térmica", use_container_width=True):
                st.session_state.simulacion_ejecutada = True
                verificar_bloqueo_pirateria()
                
                es_polar = "Oxígeno" in atomo_1 and "Hidrógeno" in atomo_2
                es_apolar = "Carbono" in atomo_1 and "Hidrógeno" in atomo_2
                es_error = "Oxígeno" in atomo_1 and "Oxígeno" in atomo_2
                
                if es_polar:
                    st.session_state.estado_sistema = "Enlace Covalente Polar (Dipolo Eléctrico Activo)"
                    st.session_state.resultado_texto = "Análisis molecular impecable. El Oxígeno retiene la carga parcial negativa y el Hidrógeno la positiva."
                    st.session_state.puntos += 100
                elif es_apolar:
                    st.session_state.estado_sistema = "Enlace Covalente No Polar (Geometría Simétrica)"
                    st.session_state.resultado_texto = "Configuración correcta. Las fuerzas del Carbono y el Hidrógeno se equilibran de forma justa."
                    st.session_state.puntos += 100
                elif es_error:
                    st.session_state.estado_sistema = "Molécula Gaseosa Homogénea (O2)"
                    st.session_state.resultado_texto = "Conflicto de variables en fluidos. Produce oxígeno molecular (O₂), incapaz de interactuar como dipolo."
                    st.session_state.vidas -= 1
                st.rerun()

        # CONTENIDO BLOQUE 1
        elif st.session_state.bloque_actual == 1:
            st.subheader("Ficha de Protocolo 1: Dinámica del Agua y Equilibrio del pH")
            with st.expander("Ver Sustento Teórico de la Disociación Iónica", expanded=True):
                st.markdown("""
                El agua ($H_2O$) representa el disolvente universal de la homeostasis biológica en todo organismo vivo.
                """)

            st.write("---")
            st.markdown("<h3>Analizador de Amortiguación Extracelular</h3>", unsafe_allow_html=True)
            
            solucion_inyectada = st.selectbox(
                "Seleccione la solución de infusión y el estado del medio interno:",
                [
                    "Ácido Clorhídrico (HCl) puro inyectado en Agua Destilada neutra",
                    "Ácido Clorhídrico (HCl) inyectado en Plasma con Amortiguador Bicarbonato (HCO3-)",
                    "Hidróxido de Sodio (NaOH) puro inyectado en Plasma sin sistemas amortiguadores"
                ]
            )
            
            if st.button("Confirmar Infusión Química", use_container_width=True):
                st.session_state.simulacion_ejecutada = True
                verificar_bloqueo_pirateria()
                
                if "Agua Destilada" in solucion_inyectada:
                    st.session_state.estado_sistema = "Acidosis Plasmática Crítica (pH = 2.0)"
                    st.session_state.resultado_texto = "Falla del medio interno. El HCl se disocia por completo liberando un exceso masivo de protones (H+)."
                    st.session_state.vidas -= 1
                elif "Amortiguador Bicarbonato" in solucion_inyectada:
                    st.session_state.estado_sistema = "Homeostasis Sanguínea Estable (pH = 7.4)"
                    st.session_state.resultado_texto = "Compensación química exitosa. El Bicarbonato captura los protones libres del medio."
                    st.session_state.puntos += 150
                elif "Hidróxido de Sodio" in solucion_inyectada:
                    st.session_state.estado_sistema = "Alcalosis Metabólica Severa (pH = 11.0)"
                    st.session_state.resultado_texto = "Desequilibrio catiónico. El NaOH libera grupos oxhidrilo (OH-) que secuestran los protones libres."
                    st.session_state.vidas -= 1
                st.rerun()

        # ESPECTRÓMETRO DIGITAL (MONITOR DE SALIDA)
        if st.session_state.simulacion_ejecutada:
            st.write("---")
            es_error_sistema = "Molécula Gaseosa" in st.session_state.estado_sistema or "Crítica" in st.session_state.estado_sistema or "Severa" in st.session_state.estado_sistema
            
            if es_error_sistema:
                st.markdown(f"""
                <div class='spectrometer-card-error'>
                    <div class='spectrometer-title' style='color:#ff5252;'>Lectura del Espectrómetro: Anomalía en el Medio</div>
                    <strong style='font-size:1.1rem; color:#ff8a80;'>Estatus: {st.session_state.estado_sistema}</strong><br><br>
                    {st.session_state.resultado_texto}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='spectrometer-card-success'>
                    <div class='spectrometer-title' style='color:#69f0ae;'>Lectura del Espectrómetro: Estabilidad Óptima</div>
                    <strong style='font-size:1.1rem; color:#b9f6ca;'>Estatus: {st.session_state.estado_sistema}</strong><br><br>
                    {st.session_state.resultado_texto}
                </div>
                """, unsafe_allow_html=True)
                
            st.write("")
            if st.button("Limpiar Cámara de Inyección", use_container_width=True):
                st.session_state.simulacion_ejecutada = False
                st.rerun()

    st.write("---")
    if st.button("Sincronizar Canales de Red"):
        st.rerun()
