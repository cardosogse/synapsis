import streamlit as st
import time

# 1. CONFIGURACIÓN DEL CHASIS DE NAVEGACIÓN
st.set_page_config(page_title="SynapsisLab", page_icon="🧠", layout="centered")

# --- ESTILOS CSS NATIVOS PARA ERGONOMÍA VISUAL PREMIUM ---
st.markdown("""
<style>
    /* Estilos globales de tipografía y fondos */
    .main-title {
        text-align: center; 
        color: #0288d1; 
        font-size: 3.8rem; 
        font-weight: 800; 
        letter-spacing: 3px;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center; 
        font-style: italic; 
        color: #666; 
        font-size: 1.1rem; 
        font-weight: 400;
        margin-top: 0px;
        margin-bottom: 5px;
    }
    .question-hook {
        text-align: center; 
        color: #0288d1; 
        font-size: 1.2rem; 
        font-weight: 600; 
        margin-top: 0px;
        margin-bottom: 25px;
    }
    /* Contenedores de la interfaz del Laboratorio */
    .console-header {
        background-color: #f8f9fa;
        border-left: 5px solid #0288d1;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 20px;
    }
    .spectrometer-card-success {
        background-color: #e8f5e9;
        border: 1px solid #c8e6c9;
        border-left: 6px solid #4caf50;
        padding: 20px;
        border-radius: 6px;
        margin-top: 15px;
    }
    .spectrometer-card-error {
        background-color: #ffebee;
        border: 1px solid #ffcdd2;
        border-left: 6px solid #f44336;
        padding: 20px;
        border-radius: 6px;
        margin-top: 15px;
    }
    .spectrometer-title {
        color: #333;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    /* Monitor de la barra lateral */
    .sidebar-monitor {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 12px;
        border-radius: 4px;
        margin-bottom: 10px;
        text-align: center;
    }
</style>
""", unsafe_style=True)

# --- BITÁCORA GLOBAL COMPARTIDA (EL MURO DE ACERO ANTIPIRATERÍA) ---
@st.cache_resource
def obtener_base_datos_global():
    return {}  # Estructura: {"codigo_licencia": "session_id_del_ultimo_dispositivo"}

base_datos_global = obtener_base_datos_global()

# Licencias autorizadas para el Tronco Común de Ciencias de la Salud
CODIGOS_VIGENTES = ["SYNAPSIS-PRO", "VET-BIOQUIMICA-2026", "MED-ELITE-30DAYS"]

if "mi_session_id" not in st.session_state:
    st.session_state["mi_session_id"] = str(time.time_ns())

# Estados locales de control de sesión
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
if "codigo_ingresado" not in st.session_state:
    st.session_state["codigo_ingresado"] = ""

# --- VARIABLES DE ESTADO LOCAL DEL LABORATORIO ---
if "vidas" not in st.session_state:
    st.session_state["vidas"] = 3
if "puntos" not in st.session_state:
    st.session_state["puntos"] = 0
if "bloque_actual" not in st.session_state:
    st.session_state["bloque_actual"] = 0  # 0 = Fundamentos, 1 = Agua y pH
if "simulacion_ejecutada" not in st.session_state:
    st.session_state["simulacion_ejecutada"] = False
if "resultado_texto" not in st.session_state:
    st.session_state["resultado_texto"] = ""
if "estado_sistema" not in st.session_state:
    st.session_state["estado_sistema"] = "En Espera"

# --- RADAR PASIVO DE PIRATERÍA (Background Polling cada 5 segundos) ---
@st.fragment(run_every=5)
def radar_seguridad_pasivo():
    if st.session_state["autenticado"]:
        codigo = st.session_state["codigo_ingresado"]
        if base_datos_global.get(codigo) != st.session_state["mi_session_id"]:
            st.rerun()

def verificar_bloqueo_pirateria():
    if st.session_state["autenticado"]:
        codigo = st.session_state["codigo_ingresado"]
        if base_datos_global.get(codigo) != st.session_state["mi_session_id"]:
            st.session_state["autenticado"] = False
            st.session_state["codigo_ingresado"] = ""
            st.error("🚨 SUSPENSIÓN POR PIRATERÍA: Se detectó un doble inicio de sesión simultáneo. Tu acceso en este dispositivo ha sido revocado automáticamente.")
            st.stop()

# ========================================================
# --- FACHADA DE ACCESO PÚBLICA (DISEÑO GEOMÉTRICO LIMPIO) ---
# ========================================================
if not st.session_state["autenticado"]:
    st.markdown("<h1 class='main-title'>SYNAPSIS</h1>", unsafe_style=True)
    st.markdown("<p class='sub-title'>Aprende rápido. Rompe las barreras biológicas.</p>", unsafe_style=True)
    st.markdown("<p class='question-hook'>¿Listo para aprender rápido con tu laboratorio digital?</p>", unsafe_style=True)
    
    st.write("---")
    
    # Contenedor estético para el Arte Digital de Redes Neuronales
    st.markdown("""
    <div style='background-color: #f1f8e9; border: 1px dashed #8bc34a; padding: 20px; text-align: center; border-radius: 4px; color: #33691e; font-size: 0.95rem; font-weight: 500;'>
        [Módulo de Interconexión Sináptica: Animación de Redes Neuronales Nativas en Desarrollo]
    </div>
    """, unsafe_style=True)
    
    st.markdown("""
    <br>
    <h3 style='color: #333; font-weight: 600;'>Sincronización del Entorno Analítico</h3>
    Introduzca su clave de acceso individual de 30 días para validar el estado de matrícula y activar los reactores digitales de tronco común.
    """, unsafe_style=True)
    
    codigo_input = st.text_input("Licencia de Acceso Digital (Token Único):", type="password", placeholder="Introduzca el código de suscripción...")
    
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
            st.error("Código de licencia inválido o expirado. Verifique su suscripción mensual.")

# ========================================================
# --- CONSOLA PRIVADA DE ESTUDIANTES (SynapsisLab) ---
# ========================================================
else:
    radar_seguridad_pasivo()
    verificar_bloqueo_pirateria()

    # Encabezado Ergonómico de la Consola
    st.markdown("""
    <div class='console-header'>
        <h2 style='margin:0; color: #01579b; font-weight: 700;'>SynapsisLab: Consola de Simulación</h2>
        <span style='color: #555; font-size: 0.85rem;'>Entorno Clínico Protegido | Matrícula Activa: {}</span>
    </div>
    """.format(st.session_state['codigo_ingresado']), unsafe_style=True)
    
    # Barra lateral — Monitor de Signos Homeostáticos del Alumno
    with st.sidebar:
        st.markdown("<h3 style='color: #333; font-weight:600; margin-bottom:15px;'>Monitor de Estado</h3>", unsafe_style=True)
        
        st.markdown("<div class='sidebar-monitor'><span style='font-size:0.8rem; color:#666; text-transform:uppercase;'>Estabilidad (Vidas)</span><br><b style='font-size:1.6rem; color:#d32f2f;'>{} / 3</b></div>".format(st.session_state.vidas), unsafe_style=True)
        st.markdown("<div class='sidebar-monitor'><span style='font-size:0.8rem; color:#666; text-transform:uppercase;'>Rigor (Puntos)</span><br><b style='font-size:1.6rem; color:#1976d2;'>{}</b></div>".format(st.session_state.puntos), unsafe_style=True)
        
        st.write("---")
        st.markdown("<h4 style='color: #333; font-weight:600;'>Navegación Curricular</h4>", unsafe_style=True)
        
        # Selector de bloques temáticos integrados
        if st.sidebar.button("Bloque 0: Fundamentos Quím
