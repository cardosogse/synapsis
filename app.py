import streamlit as st
import time

# Configuración de la página
st.set_page_config(page_title="Synapsis AI", page_icon="🔐", layout="centered")

# --- BITÁCORA GLOBAL COMPARTIDA (EL MURO DE ACERO) ---
# Esto obliga al servidor a compartir la información entre TODOS los dispositivos del mundo
@st.cache_resource
def obtener_base_datos_global():
    return {} # Formato global: {"codigo_licencia": "session_id_del_ultimo_dispositivo"}

base_datos_global = obtener_base_datos_global()

# Lista de códigos válidos de 30 días
CODIGOS_VALIDOS = ["KAIZEN-MES-SUSCRIPCION", "VET-ELITE-30DAYS", "SYNAPSIS-PRO"]

# Generar un identificador único para la pestaña actual
if "mi_session_id" not in st.session_state:
    st.session_state["mi_session_id"] = str(time.time())

# Estados locales de la pestaña
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
if "codigo_ingresado" not in st.session_state:
    st.session_state["codigo_ingresado"] = ""

# --- CONTROLADOR DE PIRATERÍA GLOBAL ---
if st.session_state["autenticado"]:
    codigo = st.session_state["codigo_ingresado"]
    # Si otra pantalla registró su ID para este mismo código, expulsamos a esta pestaña
    if base_datos_global.get(codigo) != st.session_state["mi_session_id"]:
        st.session_state["autenticado"] = False
        st.error("🚨 SUSPENSIÓN POR PIRATERÍA: Se detectó doble inicio de sesión simultáneo. Tu acceso en este dispositivo ha sido revocado.")
        st.info("💡 Cada suscripción mensual es individual. Para usar Synapsis en múltiples pantallas, adquiere una licencia adicional.")
        st.stop()

# --- INTERFAZ DE ACCESO ---
if not st.session_state["autenticado"]:
    st.title("🔐 Synapsis")
    st.subheader("Acceso a la Suscripción Mensual")
    st.write("Introduce tu código de licencia vigente de 30 días para sincronizarte con el Tutor de Inteligencia Artificial.")
    
    codigo_input = st.text_input("Código de Licencia:", type="password", placeholder="Introduce tu código aquí...")
    
    if st.button("Validar e Ingresar"):
        if codigo_input in CODIGOS_VALIDOS:
            # Reclamar el trono global para este dispositivo
            base_datos_global[codigo_input] = st.session_state["mi_session_id"]
            st.session_state["autenticado"] = True
            st.session_state["codigo_ingresado"] = codigo_input
            st.success("¡Licencia validada correctamente! Sincronizando...")
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ Código inválido o suscripción expirada. Verifica tu pago mensual.")
else:
    # --- INTERFAZ COMERCIAL DEL ALUMNO ---
    st.title("🧠 Synapsis: Tutor de Élite")
    st.success("¡Conexión Blindada y Segura!")
    
    st.write("---")
    
    # Menú de navegación estable (Evita que se congele o se reinicie la app)
    modulo = st.selectbox("Selecciona la Unidad de Aprendizaje:", 
                          ["Fase 1: Introducción Teórica", 
                           "Fase 2: Rigor Técnico", 
                           "Fase 3: Evaluación Virtual"])
    
    st.write("---")

    if modulo == "Fase 1: Introducción Teórica":
        st.header("🔬 Unidad 1: Biología Celular y Molecular")
        st.write("Bienvenido al andamiaje pedagógico automatizado. Aquí inicia tu entrenamiento científico.")
        st.info("Estás en el bloque teórico base.")
            
    elif modulo == "Fase 2: Rigor Técnico":
        st.header("🧪 Fase 2: Análisis Clínico y Veterinario")
        st.write("Contenido exclusivo de alta especialización para la facultad. Analizando estructuras moleculares avanzadas.")
        
    elif modulo == "Fase 3: Evaluación Virtual":
        st.header("📊 Fase 3: Simulador de Examen")
        st.write("Pon a prueba tus conocimientos con el motor de IA adaptativo.")

    # Botón de patrullaje para el alumno
    if st.button("🔄 Sincronizar Estado"):
        st.rerun()
